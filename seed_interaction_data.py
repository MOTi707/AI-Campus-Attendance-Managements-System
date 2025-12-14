#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
为课堂互动数据库插入测试数据
"""

from app import app
from models import db, InteractionTask, Question, BarrageMessage, User
from datetime import datetime, timedelta
import random

def seed_data():
    """插入测试数据"""
    with app.app_context():
        # 获取教师ID（假设ID=18是教师）
        teacher_id = 18
        
        # 获取学生列表（ID 1-10）
        students = User.query.filter(User.id.between(1, 10)).all()
        if not students:
            print("❌ 找不到学生数据，请先创建学生用户")
            return
        
        student_ids = [s.id for s in students]
        
        print("🚀 开始插入测试数据...\n")
        
        # ==================== 创建提问任务 ====================
        print("📝 创建提问任务...")
        question_task = InteractionTask(
            teacher_id=teacher_id,
            task_name='Python基础知识问卷',
            task_type='question',
            subject='Python编程',
            description='考察学生对Python基础知识的理解',
            status='active',
            start_time=datetime.now(),
            notes='这是一个测试任务'
        )
        db.session.add(question_task)
        db.session.flush()  # 获取task_id
        
        # 添加提问
        questions_data = [
            {
                'text': '什么是Python中的列表(list)？请说出它的三个主要特性。',
                'correct_answer': '有序，可变，可包含任何类型的对象'
            },
            {
                'text': '如何在Python中创建一个字典？请给出一个例子。',
                'correct_answer': 'd = {"key": "value"}'
            },
            {
                'text': '解释Python中的lambda函数是什么，并给出一个使用例子。',
                'correct_answer': 'lambda是匿名函数，例如: square = lambda x: x**2'
            },
            {
                'text': '什么是Python中的装饰器(decorator)？',
                'correct_answer': '装饰器是修改或增强函数功能的函数'
            },
            {
                'text': '如何在Python中处理异常？',
                'correct_answer': '使用try-except-else-finally语句块'
            }
        ]
        
        questions_list = []
        for q_data in questions_data:
            question = Question(
                task_id=question_task.id,
                question_text=q_data['text'],
                question_type='essay',
                status='pending',
                correct_answer=q_data['correct_answer']
            )
            questions_list.append(question)
            db.session.add(question)
        
        db.session.flush()
        print(f"✅ 创建了提问任务 (ID: {question_task.id})，包含 {len(questions_list)} 道题目\n")
        
        # ==================== 创建弹幕任务 ====================
        print("💬 创建弹幕讨论任务...")
        barrage_task = InteractionTask(
            teacher_id=teacher_id,
            task_name='课堂知识讨论',
            task_type='barrage',
            subject='数据结构与算法',
            description='关于二叉树的实时课堂讨论',
            status='active',
            start_time=datetime.now() - timedelta(minutes=10),
            notes='这是一个弹幕讨论任务'
        )
        db.session.add(barrage_task)
        db.session.flush()
        
        # 添加弹幕消息
        barrage_messages_data = [
            ('老师讲得很清楚呢！', '#FF6B6B'),
            ('二叉树的中序遍历怎么实现？', '#4ECDC4'),
            ('我觉得递归的方式比较好理解', '#FFE66D'),
            ('这个知识点在面试中经常考', '#95DE64'),
            ('我完全同意，刚才看题目就懂了', '#FF85C0'),
            ('能再讲一遍中序遍历吗？', '#40C057'),
            ('总结得非常好，获益匪浅', '#FF6B6B'),
            ('原来二叉树还有这么多应用场景', '#4ECDC4'),
            ('下次课能讲平衡二叉树吗？', '#FFE66D'),
            ('我把笔记都整理好了', '#95DE64'),
            ('这是今年听过最清楚的讲解了', '#FF85C0'),
            ('大家有什么疑问吗？', '#40C057'),
            ('我有个问题，红黑树和AVL树的区别是什么？', '#FF6B6B'),
            ('红黑树的自平衡比较复杂，但性能更好', '#4ECDC4'),
            ('今天学到了很多东西，感谢老师！', '#FFE66D'),
        ]
        
        barrage_messages_list = []
        for idx, (msg_text, color) in enumerate(barrage_messages_data):
            # 循环使用学生ID
            student_id = student_ids[idx % len(student_ids)]
            
            # 随机生成创建时间（在最近10分钟内）
            created_time = datetime.now() - timedelta(minutes=random.randint(0, 10))
            
            barrage_msg = BarrageMessage(
                task_id=barrage_task.id,
                student_id=student_id,
                message_text=msg_text,
                message_color=color,
                is_pinned=1 if idx < 2 else 0,  # 前两条消息置顶
                like_count=random.randint(0, 8),
                created_at=created_time
            )
            barrage_messages_list.append(barrage_msg)
            db.session.add(barrage_msg)
        
        db.session.flush()
        print(f"✅ 创建了弹幕任务 (ID: {barrage_task.id})，包含 {len(barrage_messages_list)} 条消息\n")
        
        # ==================== 统计信息 ====================
        print("=" * 60)
        print("📊 数据插入统计")
        print("=" * 60)
        print(f"✅ 提问任务:")
        print(f"   - 任务ID: {question_task.id}")
        print(f"   - 题目数: {len(questions_list)}")
        print(f"\n✅ 弹幕任务:")
        print(f"   - 任务ID: {barrage_task.id}")
        print(f"   - 消息数: {len(barrage_messages_list)}")
        print(f"   - 参与学生数: {len(set(student_ids[:len(barrage_messages_list)]))}")
        print("=" * 60)
        
        # 提交所有改变
        db.session.commit()
        print("\n🎉 所有数据已成功插入数据库！")
        print("\n💡 提示:")
        print(f"   - 提问任务ID: {question_task.id} (使用此ID进行提问相关操作)")
        print(f"   - 弹幕任务ID: {barrage_task.id} (使用此ID进行弹幕相关操作)")
        print(f"   - 教师ID: {teacher_id}")

if __name__ == '__main__':
    try:
        seed_data()
    except Exception as e:
        print(f"❌ 插入数据出错: {str(e)}")
        import traceback
        traceback.print_exc()
