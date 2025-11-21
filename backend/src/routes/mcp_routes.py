from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
import os

# إضافة مسار الوحدات
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from integrations.mcp_services import mcp_services

mcp_bp = Blueprint('mcp', __name__)

# ═══════════════════════════════════════════════════════════════════════
# Notion Routes
# ═══════════════════════════════════════════════════════════════════════

@mcp_bp.route('/notion/create-page', methods=['POST'])
@cross_origin(origins='*')
def notion_create_page():
    """إنشاء صفحة في Notion"""
    try:
        data = request.get_json()
        
        parent_id = data.get('parentId')
        title = data.get('title')
        content = data.get('content')
        properties = data.get('properties')
        
        if not parent_id or not title or not content:
            return jsonify({'error': 'Missing required fields'}), 400
        
        page_id = mcp_services.notion_create_page(
            parent_id=parent_id,
            title=title,
            content=content,
            properties=properties
        )
        
        if page_id:
            return jsonify({
                'success': True,
                'pageId': page_id,
                'message': 'تم إنشاء الصفحة بنجاح'
            })
        else:
            return jsonify({'error': 'فشل في إنشاء الصفحة'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/notion/save-conversation', methods=['POST'])
@cross_origin(origins='*')
def notion_save_conversation():
    """حفظ محادثة في Notion"""
    try:
        data = request.get_json()
        
        parent_id = data.get('parentId')
        conversation_id = data.get('conversationId')
        messages = data.get('messages', [])
        
        if not parent_id or not conversation_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        page_id = mcp_services.notion_save_conversation(
            parent_id=parent_id,
            conversation_id=conversation_id,
            messages=messages
        )
        
        if page_id:
            return jsonify({
                'success': True,
                'pageId': page_id,
                'message': 'تم حفظ المحادثة في Notion بنجاح'
            })
        else:
            return jsonify({'error': 'فشل في حفظ المحادثة'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/notion/search', methods=['GET'])
@cross_origin(origins='*')
def notion_search():
    """البحث في Notion"""
    try:
        query = request.args.get('query', '')
        filter_type = request.args.get('type')
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        results = mcp_services.notion_search_pages(
            query=query,
            filter_type=filter_type
        )
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ═══════════════════════════════════════════════════════════════════════
# Gmail Routes
# ═══════════════════════════════════════════════════════════════════════

@mcp_bp.route('/gmail/send', methods=['POST'])
@cross_origin(origins='*')
def gmail_send():
    """إرسال بريد إلكتروني"""
    try:
        data = request.get_json()
        
        to = data.get('to')
        subject = data.get('subject')
        body = data.get('body')
        cc = data.get('cc')
        bcc = data.get('bcc')
        
        if not to or not subject or not body:
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = mcp_services.gmail_send_email(
            to=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم إرسال البريد الإلكتروني بنجاح'
            })
        else:
            return jsonify({'error': 'فشل في إرسال البريد الإلكتروني'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/gmail/send-conversation', methods=['POST'])
@cross_origin(origins='*')
def gmail_send_conversation():
    """إرسال ملخص المحادثة عبر البريد"""
    try:
        data = request.get_json()
        
        to = data.get('to')
        conversation_id = data.get('conversationId')
        messages = data.get('messages', [])
        
        if not to or not conversation_id:
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = mcp_services.gmail_send_conversation_summary(
            to=to,
            conversation_id=conversation_id,
            messages=messages
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم إرسال ملخص المحادثة بنجاح'
            })
        else:
            return jsonify({'error': 'فشل في إرسال ملخص المحادثة'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/gmail/search', methods=['GET'])
@cross_origin(origins='*')
def gmail_search():
    """البحث في Gmail"""
    try:
        query = request.args.get('query', '')
        max_results = request.args.get('max', 10, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        results = mcp_services.gmail_search_emails(
            query=query,
            max_results=max_results
        )
        
        return jsonify({
            'success': True,
            'messages': results,
            'count': len(results)
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ═══════════════════════════════════════════════════════════════════════
# Google Calendar Routes
# ═══════════════════════════════════════════════════════════════════════

@mcp_bp.route('/calendar/create-event', methods=['POST'])
@cross_origin(origins='*')
def calendar_create_event():
    """إنشاء حدث في التقويم"""
    try:
        data = request.get_json()
        
        summary = data.get('summary')
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        description = data.get('description')
        location = data.get('location')
        attendees = data.get('attendees')
        
        if not summary or not start_time or not end_time:
            return jsonify({'error': 'Missing required fields'}), 400
        
        event_id = mcp_services.calendar_create_event(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location,
            attendees=attendees
        )
        
        if event_id:
            return jsonify({
                'success': True,
                'eventId': event_id,
                'message': 'تم إنشاء الحدث بنجاح'
            })
        else:
            return jsonify({'error': 'فشل في إنشاء الحدث'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/calendar/create-reminder', methods=['POST'])
@cross_origin(origins='*')
def calendar_create_reminder():
    """إنشاء تذكير في التقويم"""
    try:
        data = request.get_json()
        
        summary = data.get('summary')
        reminder_time = data.get('reminderTime')
        description = data.get('description')
        
        if not summary or not reminder_time:
            return jsonify({'error': 'Missing required fields'}), 400
        
        event_id = mcp_services.calendar_create_reminder(
            summary=summary,
            reminder_time=reminder_time,
            description=description
        )
        
        if event_id:
            return jsonify({
                'success': True,
                'eventId': event_id,
                'message': 'تم إنشاء التذكير بنجاح'
            })
        else:
            return jsonify({'error': 'فشل في إنشاء التذكير'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mcp_bp.route('/calendar/list-events', methods=['GET'])
@cross_origin(origins='*')
def calendar_list_events():
    """عرض الأحداث من التقويم"""
    try:
        time_min = request.args.get('timeMin')
        time_max = request.args.get('timeMax')
        max_results = request.args.get('max', 10, type=int)
        
        events = mcp_services.calendar_list_events(
            time_min=time_min,
            time_max=time_max,
            max_results=max_results
        )
        
        return jsonify({
            'success': True,
            'events': events,
            'count': len(events)
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ═══════════════════════════════════════════════════════════════════════
# Health Check
# ═══════════════════════════════════════════════════════════════════════

@mcp_bp.route('/health', methods=['GET'])
@cross_origin(origins='*')
def health():
    """فحص صحة خدمات MCP"""
    return jsonify({
        'status': 'healthy',
        'service': 'MCP Services Integration',
        'services': {
            'notion': 'available',
            'gmail': 'available',
            'google-calendar': 'available'
        }
    })
