from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Chat(db.Model):
    """Chat session model"""
    __tablename__ = 'chats'
    
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.String(36), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        last_message = None
        if self.messages:
            last_message = self.messages[-1].content[:100] + "..." if len(self.messages[-1].content) > 100 else self.messages[-1].content
        
        return {
            'id': self.id,
            'title': self.title or 'محادثة جديدة',
            'lastMessage': last_message,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'messageCount': len(self.messages),
            'isActive': self.is_active
        }

class Message(db.Model):
    """Message model"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True)
    chat_id = db.Column(db.String(36), db.ForeignKey('chats.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parts_json = db.Column(db.Text, nullable=True)
    metadata_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        parts = []
        if self.parts_json:
            try:
                parts = json.loads(self.parts_json)
            except:
                parts = [{'type': 'text', 'text': self.content}]
        else:
            parts = [{'type': 'text', 'text': self.content}]
        
        metadata = {}
        if self.metadata_json:
            try:
                metadata = json.loads(self.metadata_json)
            except:
                metadata = {}
        
        return {
            'id': self.id,
            'role': self.role,
            'parts': parts,
            'content': self.content,
            'createdAt': self.created_at.isoformat(),
            'metadata': metadata
        }
