from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, comment='用户ID')
    identity = db.Column(db.String(50), nullable=False, comment='用户身份: student/teacher')
    username = db.Column(db.String(100), nullable=False, unique=True, comment='用户名/学号/工号')
    fullname = db.Column(db.String(100), comment='姓名')
    password = db.Column(db.String(255), nullable=False, comment='密码（加密）')
    subject = db.Column(db.String(100), comment='授课科目')
    token = db.Column(db.String(500), comment='JWT令牌')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def set_password(self, password):
        """设置密码"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'identity': self.identity,
            'username': self.username,
            'fullname': self.fullname,
            'subject': self.subject,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Document(db.Model):
    """文档资料模型"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True, comment='文档ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='上传教师ID')
    filename = db.Column(db.String(255), nullable=False, comment='文件名')
    original_name = db.Column(db.String(255), comment='原始文件名')
    file_path = db.Column(db.String(500), nullable=False, comment='文件保存路径')
    file_size = db.Column(db.Integer, comment='文件大小(字节)')
    file_type = db.Column(db.String(50), comment='文件类型: pdf/doc/docx/pptx/txt等')
    title = db.Column(db.String(255), comment='文档标题')
    description = db.Column(db.Text, comment='文档描述')
    keywords = db.Column(db.Text, comment='提取的关键词(JSON格式)')
    category = db.Column(db.String(100), comment='分类: 数学/英语/物理等')
    sub_category = db.Column(db.String(100), comment='子分类')
    confidence_score = db.Column(db.Float, default=0.0, comment='分类置信度(0-1)')
    tags = db.Column(db.Text, comment='标签(JSON格式)')
    is_auto_classified = db.Column(db.Boolean, default=False, comment='是否自动分类')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='上传时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def set_keywords(self, keywords_list):
        """设置关键词"""
        self.keywords = json.dumps(keywords_list, ensure_ascii=False)
    
    def get_keywords(self):
        """获取关键词"""
        if self.keywords:
            return json.loads(self.keywords)
        return []
    
    def set_tags(self, tags_list):
        """设置标签"""
        self.tags = json.dumps(tags_list, ensure_ascii=False)
    
    def get_tags(self):
        """获取标签"""
        if self.tags:
            return json.loads(self.tags)
        return []
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'filename': self.filename,
            'original_name': self.original_name,
            'title': self.title,
            'description': self.description,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'keywords': self.get_keywords(),
            'category': self.category,
            'sub_category': self.sub_category,
            'confidence_score': self.confidence_score,
            'tags': self.get_tags(),
            'is_auto_classified': self.is_auto_classified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<Document {self.filename}>'


class TeacherStudent(db.Model):
    """教师学生关联模型"""
    __tablename__ = 'teacher_students'
    
    id = db.Column(db.Integer, primary_key=True, comment='关联ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def __repr__(self):
        return f'<TeacherStudent teacher_id={self.teacher_id} student_id={self.student_id}>'


class StudentScore(db.Model):
    """学生成绩模型"""
    __tablename__ = 'student_scores'
    
    id = db.Column(db.Integer, primary_key=True, comment='成绩ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    subject = db.Column(db.String(100), nullable=False, comment='科目')
    exam_number = db.Column(db.Integer, default=1, comment='第几次考试')
    score = db.Column(db.Float, nullable=False, comment='成绩')
    full_score = db.Column(db.Float, default=100, comment='满分')
    exam_date = db.Column(db.Date, comment='考试日期')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'student_id': self.student_id,
            'teacher_id': self.teacher_id,
            'subject': self.subject,
            'exam_number': self.exam_number,
            'score': self.score,
            'full_score': self.full_score,
            'exam_date': self.exam_date.isoformat() if self.exam_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<StudentScore student_id={self.student_id} subject={self.subject}>'


# ==================== 课堂考勤模型 ====================

class AttendanceTask(db.Model):
    """考勤任务模型"""
    __tablename__ = 'attendance_tasks'
    
    id = db.Column(db.Integer, primary_key=True, comment='任务ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    task_name = db.Column(db.String(200), nullable=False, comment='任务名称')
    class_name = db.Column(db.String(100), comment='班级名称')
    subject = db.Column(db.String(100), comment='课程名称')
    task_code = db.Column(db.String(50), unique=True, comment='任务唯一码')
    status = db.Column(db.String(20), default='pending', comment='任务状态')
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
    expected_count = db.Column(db.Integer, default=0, comment='预期出勤人数')
    actual_count = db.Column(db.Integer, default=0, comment='实际出勤人数')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def __repr__(self):
        return f'<AttendanceTask id={self.id} task_name={self.task_name}>'


class AttendanceRecord(db.Model):
    """学生考勤记录模型"""
    __tablename__ = 'attendance_records'
    
    id = db.Column(db.Integer, primary_key=True, comment='记录ID')
    task_id = db.Column(db.Integer, db.ForeignKey('attendance_tasks.id'), nullable=False, comment='任务ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    check_in_time = db.Column(db.DateTime, comment='签到时间')
    check_in_method = db.Column(db.String(20), default='qr_code', comment='签到方式')
    check_in_location = db.Column(db.String(200), comment='签到位置')
    is_present = db.Column(db.Integer, default=1, comment='是否出勤')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def __repr__(self):
        return f'<AttendanceRecord task_id={self.task_id} student_id={self.student_id}>'


# ==================== 课堂互动模型 ====================

class InteractionTask(db.Model):
    """互动任务模型"""
    __tablename__ = 'interaction_tasks'
    
    id = db.Column(db.Integer, primary_key=True, comment='任务ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    task_name = db.Column(db.String(200), nullable=False, comment='任务名称')
    task_type = db.Column(db.String(20), comment='任务类型')
    subject = db.Column(db.String(100), comment='课程名称')
    description = db.Column(db.Text, comment='任务描述')
    status = db.Column(db.String(20), default='draft', comment='任务状态')
    start_time = db.Column(db.DateTime, comment='开始时间')
    end_time = db.Column(db.DateTime, comment='结束时间')
    participation_count = db.Column(db.Integer, default=0, comment='参与人数')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def __repr__(self):
        return f'<InteractionTask id={self.id} task_type={self.task_type}>'


class PollOption(db.Model):
    """投票选项模型"""
    __tablename__ = 'poll_options'
    
    id = db.Column(db.Integer, primary_key=True, comment='选项ID')
    task_id = db.Column(db.Integer, db.ForeignKey('interaction_tasks.id'), nullable=False, comment='任务ID')
    option_text = db.Column(db.String(500), nullable=False, comment='选项文本')
    option_order = db.Column(db.Integer, default=0, comment='选项顺序')
    vote_count = db.Column(db.Integer, default=0, comment='投票数')
    percentage = db.Column(db.Float, comment='百分比')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def __repr__(self):
        return f'<PollOption id={self.id} option_text={self.option_text}>'


class PollVote(db.Model):
    """投票记录模型"""
    __tablename__ = 'poll_votes'
    
    id = db.Column(db.Integer, primary_key=True, comment='投票ID')
    task_id = db.Column(db.Integer, db.ForeignKey('interaction_tasks.id'), nullable=False, comment='任务ID')
    option_id = db.Column(db.Integer, db.ForeignKey('poll_options.id'), nullable=False, comment='选项ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    vote_time = db.Column(db.DateTime, default=datetime.utcnow, comment='投票时间')
    
    def __repr__(self):
        return f'<PollVote student_id={self.student_id} option_id={self.option_id}>'


class Question(db.Model):
    """提问模型"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True, comment='问题ID')
    task_id = db.Column(db.Integer, db.ForeignKey('interaction_tasks.id'), nullable=False, comment='任务ID')
    question_text = db.Column(db.Text, nullable=False, comment='问题内容')
    question_type = db.Column(db.String(50), comment='问题类型')
    status = db.Column(db.String(20), default='pending', comment='问题状态')
    answer_count = db.Column(db.Integer, default=0, comment='回答数')
    correct_answer = db.Column(db.Text, comment='标准答案')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def __repr__(self):
        return f'<Question id={self.id} status={self.status}>'


class QuestionAnswer(db.Model):
    """问题回答模型"""
    __tablename__ = 'question_answers'
    
    id = db.Column(db.Integer, primary_key=True, comment='回答ID')
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, comment='问题ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    answer_text = db.Column(db.Text, nullable=False, comment='回答内容')
    is_correct = db.Column(db.Integer, comment='是否正确')
    answer_time = db.Column(db.DateTime, default=datetime.utcnow, comment='回答时间')
    
    def __repr__(self):
        return f'<QuestionAnswer question_id={self.question_id} student_id={self.student_id}>'


class BarrageMessage(db.Model):
    """弹幕消息模型"""
    __tablename__ = 'barrage_messages'
    
    id = db.Column(db.Integer, primary_key=True, comment='消息ID')
    task_id = db.Column(db.Integer, db.ForeignKey('interaction_tasks.id'), nullable=False, comment='任务ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    message_text = db.Column(db.Text, nullable=False, comment='消息内容')
    message_color = db.Column(db.String(20), default='#333333', comment='消息颜色')
    is_pinned = db.Column(db.Integer, default=0, comment='是否置顶')
    like_count = db.Column(db.Integer, default=0, comment='点赞数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def __repr__(self):
        return f'<BarrageMessage id={self.id} student_id={self.student_id}>'


class BarrageLike(db.Model):
    """弹幕点赞模型"""
    __tablename__ = 'barrage_likes'
    
    id = db.Column(db.Integer, primary_key=True, comment='点赞ID')
    message_id = db.Column(db.Integer, db.ForeignKey('barrage_messages.id'), nullable=False, comment='消息ID')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='学生ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def __repr__(self):
        return f'<BarrageLike message_id={self.message_id} student_id={self.student_id}>'


# ==================== 智能问答助手 ====================

class ChatConversation(db.Model):
    """聊天会话模型"""
    __tablename__ = 'chat_conversations'
    
    id = db.Column(db.Integer, primary_key=True, comment='会ID')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='教师ID')
    title = db.Column(db.String(255), default='新对话', comment='会话标题')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    deleted_at = db.Column(db.DateTime, comment='删除时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f'<ChatConversation id={self.id} title={self.title}>'


class ChatMessage(db.Model):
    """聊天消息模型"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True, comment='消息ID')
    conversation_id = db.Column(db.Integer, db.ForeignKey('chat_conversations.id'), nullable=False, comment='会话ID')
    role = db.Column(db.String(20), nullable=False, comment='角色: user/assistant')
    content = db.Column(db.Text, nullable=False, comment='消息内容')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self):
        return f'<ChatMessage id={self.id} role={self.role}>'
