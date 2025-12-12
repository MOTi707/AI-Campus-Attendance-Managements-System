import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


def generate_token(user_id, identity, username, expires_in=None):
    """生成JWT令牌"""
    if expires_in is None:
        expires_in = 30 * 24 * 3600  # 30天
    
    payload = {
        'user_id': user_id,
        'identity': identity,
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config.get('JWT_SECRET_KEY', 'jwt-secret-key-change-this'),
        algorithm='HS256'
    )
    return token


def verify_token(token):
    """验证JWT令牌"""
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('JWT_SECRET_KEY', 'jwt-secret-key-change-this'),
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None  # 令牌已过期
    except jwt.InvalidTokenError:
        return None  # 令牌无效


def token_required(f):
    """令牌验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'code': 401, 'message': '无效的授权令牌'}), 401
        
        if not token:
            return jsonify({'code': 401, 'message': '缺少授权令牌'}), 401
        
        payload = verify_token(token)
        if not payload:
            return jsonify({'code': 401, 'message': '令牌无效或已过期'}), 401
        
        return f(payload, *args, **kwargs)
    
    return decorated
