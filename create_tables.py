#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import Error

def create_tables():
    try:
        # 连接数据库
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='teaching_assistant'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 创建互动任务表
            create_interaction_tasks = """
            CREATE TABLE IF NOT EXISTS interaction_tasks (
              id INT AUTO_INCREMENT PRIMARY KEY,
              teacher_id INT NOT NULL,
              task_name VARCHAR(200) NOT NULL,
              task_type ENUM('poll', 'question', 'barrage'),
              subject VARCHAR(100),
              description TEXT,
              status ENUM('draft', 'active', 'completed') DEFAULT 'draft',
              start_time TIMESTAMP NULL,
              end_time TIMESTAMP NULL,
              participation_count INT DEFAULT 0,
              notes TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              deleted_at TIMESTAMP NULL,
              FOREIGN KEY (teacher_id) REFERENCES users(id),
              INDEX idx_teacher_id (teacher_id),
              INDEX idx_task_type (task_type),
              INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_interaction_tasks)
            print("✓ Created table: interaction_tasks")
            
            # 创建投票选项表
            create_poll_options = """
            CREATE TABLE IF NOT EXISTS poll_options (
              id INT AUTO_INCREMENT PRIMARY KEY,
              task_id INT NOT NULL,
              option_text VARCHAR(500) NOT NULL,
              option_order INT DEFAULT 0,
              vote_count INT DEFAULT 0,
              percentage DECIMAL(5,2),
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (task_id) REFERENCES interaction_tasks(id) ON DELETE CASCADE,
              INDEX idx_task_id (task_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_poll_options)
            print("✓ Created table: poll_options")
            
            # 创建投票记录表
            create_poll_votes = """
            CREATE TABLE IF NOT EXISTS poll_votes (
              id INT AUTO_INCREMENT PRIMARY KEY,
              task_id INT NOT NULL,
              option_id INT NOT NULL,
              student_id INT NOT NULL,
              vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (task_id) REFERENCES interaction_tasks(id),
              FOREIGN KEY (option_id) REFERENCES poll_options(id),
              FOREIGN KEY (student_id) REFERENCES users(id),
              INDEX idx_task_id (task_id),
              UNIQUE KEY uk_task_student (task_id, student_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_poll_votes)
            print("✓ Created table: poll_votes")
            
            # 创建提问表
            create_questions = """
            CREATE TABLE IF NOT EXISTS questions (
              id INT AUTO_INCREMENT PRIMARY KEY,
              task_id INT NOT NULL,
              question_text TEXT NOT NULL,
              question_type VARCHAR(50),
              status ENUM('pending', 'answered', 'closed') DEFAULT 'pending',
              answer_count INT DEFAULT 0,
              correct_answer TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (task_id) REFERENCES interaction_tasks(id) ON DELETE CASCADE,
              INDEX idx_task_id (task_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_questions)
            print("✓ Created table: questions")
            
            # 创建提问回答表
            create_question_answers = """
            CREATE TABLE IF NOT EXISTS question_answers (
              id INT AUTO_INCREMENT PRIMARY KEY,
              question_id INT NOT NULL,
              student_id INT NOT NULL,
              answer_text TEXT NOT NULL,
              is_correct TINYINT,
              answer_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
              FOREIGN KEY (student_id) REFERENCES users(id),
              INDEX idx_question_id (question_id),
              UNIQUE KEY uk_question_student (question_id, student_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_question_answers)
            print("✓ Created table: question_answers")
            
            # 创建弹幕表
            create_barrage_messages = """
            CREATE TABLE IF NOT EXISTS barrage_messages (
              id INT AUTO_INCREMENT PRIMARY KEY,
              task_id INT NOT NULL,
              student_id INT NOT NULL,
              message_text TEXT NOT NULL,
              message_color VARCHAR(20) DEFAULT '#333333',
              is_pinned TINYINT DEFAULT 0,
              like_count INT DEFAULT 0,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              deleted_at TIMESTAMP NULL,
              FOREIGN KEY (task_id) REFERENCES interaction_tasks(id) ON DELETE CASCADE,
              FOREIGN KEY (student_id) REFERENCES users(id),
              INDEX idx_task_id (task_id),
              INDEX idx_created_at (created_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_barrage_messages)
            print("✓ Created table: barrage_messages")
            
            # 创建弹幕点赞表
            create_barrage_likes = """
            CREATE TABLE IF NOT EXISTS barrage_likes (
              id INT AUTO_INCREMENT PRIMARY KEY,
              message_id INT NOT NULL,
              student_id INT NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              FOREIGN KEY (message_id) REFERENCES barrage_messages(id) ON DELETE CASCADE,
              FOREIGN KEY (student_id) REFERENCES users(id),
              UNIQUE KEY uk_message_student (message_id, student_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            cursor.execute(create_barrage_likes)
            print("✓ Created table: barrage_likes")
            
            connection.commit()
            print("\n✅ All tables created successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_tables()
