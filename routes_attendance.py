#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课堂考勤API路由
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from datetime import datetime, timedelta
import uuid
import qrcode
import io
import base64
from models import db, User
from sqlalchemy import and_, or_, func

# 定义蓝图
attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

# JWT验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'code': 401, 'message': '缺少授权令牌'}), 401
        try:
            token = token.replace('Bearer ', '')
            # 简化的token验证，为了演示，仅检查token是否存在
            # 实际应用中应使用PyJWT验证
            try:
                import json
                payload = json.loads(token)
                # 如果是json，此处需要阅放字段
                if 'user_id' not in payload:
                    # 如果没有user_id，使用黑字段
                    payload['user_id'] = 18
            except:
                # 不是json，就是简单的串行令牌，需要要标源token来获取user_id
                # 为了演示，仅需要token存在即可，使用黑字段user_id=18
                payload = {'user_id': 18}
            return f(payload, *args, **kwargs)
        except Exception as e:
            return jsonify({'code': 401, 'message': f'令牌无效: {str(e)}'}), 401
    return decorated

# ==================== 考勤任务管理 ====================

@attendance_bp.route('/tasks', methods=['POST'])
@token_required
def create_attendance_task(payload):
    """创建考勤任务"""
    try:
        data = request.get_json()
        teacher_id = payload.get('user_id')
        
        # 验证必填字段
        if not data.get('task_name'):
            return jsonify({'code': 400, 'message': '考勤任务名称不能为空'}), 400
        
        # 生成任务码
        task_code = f"TASK{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8]}"
        
        # 创建任务
        from models import AttendanceTask
        task = AttendanceTask(
            teacher_id=teacher_id,
            task_name=data.get('task_name'),
            class_name=data.get('class_name', ''),
            subject=data.get('subject', ''),
            task_code=task_code,
            expected_count=data.get('expected_count', 0),
            notes=data.get('notes', '')
        )
        
        db.session.add(task)
        db.session.commit()
        
        # 生成二维码
        qr_data = {
            'task_id': task.id,
            'task_code': task_code,
            'teacher_id': teacher_id
        }
        qr_code_img = generate_qr_code(str(qr_data))
        
        task.qr_code = str(qr_data)
        task.qr_code_image = qr_code_img
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '考勤任务创建成功',
            'data': {
                'id': task.id,
                'task_code': task_code,
                'task_name': task.task_name,
                'qr_code': qr_code_img
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'创建失败: {str(e)}'}), 500

@attendance_bp.route('/tasks/<int:task_id>/start', methods=['PUT'])
@token_required
def start_attendance_task(payload, task_id):
    """开始考勤"""
    try:
        from models import AttendanceTask
        task = AttendanceTask.query.filter_by(id=task_id).first()
        
        if not task:
            return jsonify({'code': 404, 'message': '考勤任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限修改此任务'}), 403
        
        task.status = 'in_progress'
        task.start_time = datetime.now()
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '考勤已开始',
            'data': {'task_id': task.id, 'status': task.status}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'操作失败: {str(e)}'}), 500

@attendance_bp.route('/tasks/<int:task_id>/end', methods=['PUT'])
@token_required
def end_attendance_task(payload, task_id):
    """结束考勤"""
    try:
        from models import AttendanceTask, AttendanceRecord
        task = AttendanceTask.query.filter_by(id=task_id).first()
        
        if not task:
            return jsonify({'code': 404, 'message': '考勤任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限修改此任务'}), 403
        
        task.status = 'completed'
        task.end_time = datetime.now()
        
        # 统计出勤人数
        actual_count = AttendanceRecord.query.filter_by(
            task_id=task_id, is_present=1
        ).count()
        task.actual_count = actual_count
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '考勤已结束',
            'data': {
                'task_id': task.id,
                'status': task.status,
                'actual_count': actual_count
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'操作失败: {str(e)}'}), 500

@attendance_bp.route('/tasks', methods=['GET'])
@token_required
def list_attendance_tasks(payload):
    """获取教师的考勤任务列表"""
    try:
        from models import AttendanceTask
        teacher_id = payload.get('user_id')
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status', '', type=str)
        
        query = AttendanceTask.query.filter_by(teacher_id=teacher_id, deleted_at=None)
        
        if status:
            query = query.filter_by(status=status)
        
        total = query.count()
        tasks = query.order_by(AttendanceTask.created_at.desc()).offset(
            (page - 1) * limit
        ).limit(limit).all()
        
        data = [{
            'id': t.id,
            'task_name': t.task_name,
            'class_name': t.class_name,
            'subject': t.subject,
            'status': t.status,
            'expected_count': t.expected_count,
            'actual_count': t.actual_count,
            'created_at': t.created_at.isoformat() if t.created_at else None
        } for t in tasks]
        
        return jsonify({
            'code': 200,
            'data': data,
            'total': total,
            'page': page,
            'limit': limit
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取失败: {str(e)}'}), 500

# ==================== 学生签到 ====================

@attendance_bp.route('/check-in', methods=['POST'])
def check_in_student():
    """学生签到（支持二维码和手动输入）"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data.get('task_code') and not data.get('task_id'):
            return jsonify({'code': 400, 'message': '缺少考勤信息'}), 400
        
        if not data.get('student_id'):
            return jsonify({'code': 400, 'message': '学生ID不能为空'}), 400
        
        from models import AttendanceTask, AttendanceRecord
        
        # 查找任务
        if data.get('task_code'):
            task = AttendanceTask.query.filter_by(task_code=data.get('task_code')).first()
        else:
            task = AttendanceTask.query.filter_by(id=data.get('task_id')).first()
        
        if not task:
            return jsonify({'code': 404, 'message': '考勤任务不存在'}), 404
        
        # 检查任务状态
        if task.status != 'in_progress':
            return jsonify({'code': 400, 'message': '该考勤任务未进行中'}), 400
        
        # 检查是否已签到
        existing_record = AttendanceRecord.query.filter_by(
            task_id=task.id,
            student_id=data.get('student_id')
        ).first()
        
        if existing_record:
            return jsonify({'code': 400, 'message': '您已经签到过了'}), 400
        
        # 创建签到记录
        record = AttendanceRecord(
            task_id=task.id,
            teacher_id=task.teacher_id,
            student_id=data.get('student_id'),
            check_in_time=datetime.now(),
            check_in_method=data.get('check_in_method', 'qr_code'),
            is_present=1
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '签到成功',
            'data': {
                'record_id': record.id,
                'check_in_time': record.check_in_time.isoformat() if record.check_in_time else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'签到失败: {str(e)}'}), 500

@attendance_bp.route('/tasks/<int:task_id>/records', methods=['GET'])
@token_required
def get_attendance_records(payload, task_id):
    """获取考勤任务的学生签到记录"""
    try:
        from models import AttendanceTask, AttendanceRecord, TeacherStudent
        
        task = AttendanceTask.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'code': 404, 'message': '考勤任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限查看此任务'}), 403
        
        # 获取所有学生的签到记录
        students = db.session.query(TeacherStudent.student_id).filter_by(
            teacher_id=task.teacher_id
        ).all()
        student_ids = [s[0] for s in students]
        
        records = AttendanceRecord.query.filter_by(task_id=task_id).all()
        checked_student_ids = {r.student_id for r in records}
        
        # 构建响应数据
        data = []
        for record in records:
            student = User.query.get(record.student_id)
            data.append({
                'record_id': record.id,
                'student_id': record.student_id,
                'student_name': student.fullname if student else '',
                'check_in_time': record.check_in_time.isoformat() if record.check_in_time else None,
                'check_in_method': record.check_in_method,
                'is_present': record.is_present
            })
        
        # 添加未签到的学生
        for student_id in student_ids:
            if student_id not in checked_student_ids:
                student = User.query.get(student_id)
                data.append({
                    'record_id': None,
                    'student_id': student_id,
                    'student_name': student.fullname if student else '',
                    'check_in_time': None,
                    'check_in_method': None,
                    'is_present': 0
                })
        
        return jsonify({
            'code': 200,
            'data': data,
            'total': len(data),
            'checked_count': len([r for r in data if r['is_present'] == 1])
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取失败: {str(e)}'}), 500

@attendance_bp.route('/records/<int:record_id>', methods=['PUT'])
@token_required
def update_attendance_record(payload, record_id):
    """修改学生考勤状态（教师手动确认缺勤等）"""
    try:
        from models import AttendanceRecord, AttendanceTask
        
        record = AttendanceRecord.query.filter_by(id=record_id).first()
        if not record:
            return jsonify({'code': 404, 'message': '考勤记录不存在'}), 404
        
        task = AttendanceTask.query.get(record.task_id)
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限修改'}), 403
        
        data = request.get_json()
        
        if 'is_present' in data:
            record.is_present = data['is_present']
        if 'notes' in data:
            record.notes = data['notes']
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '考勤记录更新成功',
            'data': {'record_id': record.id}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'更新失败: {str(e)}'}), 500

# ==================== 考勤统计 ====================

@attendance_bp.route('/statistics/<int:student_id>', methods=['GET'])
@token_required
def get_student_attendance_stats(payload, student_id):
    """获取学生的考勤统计"""
    try:
        from models import AttendanceRecord
        
        # 当前月份
        today = datetime.now()
        month_start = today.replace(day=1)
        month_end = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # 查询该月的考勤记录
        records = AttendanceRecord.query.filter(
            and_(
                AttendanceRecord.student_id == student_id,
                AttendanceRecord.teacher_id == payload.get('user_id'),
                AttendanceRecord.created_at >= month_start,
                AttendanceRecord.created_at <= month_end
            )
        ).all()
        
        total = len(records)
        present = sum(1 for r in records if r.is_present == 1)
        absent = total - present
        attendance_rate = (present / total * 100) if total > 0 else 0
        
        return jsonify({
            'code': 200,
            'data': {
                'student_id': student_id,
                'total_classes': total,
                'present_count': present,
                'absent_count': absent,
                'attendance_rate': round(attendance_rate, 2)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取统计失败: {str(e)}'}), 500

# ==================== 辅助函数 ====================

def generate_qr_code(data):
    """生成二维码并返回Base64编码"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 转换为Base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"二维码生成失败: {str(e)}")
        return ""
