from flask import Blueprint, request, jsonify
from models import db, User
from jwt_utils import generate_token, token_required
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    try:
        data = request.get_json()
        
        # 验证必填字段（移除email，添加subject）
        required_fields = ['identity', 'username', 'fullname', 'password', 'subject']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'code': 400,
                    'message': f'缺少必填字段: {field}'
                }), 400
        
        # 验证身份字段
        if data['identity'] not in ['student', 'teacher']:
            return jsonify({
                'code': 400,
                'message': '身份信息错误，请选择学生或教师'
            }), 400
        
        # 验证密码长度
        if len(data['password']) < 6:
            return jsonify({
                'code': 400,
                'message': '密码至少需要6位'
            }), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username'], deleted_at=None).first():
            return jsonify({
                'code': 400,
                'message': '用户名已存在'
            }), 400
        
        # ... existing code ...
        
        # 创建新用户
        user = User(
            identity=data['identity'],
            username=data['username'],
            fullname=data['fullname'],
            subject=data.get('subject')
        )
        user.set_password(data['password'])
        
        # 生成令牌
        token = generate_token(user.id, user.identity, user.username)
        user.token = token
        
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': {
                'id': user.id,
                'identity': user.identity,
                'username': user.username,
                'fullname': user.fullname,
                'subject': user.subject,
                'token': token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'注册失败: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data or not data.get('identity') or not data.get('username') or not data.get('password'):
            return jsonify({
                'code': 400,
                'message': '缺少必填字段'
            }), 400
        
        # 验证身份字段
        if data['identity'] not in ['student', 'teacher']:
            return jsonify({
                'code': 400,
                'message': '身份信息错误'
            }), 400
        
        # 查询用户
        user = User.query.filter_by(
            identity=data['identity'],
            username=data['username'],
            deleted_at=None
        ).first()
        
        if not user:
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
        
        # 验证密码
        if not user.check_password(data['password']):
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
        
        # 生成新令牌
        token = generate_token(user.id, user.identity, user.username)
        user.token = token
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'id': user.id,
                'identity': user.identity,
                'username': user.username,
                'fullname': user.fullname,
                'subject': user.subject,
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'登录失败: {str(e)}'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(payload):
    """用户登出接口"""
    try:
        user_id = payload.get('user_id')
        user = User.query.get(user_id)
        
        if user:
            user.token = None
            db.session.commit()
        
        return jsonify({
            'code': 200,
            'message': '登出成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'登出失败: {str(e)}'
        }), 500


@auth_bp.route('/user', methods=['GET'])
@token_required
def get_user(payload):
    """获取当前用户信息"""
    try:
        user_id = payload.get('user_id')
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'code': 404,
                'message': '用户不存在'
            }), 404
        
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'获取失败: {str(e)}'
        }), 500
