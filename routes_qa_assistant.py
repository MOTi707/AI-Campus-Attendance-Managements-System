"""
智能问答助手路由 - 使用 OpenAI SDK (SiliconFlow/DeepSeek)
"""

from flask import Blueprint, request, jsonify, Response
from models import db, ChatConversation, ChatMessage
from jwt_utils import token_required
from datetime import datetime
from openai import OpenAI
import logging
import json

# 配置日志
logger = logging.getLogger(__name__)

# 创建蓝图
qa_assistant_bp = Blueprint('qa_assistant', __name__, url_prefix='/api/qa-assistant')

# ==========================================
# API 配置 - 请在此处填写你的 API 配置
# ==========================================

# 选择使用的 API 提供商: 'siliconflow' 或 'deepseek'
API_PROVIDER = 'siliconflow'  # 请为此处选择 API 提供商

# SiliconFlow API 配置
SILICONFLOW_API_KEY = 'sk-rpuequlhparhcmoewdrfixlrjmeywjxwxskwebcbzkhjnxtd'  # 请填入你的 SiliconFlow API Key
SILICONFLOW_BASE_URL = 'https://api.siliconflow.cn/v1'
SILICONFLOW_MODEL = 'deepseek-ai/DeepSeek-V3'  # 使用的模型

# DeepSeek API 配置
DEEPSEEK_API_KEY = 'sk-rpuequlhparhcmoewdrfixlrjmeywjxwxskwebcbzkhjnxtd'  # 请填入你的 DeepSeek API Key
DEEPSEEK_BASE_URL = 'https://api.deepseek.com'
DEEPSEEK_MODEL = 'deepseek-chat'

# ==========================================
# 根据配置自动为你选择应用的 API
if API_PROVIDER.lower() == 'siliconflow':
    API_KEY = SILICONFLOW_API_KEY
    BASE_URL = SILICONFLOW_BASE_URL
    MODEL = SILICONFLOW_MODEL
else:
    API_KEY = DEEPSEEK_API_KEY
    BASE_URL = DEEPSEEK_BASE_URL
    MODEL = DEEPSEEK_MODEL

# 初始化 OpenAI 客户端
try:
    if API_KEY and API_KEY.strip():
        client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )
        logger.info(f'OpenAI 客户端初始化成功，使用 {API_PROVIDER.upper()} API')
    else:
        logger.warning('API Key 未配置')
        client = None
except Exception as e:
    logger.error(f'OpenAI 客户端初始化失败: {str(e)}')
    client = None

# 系统提示词
SYSTEM_PROMPT = """你是一位经验丰富的教学助手，专门帮助教师。

你的主要职责：
1. 回答关于课程安排、作业要求，学生成绩等常见问题
2. 提供教学建议和学生管理策略
3. 解答教学过程中的各类疑问

回答时请：
- 保持专业、友好的语气
- 提供具体、可操作的建议
- 简洁明了，重点突出



我是一名大学软件工程老师，教授Javaweb和python课程。

学生的情况如下“
张明远：作业完成率100%，均分92，代码规范优秀；期中88分（第3名），失分点在接口与抽象类区别、异常处理机制。系统评级：优秀。
李晓萌：作业完成率85%，均分75，第3次作业延期，泛型通配符理解模糊；期中68分（第22名），内存管理与多线程概念薄弱。系统评级：中等。
王浩宇：作业完成率60%，均分58，多次延期，代码格式混乱，第6次未交；期中45分（第38名），面向对象三大特征、异常语法失分严重。系统评级：预警。
”
"""


def call_ai_api_stream(messages):
    """
    调用 AI API (使用 OpenAI SDK) - 流式传输
    
    Args:
        messages: 消息列表
    
    Yields:
        逐行返回 API 响应，SSE 格式
    """
    if not API_KEY or API_KEY.strip() == '':
        logger.error(f'{API_PROVIDER.upper()} API Key 未填写')
        yield f"data: {{'error': '请先填写 {API_PROVIDER.upper()} API Key', 'done': True}}\n\n"
        return
    
    if not client:
        logger.error('OpenAI 客户端未初始化')
        yield f"data: {{'error': 'OpenAI 客户端初始化失败', 'done': True}}\n\n"
        return
    
    try:
        logger.info(f'开始调用 {API_PROVIDER.upper()} API, 模型: {MODEL}')
        
        # 使用 OpenAI SDK 调用 API，启用流式传输
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            stream=True  # 启用流式传输
        )
        
        logger.info('API 流式连接建立成功')
        
        # 逐步接收并处理响应
        for chunk in response:
            if not chunk.choices:
                continue
            
            # 处理内容增量
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                # 使用 json.dumps 确保字符串正常编码
                yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
        
        logger.info('API 响应完成')
        # 发送完成信号
        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f'API 调用失败: {error_msg}')
        
        # 提供详细的错误信息
        if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
            error_text = f'⏱️ 请求超时！请检查：\n1. 网络连接是否正常\n2. API 密钥是否有效\n3. 稍后重试'
        elif 'connection' in error_msg.lower() or 'refused' in error_msg.lower():
            error_text = f'❌ 网络连接失败！\n请检查：\n1. API 地址是否正确: {BASE_URL}\n2. 网络是否正常\n3. 是否需要代理'
        elif 'authentication' in error_msg.lower() or 'unauthorized' in error_msg.lower() or 'invalid' in error_msg.lower():
            error_text = f'🔑 API Key 无效或已过期，请检查配置'
        else:
            error_text = f'❌ 请求失败: {error_msg[:100]}'
        
        yield f"data: {json.dumps({'error': error_text, 'done': True})}\n\n"


@qa_assistant_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations(payload):
    """获取用户的所有对话"""
    try:
        teacher_id = payload.get('user_id')
        
        conversations = ChatConversation.query.filter_by(
            teacher_id=teacher_id,
            deleted_at=None
        ).order_by(ChatConversation.updated_at.desc()).all()
        
        return jsonify({
            'code': 200,
            'message': '获取对话列表成功',
            'data': [conv.to_dict() for conv in conversations]
        }), 200
        
    except Exception as e:
        logger.error(f'获取对话列表失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': f'获取对话列表失败: {str(e)}'
        }), 500


@qa_assistant_bp.route('/conversations', methods=['POST'])
@token_required
def create_conversation(payload):
    """创建新对话"""
    try:
        teacher_id = payload.get('user_id')
        data = request.get_json() or {}
        
        title = data.get('title', '新对话')
        
        conversation = ChatConversation(
            teacher_id=teacher_id,
            title=title
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        logger.info(f'创建对话成功: {conversation.id}')
        return jsonify({
            'code': 200,
            'message': '创建对话成功',
            'data': conversation.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'创建对话失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': f'创建对话失败: {str(e)}'
        }), 500


@qa_assistant_bp.route('/conversations/<int:conversation_id>', methods=['DELETE'])
@token_required
def delete_conversation(payload, conversation_id):
    """删除对话"""
    try:
        teacher_id = payload.get('user_id')
        
        conversation = ChatConversation.query.filter_by(
            id=conversation_id,
            teacher_id=teacher_id,
            deleted_at=None
        ).first()
        
        if not conversation:
            return jsonify({
                'code': 404,
                'message': '对话不存在'
            }), 404
        
        conversation.deleted_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f'删除对话成功: {conversation_id}')
        return jsonify({
            'code': 200,
            'message': '删除对话成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'删除对话失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': f'删除对话失败: {str(e)}'
        }), 500


@qa_assistant_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(payload, conversation_id):
    """获取对话中的所有消息"""
    try:
        teacher_id = payload.get('user_id')
        
        # 验证对话所有权
        conversation = ChatConversation.query.filter_by(
            id=conversation_id,
            teacher_id=teacher_id,
            deleted_at=None
        ).first()
        
        if not conversation:
            return jsonify({
                'code': 404,
                'message': '对话不存在'
            }), 404
        
        messages = ChatMessage.query.filter_by(
            conversation_id=conversation_id
        ).order_by(ChatMessage.created_at.asc()).all()
        
        return jsonify({
            'code': 200,
            'message': '获取消息成功',
            'data': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        logger.error(f'获取消息失败: {str(e)}')
        return jsonify({
            'code': 500,
            'message': f'获取消息失败: {str(e)}'
        }), 500


@qa_assistant_bp.route('/chat', methods=['POST'])
@token_required
def send_message(payload):
    """发送消息并获取AI回复"""
    conversation_id = None
    try:
        teacher_id = payload.get('user_id')
        data = request.get_json() or {}
        
        conversation_id = data.get('conversation_id')
        user_message = data.get('message', '').strip()
        
        logger.info(f'收到消息请求，对话ID: {conversation_id}, 消息: {user_message[:50]}')
        
        if not user_message:
            return jsonify({'code': 400, 'message': '消息内容不能为空'}), 400
        
        # 验证对话所有权
        conversation = ChatConversation.query.filter_by(
            id=conversation_id,
            teacher_id=teacher_id,
            deleted_at=None
        ).first()
        
        if not conversation:
            return jsonify({'code': 404, 'message': '对话不存在'}), 404
        
        # 保存用户消息
        user_chat_message = ChatMessage(
            conversation_id=conversation_id,
            role='user',
            content=user_message
        )
        db.session.add(user_chat_message)
        db.session.commit()
        logger.info(f'用户消息已保存')
        
        # 检查 API 配置
        if not API_KEY or not API_KEY.strip():
            logger.error('API Key 未配置')
            return jsonify({'code': 400, 'message': 'API Key 未配置'}), 400
        
        if not client:
            logger.error('OpenAI 客户端未初始化')
            return jsonify({'code': 500, 'message': 'OpenAI 客户端初始化失败'}), 500
        
        # 构建简单的 API 请求
        api_messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_message}
        ]
        
        logger.info(f'开始调用 {API_PROVIDER} API')
        
        # 调用 AI API
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2000,
                stream=False
            )
            
            ai_content = response.choices[0].message.content
            logger.info(f'✅ AI 回复成功，内容长度: {len(ai_content)}')
            
            # 保存 AI 消息
            ai_message = ChatMessage(
                conversation_id=conversation_id,
                role='assistant',
                content=ai_content
            )
            db.session.add(ai_message)
            
            # 更新对话
            conversation.updated_at = datetime.utcnow()
            if conversation.title == '新对话':
                conversation.title = user_message[:30]
            
            db.session.commit()
            logger.info('✅ AI 消息已保存到数据库')
            
            # 返回成功响应
            return jsonify({
                'code': 200,
                'message': '成功',
                'data': {'content': ai_content}
            }), 200
            
        except Exception as api_err:
            logger.error(f'❌ API 调用失败: {str(api_err)}')
            db.session.rollback()
            return jsonify({
                'code': 500,
                'message': f'API 调用失败: {str(api_err)}'
            }), 500
        
    except Exception as e:
        logger.error(f'❌ 处理消息失败: {str(e)}')
        if conversation_id:
            db.session.rollback()
        return jsonify({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }), 500


@qa_assistant_bp.route('/config', methods=['GET'])
@token_required
def get_config(payload):
    """获取API配置状态"""
    return jsonify({
        'code': 200,
        'data': {
            'api_key_configured': bool(API_KEY and API_KEY.strip()),
            'provider': API_PROVIDER,
            'model': MODEL
        }
    }), 200
