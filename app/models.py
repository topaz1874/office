from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Document(db.Model):
    """文档模型"""
    id = db.Column(db.Integer, primary_key=True)
    register_time = db.Column(db.DateTime, nullable=True)
    doc_number = db.Column(db.String(100), nullable=False)
    source_unit = db.Column(db.String(200), nullable=True)
    original_number = db.Column(db.String(100), nullable=True)
    security_level = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(500), nullable=False)
    transfer_dept = db.Column(db.String(200), nullable=True)
    business_type = db.Column(db.String(100), nullable=True)
    tracking = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<Document {self.doc_number}: {self.title}>'

class Announcement(db.Model):
    """公告模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.now)
    author = db.Column(db.String(100), nullable=True)
    is_important = db.Column(db.Boolean, default=False)  # 重要公告标记
    
    # 添加附件字段
    attachment_filename = db.Column(db.String(255), nullable=True)  # 原始文件名
    attachment_path = db.Column(db.String(255), nullable=True)  # 存储路径
    attachment_type = db.Column(db.String(50), nullable=True)  # 文件类型
    
    def __repr__(self):
        return f'<Announcement {self.id}: {self.title}>' 