"""
تكامل قاعدة البيانات مع واجهة الدردشة
يربط واجهة الدردشة مع قاعدة بيانات منصة التدريب
"""

import os
import requests
from datetime import datetime
from typing import Optional, Dict, List, Any
import hashlib

# إعدادات الاتصال بالمنصة
PLATFORM_API_URL = os.getenv('PLATFORM_API_URL', 'https://aitrainhub-ifghcdxx.manus.space')
PLATFORM_API_KEY = os.getenv('PLATFORM_API_KEY', '')

class DatabaseIntegration:
    """فئة تكامل قاعدة البيانات"""
    
    def __init__(self):
        self.api_url = PLATFORM_API_URL
        self.api_key = PLATFORM_API_KEY
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
        }
    
    def save_conversation(
        self, 
        user_id: int, 
        conversation_id: str, 
        user_message: str, 
        assistant_response: str,
        session_id: Optional[int] = None
    ) -> bool:
        """
        حفظ المحادثة في الذاكرة قصيرة المدى
        
        Args:
            user_id: معرف المستخدم
            conversation_id: معرف المحادثة
            user_message: رسالة المستخدم
            assistant_response: رد المساعد
            session_id: معرف الجلسة (اختياري)
        
        Returns:
            bool: نجاح العملية
        """
        try:
            # حساب عدد التوكنات التقريبي
            user_tokens = len(user_message) // 4
            assistant_tokens = len(assistant_response) // 4
            
            # حفظ رسالة المستخدم
            user_memory = {
                'userId': user_id,
                'sessionId': session_id,
                'conversationId': conversation_id,
                'role': 'user',
                'content': user_message,
                'tokenCount': user_tokens,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'source': 'chat_interface'
                }
            }
            
            # حفظ رد المساعد
            assistant_memory = {
                'userId': user_id,
                'sessionId': session_id,
                'conversationId': conversation_id,
                'role': 'assistant',
                'content': assistant_response,
                'tokenCount': assistant_tokens,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'source': 'chat_interface'
                }
            }
            
            # إرسال البيانات إلى API المنصة
            # في حالة عدم توفر API، يمكن حفظ البيانات محلياً
            if self.api_key:
                self._send_to_platform_api('memory/save', [user_memory, assistant_memory])
            
            return True
            
        except Exception as e:
            print(f"خطأ في حفظ المحادثة: {str(e)}")
            return False
    
    def get_conversation_context(
        self, 
        conversation_id: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        استرجاع سياق المحادثة من الذاكرة
        
        Args:
            conversation_id: معرف المحادثة
            limit: عدد الرسائل المطلوبة
        
        Returns:
            List[Dict]: قائمة الرسائل
        """
        try:
            if self.api_key:
                response = self._send_to_platform_api(
                    'memory/context', 
                    {'conversationId': conversation_id, 'limit': limit}
                )
                return response.get('messages', [])
            return []
            
        except Exception as e:
            print(f"خطأ في استرجاع السياق: {str(e)}")
            return []
    
    def save_training_data(
        self,
        user_id: int,
        data_name: str,
        content: str,
        data_type: str = 'conversation',
        session_id: Optional[int] = None
    ) -> Optional[int]:
        """
        حفظ بيانات التدريب
        
        Args:
            user_id: معرف المستخدم
            data_name: اسم البيانات
            content: المحتوى
            data_type: نوع البيانات
            session_id: معرف الجلسة
        
        Returns:
            Optional[int]: معرف البيانات المحفوظة
        """
        try:
            # حساب hash للمحتوى لتجنب التكرار
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            training_data = {
                'userId': user_id,
                'sessionId': session_id,
                'dataName': data_name,
                'dataType': data_type,
                'content': content,
                'contentHash': content_hash,
                'tokenCount': len(content) // 4,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'source': 'chat_interface'
                }
            }
            
            if self.api_key:
                response = self._send_to_platform_api('data/upload', training_data)
                return response.get('id')
            
            return None
            
        except Exception as e:
            print(f"خطأ في حفظ بيانات التدريب: {str(e)}")
            return None
    
    def log_activity(
        self,
        user_id: int,
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        details: Optional[Dict] = None,
        status: str = 'success'
    ) -> bool:
        """
        تسجيل النشاط
        
        Args:
            user_id: معرف المستخدم
            action: الإجراء
            resource_type: نوع المورد
            resource_id: معرف المورد
            details: تفاصيل إضافية
            status: حالة العملية
        
        Returns:
            bool: نجاح العملية
        """
        try:
            activity_log = {
                'userId': user_id,
                'action': action,
                'resourceType': resource_type,
                'resourceId': resource_id,
                'details': details or {},
                'status': status
            }
            
            if self.api_key:
                self._send_to_platform_api('activity/log', activity_log)
            
            return True
            
        except Exception as e:
            print(f"خطأ في تسجيل النشاط: {str(e)}")
            return False
    
    def extract_patterns(
        self,
        user_id: int,
        conversation_id: str
    ) -> List[Dict[str, Any]]:
        """
        استخراج الأنماط من المحادثة
        
        Args:
            user_id: معرف المستخدم
            conversation_id: معرف المحادثة
        
        Returns:
            List[Dict]: الأنماط المستخرجة
        """
        try:
            if self.api_key:
                response = self._send_to_platform_api(
                    'memory/patterns',
                    {'userId': user_id, 'conversationId': conversation_id}
                )
                return response.get('patterns', [])
            return []
            
        except Exception as e:
            print(f"خطأ في استخراج الأنماط: {str(e)}")
            return []
    
    def _send_to_platform_api(
        self, 
        endpoint: str, 
        data: Any
    ) -> Dict[str, Any]:
        """
        إرسال البيانات إلى API المنصة
        
        Args:
            endpoint: نقطة النهاية
            data: البيانات المرسلة
        
        Returns:
            Dict: الاستجابة
        """
        try:
            url = f"{self.api_url}/api/{endpoint}"
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"خطأ في API: {response.status_code} - {response.text}")
                return {}
                
        except Exception as e:
            print(f"خطأ في الاتصال بـ API: {str(e)}")
            return {}

# إنشاء نسخة عامة للاستخدام
db_integration = DatabaseIntegration()
