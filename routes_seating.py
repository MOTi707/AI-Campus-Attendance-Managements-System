"""
智能座位表路由 - 获取教师的学生姓名列表
"""

from flask import Blueprint, request, jsonify
from models import db, User, TeacherStudent
from jwt_utils import token_required

# 创建蓝图
seating_bp = Blueprint('seating', __name__, url_prefix='/api/seating')


@seating_bp.route('/students', methods=['GET'])
@token_required
def get_students_for_seating(payload):
    """
    获取教师的学生列表 (仅返回姓名)
    用于智能座位表
    
    请求:
    GET /api/seating/students
    Authorization: Bearer <TOKEN>
    
    响应:
    {
        "code": 200,
        "message": "获取成功",
        "data": [
            {"id": 19, "name": "何梦瑶"},
            {"id": 20, "name": "吕晨"},
            {"id": 21, "name": "施雨涵"},
            ...
        ]
    }
    """
    try:
        teacher_id = payload.get('user_id')
        
        # 获取该教师绑定的所有学生 (只需要ID和姓名)
        students = db.session.query(User.id, User.fullname).join(
            TeacherStudent,
            TeacherStudent.student_id == User.id
        ).filter(
            TeacherStudent.teacher_id == teacher_id,
            TeacherStudent.deleted_at == None,
            User.identity == 'student'
        ).all()
        
        if not students:
            return jsonify({
                'code': 200,
                'message': '获取成功',
                'data': []
            }), 200
        
        # 组装数据：只需要ID和姓名
        student_data = [
            {
                'id': student[0],
                'name': student[1]
            }
            for student in students
        ]
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': student_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取学生列表失败: {str(e)}'
        }), 500
