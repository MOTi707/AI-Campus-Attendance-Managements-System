"""
创建智能问答助手相关数据表
"""

from app import app
from models import db, ChatConversation, ChatMessage

def create_qa_tables():
    """创建问答助手表"""
    with app.app_context():
        # 创建表
        db.create_all()
        print("✅ 智能问答助手数据表创建成功！")
        print("   - chat_conversations (对话表)")
        print("   - chat_messages (消息表)")

if __name__ == '__main__':
    create_qa_tables()
