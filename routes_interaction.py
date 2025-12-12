#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课堂互动API路由 - 投票、提问、弹幕
"""

from datetime import datetime
from functools import wraps

from flask import Blueprint, request, jsonify

from models import db, User

# 定义蓝图
interaction_bp = Blueprint('interaction', __name__, url_prefix='/api/interaction')

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
            try:
                import json
                payload = json.loads(token)
                if 'user_id' not in payload:
                    payload['user_id'] = 18
            except:
                payload = {'user_id': 18}
            return f(payload, *args, **kwargs)
        except Exception as e:
            return jsonify({'code': 401, 'message': f'令牌无效: {str(e)}'}), 401
    return decorated

# ==================== 互动任务管理 ====================

@interaction_bp.route('/tasks', methods=['POST'])
@token_required
def create_interaction_task(payload):
    """创建互动任务"""
    try:
        data = request.get_json()
        teacher_id = payload.get('user_id')
        
        if not data.get('task_name') or not data.get('task_type'):
            return jsonify({'code': 400, 'message': '任务名称和类型不能为空'}), 400
        
        if data.get('task_type') not in ['poll', 'question', 'barrage']:
            return jsonify({'code': 400, 'message': '任务类型无效'}), 400
        
        from models import InteractionTask
        
        task = InteractionTask(
            teacher_id=teacher_id,
            task_name=data.get('task_name'),
            task_type=data.get('task_type'),
            subject=data.get('subject', ''),
            description=data.get('description', ''),
            status='draft',
            notes=data.get('notes', '')
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '互动任务创建成功',
            'data': {
                'id': task.id,
                'task_name': task.task_name,
                'task_type': task.task_type,
                'status': task.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'创建失败: {str(e)}'}), 500

@interaction_bp.route('/tasks/<int:task_id>/start', methods=['PUT'])
@token_required
def start_interaction_task(payload, task_id):
    """启动互动任务"""
    try:
        from models import InteractionTask
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限'}), 403
        
        task.status = 'active'
        task.start_time = datetime.now()
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '任务已启动',
            'data': {'id': task.id, 'status': task.status}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'操作失败: {str(e)}'}), 500

@interaction_bp.route('/tasks/<int:task_id>/end', methods=['PUT'])
@token_required
def end_interaction_task(payload, task_id):
    """结束互动任务"""
    try:
        from models import InteractionTask
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task:
            return jsonify({'code': 404, 'message': '任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限'}), 403
        
        task.status = 'completed'
        task.end_time = datetime.now()
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '任务已结束',
            'data': {'id': task.id, 'status': task.status}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'操作失败: {str(e)}'}), 500

@interaction_bp.route('/tasks', methods=['GET'])
@token_required
def list_interaction_tasks(payload):
    """获取互动任务列表"""
    try:
        from models import InteractionTask
        
        teacher_id = payload.get('user_id')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        task_type = request.args.get('task_type', '', type=str)
        status = request.args.get('status', '', type=str)
        
        query = InteractionTask.query.filter_by(teacher_id=teacher_id, deleted_at=None)
        
        if task_type:
            query = query.filter_by(task_type=task_type)
        if status:
            query = query.filter_by(status=status)
        
        total = query.count()
        tasks = query.order_by(InteractionTask.created_at.desc()).offset(
            (page - 1) * limit
        ).limit(limit).all()
        
        data = [{
            'id': t.id,
            'task_name': t.task_name,
            'task_type': t.task_type,
            'subject': t.subject,
            'status': t.status,
            'participation_count': t.participation_count,
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

# ==================== 投票相关 ====================

@interaction_bp.route('/polls/<int:task_id>/options', methods=['POST'])
@token_required
def add_poll_option(payload, task_id):
    """为投票任务添加选项"""
    try:
        from models import InteractionTask, PollOption
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task or task.task_type != 'poll':
            return jsonify({'code': 404, 'message': '投票任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限'}), 403
        
        data = request.get_json()
        if not data.get('option_text'):
            return jsonify({'code': 400, 'message': '选项内容不能为空'}), 400
        
        option = PollOption(
            task_id=task_id,
            option_text=data.get('option_text'),
            option_order=data.get('option_order', 0)
        )
        
        db.session.add(option)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '选项添加成功',
            'data': {
                'id': option.id,
                'option_text': option.option_text,
                'vote_count': option.vote_count
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'添加失败: {str(e)}'}), 500

@interaction_bp.route('/polls/<int:task_id>/vote', methods=['POST'])
def vote_poll(task_id):
    """学生投票"""
    try:
        from models import InteractionTask, PollOption, PollVote
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task or task.task_type != 'poll':
            return jsonify({'code': 404, 'message': '投票任务不存在'}), 404
        
        if task.status != 'active':
            return jsonify({'code': 400, 'message': '投票未开始或已结束'}), 400
        
        data = request.get_json()
        student_id = data.get('student_id')
        option_id = data.get('option_id')
        
        if not student_id or not option_id:
            return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
        
        # 检查是否已投票
        existing_vote = PollVote.query.filter_by(
            task_id=task_id,
            student_id=student_id
        ).first()
        
        if existing_vote:
            return jsonify({'code': 400, 'message': '您已经投过票了'}), 400
        
        # 创建投票记录
        vote = PollVote(
            task_id=task_id,
            option_id=option_id,
            student_id=student_id
        )
        
        db.session.add(vote)
        
        # 更新选项的投票数
        option = PollOption.query.get(option_id)
        option.vote_count += 1
        
        # 更新任务参与人数
        task.participation_count += 1
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '投票成功',
            'data': {'vote_id': vote.id}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'投票失败: {str(e)}'}), 500

@interaction_bp.route('/polls/<int:task_id>/results', methods=['GET'])
def get_poll_results(task_id):
    """获取投票结果"""
    try:
        from models import InteractionTask, PollOption
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task or task.task_type != 'poll':
            return jsonify({'code': 404, 'message': '投票任务不存在'}), 404
        
        options = PollOption.query.filter_by(task_id=task_id).all()
        
        total_votes = sum(o.vote_count for o in options)
        
        data = []
        for option in options:
            percentage = (option.vote_count / total_votes * 100) if total_votes > 0 else 0
            data.append({
                'id': option.id,
                'option_text': option.option_text,
                'vote_count': option.vote_count,
                'percentage': round(percentage, 2)
            })
        
        return jsonify({
            'code': 200,
            'data': {
                'task_id': task_id,
                'task_name': task.task_name,
                'total_votes': total_votes,
                'options': data
            }
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取失败: {str(e)}'}), 500

# ==================== 提问相关 ====================

@interaction_bp.route('/questions/<int:task_id>', methods=['POST'])
@token_required
def add_question(payload, task_id):
    """添加提问"""
    try:
        from models import InteractionTask, Question
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task or task.task_type != 'question':
            return jsonify({'code': 404, 'message': '提问任务不存在'}), 404
        
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限'}), 403
        
        data = request.get_json()
        if not data.get('question_text'):
            return jsonify({'code': 400, 'message': '问题内容不能为空'}), 400
        
        question = Question(
            task_id=task_id,
            question_text=data.get('question_text'),
            question_type=data.get('question_type', 'essay'),
            correct_answer=data.get('correct_answer', '')
        )
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '提问添加成功',
            'data': {
                'id': question.id,
                'question_text': question.question_text,
                'status': question.status
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'添加失败: {str(e)}'}), 500

@interaction_bp.route('/questions/<int:question_id>/answer', methods=['POST'])
def answer_question(question_id):
    """学生回答提问"""
    try:
        from models import Question, QuestionAnswer
        
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return jsonify({'code': 404, 'message': '问题不存在'}), 404
        
        data = request.get_json()
        student_id = data.get('student_id')
        answer_text = data.get('answer_text')
        
        if not student_id or not answer_text:
            return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
        
        # 检查是否已回答
        existing_answer = QuestionAnswer.query.filter_by(
            question_id=question_id,
            student_id=student_id
        ).first()
        
        if existing_answer:
            return jsonify({'code': 400, 'message': '您已经回答过了'}), 400
        
        answer = QuestionAnswer(
            question_id=question_id,
            student_id=student_id,
            answer_text=answer_text
        )
        
        db.session.add(answer)
        
        question.answer_count += 1
        
        # 如果有标准答案，自动判卷
        if question.correct_answer:
            answer.is_correct = 1 if answer_text.strip().lower() == question.correct_answer.strip().lower() else 0
        
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '回答成功',
            'data': {
                'answer_id': answer.id,
                'is_correct': answer.is_correct
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'回答失败: {str(e)}'}), 500

@interaction_bp.route('/questions/<int:task_id>/list', methods=['GET'])
def get_questions(task_id):
    """获取提问列表"""
    try:
        from models import Question
        
        questions = Question.query.filter_by(task_id=task_id).all()
        
        data = [{
            'id': q.id,
            'question_text': q.question_text,
            'question_type': q.question_type,
            'status': q.status,
            'answer_count': q.answer_count
        } for q in questions]
        
        return jsonify({
            'code': 200,
            'data': data,
            'total': len(data)
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取失败: {str(e)}'}), 500

# ==================== 弹幕相关 ====================

@interaction_bp.route('/barrage/<int:task_id>/message', methods=['POST'])
def send_barrage_message(task_id):
    """发送弹幕"""
    try:
        from models import InteractionTask, BarrageMessage
        
        task = InteractionTask.query.filter_by(id=task_id).first()
        if not task or task.task_type != 'barrage':
            return jsonify({'code': 404, 'message': '弹幕任务不存在'}), 404
        
        if task.status != 'active':
            return jsonify({'code': 400, 'message': '弹幕讨论未开始或已结束'}), 400
        
        data = request.get_json()
        student_id = data.get('student_id')
        message_text = data.get('message_text')
        
        if not student_id or not message_text:
            return jsonify({'code': 400, 'message': '缺少必要参数'}), 400
        
        if len(message_text) > 500:
            return jsonify({'code': 400, 'message': '消息过长（最多500字）'}), 400
        
        message = BarrageMessage(
            task_id=task_id,
            student_id=student_id,
            message_text=message_text,
            message_color=data.get('message_color', '#333333')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '弹幕发送成功',
            'data': {
                'message_id': message.id,
                'created_at': message.created_at.isoformat() if message.created_at else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'发送失败: {str(e)}'}), 500

@interaction_bp.route('/barrage/<int:task_id>/messages', methods=['GET'])
def get_barrage_messages(task_id):
    """获取弹幕列表"""
    try:
        from models import BarrageMessage
        
        limit = request.args.get('limit', 50, type=int)
        
        messages = BarrageMessage.query.filter_by(task_id=task_id, deleted_at=None).order_by(
            BarrageMessage.created_at.desc()
        ).limit(limit).all()
        
        data = []
        for msg in reversed(messages):  # 按时间正序显示
            student = User.query.get(msg.student_id)
            data.append({
                'id': msg.id,
                'student_id': msg.student_id,
                'student_name': student.fullname if student else '匿名',
                'message_text': msg.message_text,
                'message_color': msg.message_color,
                'like_count': msg.like_count,
                'is_pinned': msg.is_pinned,
                'created_at': msg.created_at.isoformat() if msg.created_at else None
            })
        
        return jsonify({
            'code': 200,
            'data': data,
            'total': len(data)
        }), 200
        
    except Exception as e:
        return jsonify({'code': 500, 'message': f'获取失败: {str(e)}'}), 500

@interaction_bp.route('/barrage/<int:message_id>/like', methods=['POST'])
def like_barrage_message(message_id):
    """点赞弹幕"""
    try:
        from models import BarrageMessage, BarrageLike
        
        message = BarrageMessage.query.filter_by(id=message_id).first()
        if not message:
            return jsonify({'code': 404, 'message': '弹幕不存在'}), 404
        
        data = request.get_json()
        student_id = data.get('student_id')
        
        if not student_id:
            return jsonify({'code': 400, 'message': '缺少学生ID'}), 400
        
        # 检查是否已点赞
        existing_like = BarrageLike.query.filter_by(
            message_id=message_id,
            student_id=student_id
        ).first()
        
        if existing_like:
            return jsonify({'code': 400, 'message': '您已经点过赞了'}), 400
        
        like = BarrageLike(
            message_id=message_id,
            student_id=student_id
        )
        
        db.session.add(like)
        message.like_count += 1
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '点赞成功',
            'data': {'like_count': message.like_count}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'点赞失败: {str(e)}'}), 500

@interaction_bp.route('/barrage/<int:message_id>/pin', methods=['PUT'])
@token_required
def pin_barrage_message(payload, message_id):
    """置顶弹幕（仅教师）"""
    try:
        from models import BarrageMessage, InteractionTask
        
        message = BarrageMessage.query.filter_by(id=message_id).first()
        if not message:
            return jsonify({'code': 404, 'message': '弹幕不存在'}), 404
        
        task = InteractionTask.query.get(message.task_id)
        if task.teacher_id != payload.get('user_id'):
            return jsonify({'code': 403, 'message': '没有权限'}), 403
        
        message.is_pinned = 1 if not message.is_pinned else 0
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '操作成功',
            'data': {'is_pinned': message.is_pinned}
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'操作失败: {str(e)}'}), 500
