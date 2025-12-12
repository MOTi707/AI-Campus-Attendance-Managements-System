from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from models import db
from routes_auth import auth_bp
from routes_materials import materials_bp
from routes_grades import grades_bp
from routes_attendance import attendance_bp
from routes_interaction import interaction_bp
from routes_smart_attendance import smart_attendance_bp
from routes_seating import seating_bp
from routes_qa_assistant import qa_assistant_bp
import os

# 初始化Flask应用
app = Flask(__name__)

# 配置文件上传文件大小限制 (50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# 加载配置
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# 初始化数据库
db.init_app(app)

# 初始化CORS
CORS(app, origins=app.config.get('CORS_ORIGINS', ['*']))

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(grades_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(interaction_bp)
app.register_blueprint(smart_attendance_bp)
app.register_blueprint(seating_bp)
app.register_blueprint(qa_assistant_bp)


@app.route('/')
def hello_world():
    """欢迎页面"""
    return jsonify({
        'code': 200,
        'message': 'Welcome to Teaching Assistant API',
        'version': '1.0.0'
    })


@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """提供上传文件的访问"""
    from flask import send_from_directory
    return send_from_directory('uploads', filename)


@app.route('/face_database/<path:filename>')
def serve_face_image(filename):
    """提供人脸图片的访问"""
    from flask import send_from_directory
    return send_from_directory('face_database', filename)


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'code': 404,
        'message': '请求的资源不存在'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({
        'code': 500,
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
