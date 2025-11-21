"""
تكامل خدمات MCP (Notion, Gmail, Google Calendar)
يوفر واجهات للتفاعل مع الخدمات الخارجية
"""

import os
import subprocess
import json
from typing import Optional, Dict, List, Any
from datetime import datetime

class MCPServicesIntegration:
    """فئة تكامل خدمات MCP"""
    
    def __init__(self):
        self.mcp_cli = 'manus-mcp-cli'
    
    def _execute_mcp_command(
        self, 
        tool_name: str, 
        server: str, 
        input_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        تنفيذ أمر MCP
        
        Args:
            tool_name: اسم الأداة
            server: اسم الخادم
            input_data: بيانات الإدخال
        
        Returns:
            Optional[Dict]: النتيجة
        """
        try:
            input_json = json.dumps(input_data)
            
            cmd = [
                self.mcp_cli,
                'tool',
                'call',
                tool_name,
                '--server',
                server,
                '--input',
                input_json
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"خطأ في تنفيذ MCP: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"خطأ في تنفيذ أمر MCP: {str(e)}")
            return None
    
    # ═══════════════════════════════════════════════════════════════════════
    # تكامل Notion
    # ═══════════════════════════════════════════════════════════════════════
    
    def notion_create_page(
        self,
        parent_id: str,
        title: str,
        content: str,
        properties: Optional[Dict] = None
    ) -> Optional[str]:
        """
        إنشاء صفحة في Notion
        
        Args:
            parent_id: معرف الصفحة الأم أو قاعدة البيانات
            title: عنوان الصفحة
            content: محتوى الصفحة
            properties: خصائص إضافية
        
        Returns:
            Optional[str]: معرف الصفحة المنشأة
        """
        try:
            input_data = {
                'parent_page_id': parent_id,
                'title': title,
                'content_blocks': [
                    {
                        'type': 'paragraph',
                        'text': content
                    }
                ]
            }
            
            if properties:
                input_data['properties'] = properties
            
            result = self._execute_mcp_command(
                'create_page',
                'notion',
                input_data
            )
            
            if result:
                return result.get('page_id')
            
            return None
            
        except Exception as e:
            print(f"خطأ في إنشاء صفحة Notion: {str(e)}")
            return None
    
    def notion_save_conversation(
        self,
        parent_id: str,
        conversation_id: str,
        messages: List[Dict[str, Any]]
    ) -> Optional[str]:
        """
        حفظ محادثة في Notion
        
        Args:
            parent_id: معرف الصفحة الأم
            conversation_id: معرف المحادثة
            messages: قائمة الرسائل
        
        Returns:
            Optional[str]: معرف الصفحة
        """
        try:
            title = f"محادثة {conversation_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            content = "## المحادثة\n\n"
            for msg in messages:
                role = msg.get('role', 'user')
                text = msg.get('content', '')
                content += f"**{role.upper()}**: {text}\n\n"
            
            return self.notion_create_page(
                parent_id=parent_id,
                title=title,
                content=content
            )
            
        except Exception as e:
            print(f"خطأ في حفظ المحادثة في Notion: {str(e)}")
            return None
    
    def notion_search_pages(
        self,
        query: str,
        filter_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        البحث في صفحات Notion
        
        Args:
            query: نص البحث
            filter_type: نوع التصفية
        
        Returns:
            List[Dict]: نتائج البحث
        """
        try:
            input_data = {
                'query': query
            }
            
            if filter_type:
                input_data['filter'] = {'property': 'object', 'value': filter_type}
            
            result = self._execute_mcp_command(
                'search',
                'notion',
                input_data
            )
            
            if result:
                return result.get('results', [])
            
            return []
            
        except Exception as e:
            print(f"خطأ في البحث في Notion: {str(e)}")
            return []
    
    # ═══════════════════════════════════════════════════════════════════════
    # تكامل Gmail
    # ═══════════════════════════════════════════════════════════════════════
    
    def gmail_send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """
        إرسال بريد إلكتروني عبر Gmail
        
        Args:
            to: المستلم
            subject: الموضوع
            body: المحتوى
            cc: نسخة كربونية
            bcc: نسخة كربونية مخفية
        
        Returns:
            bool: نجاح العملية
        """
        try:
            input_data = {
                'to': to,
                'subject': subject,
                'body': body
            }
            
            if cc:
                input_data['cc'] = cc
            if bcc:
                input_data['bcc'] = bcc
            
            result = self._execute_mcp_command(
                'send_email',
                'gmail',
                input_data
            )
            
            return result is not None
            
        except Exception as e:
            print(f"خطأ في إرسال البريد الإلكتروني: {str(e)}")
            return False
    
    def gmail_send_conversation_summary(
        self,
        to: str,
        conversation_id: str,
        messages: List[Dict[str, Any]]
    ) -> bool:
        """
        إرسال ملخص المحادثة عبر البريد الإلكتروني
        
        Args:
            to: المستلم
            conversation_id: معرف المحادثة
            messages: قائمة الرسائل
        
        Returns:
            bool: نجاح العملية
        """
        try:
            subject = f"ملخص المحادثة {conversation_id}"
            
            body = f"ملخص المحادثة {conversation_id}\n"
            body += f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            body += "=" * 50 + "\n\n"
            
            for msg in messages:
                role = msg.get('role', 'user')
                text = msg.get('content', '')
                timestamp = msg.get('createdAt', '')
                
                body += f"{role.upper()} ({timestamp}):\n{text}\n\n"
                body += "-" * 50 + "\n\n"
            
            return self.gmail_send_email(
                to=to,
                subject=subject,
                body=body
            )
            
        except Exception as e:
            print(f"خطأ في إرسال ملخص المحادثة: {str(e)}")
            return False
    
    def gmail_search_emails(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        البحث في رسائل البريد الإلكتروني
        
        Args:
            query: نص البحث
            max_results: عدد النتائج الأقصى
        
        Returns:
            List[Dict]: نتائج البحث
        """
        try:
            input_data = {
                'query': query,
                'max_results': max_results
            }
            
            result = self._execute_mcp_command(
                'search_emails',
                'gmail',
                input_data
            )
            
            if result:
                return result.get('messages', [])
            
            return []
            
        except Exception as e:
            print(f"خطأ في البحث في Gmail: {str(e)}")
            return []
    
    # ═══════════════════════════════════════════════════════════════════════
    # تكامل Google Calendar
    # ═══════════════════════════════════════════════════════════════════════
    
    def calendar_create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        إنشاء حدث في Google Calendar
        
        Args:
            summary: عنوان الحدث
            start_time: وقت البداية (ISO format)
            end_time: وقت النهاية (ISO format)
            description: الوصف
            location: الموقع
            attendees: الحضور
        
        Returns:
            Optional[str]: معرف الحدث
        """
        try:
            input_data = {
                'summary': summary,
                'start': {'dateTime': start_time},
                'end': {'dateTime': end_time}
            }
            
            if description:
                input_data['description'] = description
            if location:
                input_data['location'] = location
            if attendees:
                input_data['attendees'] = [{'email': email} for email in attendees]
            
            result = self._execute_mcp_command(
                'create_event',
                'google-calendar',
                input_data
            )
            
            if result:
                return result.get('event_id')
            
            return None
            
        except Exception as e:
            print(f"خطأ في إنشاء حدث التقويم: {str(e)}")
            return None
    
    def calendar_list_events(
        self,
        time_min: Optional[str] = None,
        time_max: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        عرض الأحداث من Google Calendar
        
        Args:
            time_min: الوقت الأدنى (ISO format)
            time_max: الوقت الأقصى (ISO format)
            max_results: عدد النتائج الأقصى
        
        Returns:
            List[Dict]: قائمة الأحداث
        """
        try:
            input_data = {
                'max_results': max_results
            }
            
            if time_min:
                input_data['time_min'] = time_min
            if time_max:
                input_data['time_max'] = time_max
            
            result = self._execute_mcp_command(
                'list_events',
                'google-calendar',
                input_data
            )
            
            if result:
                return result.get('events', [])
            
            return []
            
        except Exception as e:
            print(f"خطأ في عرض أحداث التقويم: {str(e)}")
            return []
    
    def calendar_create_reminder(
        self,
        summary: str,
        reminder_time: str,
        description: Optional[str] = None
    ) -> Optional[str]:
        """
        إنشاء تذكير في Google Calendar
        
        Args:
            summary: عنوان التذكير
            reminder_time: وقت التذكير (ISO format)
            description: الوصف
        
        Returns:
            Optional[str]: معرف الحدث
        """
        try:
            # التذكير هو حدث مدته ساعة واحدة
            from datetime import datetime, timedelta
            
            start_dt = datetime.fromisoformat(reminder_time.replace('Z', '+00:00'))
            end_dt = start_dt + timedelta(hours=1)
            
            return self.calendar_create_event(
                summary=f"🔔 {summary}",
                start_time=start_dt.isoformat(),
                end_time=end_dt.isoformat(),
                description=description
            )
            
        except Exception as e:
            print(f"خطأ في إنشاء التذكير: {str(e)}")
            return None

# إنشاء نسخة عامة للاستخدام
mcp_services = MCPServicesIntegration()
