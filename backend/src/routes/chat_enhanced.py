from flask import Blueprint, request, jsonify, Response
from flask_cors import cross_origin
import json
import time
import uuid
from datetime import datetime
import requests
import os
import sys

# إضافة مسار الوحدات
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database.db_integration import db_integration

chat_enhanced_bp = Blueprint('chat_enhanced', __name__)

# Deep Seek API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# Hugging Face API Configuration  
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
HUGGINGFACE_API_URL = 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium'

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'

# Groq API Configuration
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

def generate_message_id():
    """Generate unique message ID"""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def call_openai_api(messages, model="gpt-4o-mini"):
    """Call OpenAI API for chat completion"""
    try:
        if not OPENAI_API_KEY:
            return None
            
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        api_messages = []
        for msg in messages:
            if msg.get('role') in ['user', 'assistant', 'system']:
                content = ""
                if 'parts' in msg:
                    content = ''.join([part.get('text', '') for part in msg['parts'] if part.get('type') == 'text'])
                else:
                    content = msg.get('content', '')
                
                api_messages.append({
                    'role': msg['role'],
                    'content': content
                })
        
        payload = {
            'model': model,
            'messages': api_messages,
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"OpenAI API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"OpenAI API Exception: {str(e)}")
        return None

def call_groq_api(messages, model="llama-3.3-70b-versatile"):
    """Call Groq API for chat completion"""
    try:
        if not GROQ_API_KEY:
            return None
            
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        api_messages = []
        for msg in messages:
            if msg.get('role') in ['user', 'assistant', 'system']:
                content = ""
                if 'parts' in msg:
                    content = ''.join([part.get('text', '') for part in msg['parts'] if part.get('type') == 'text'])
                else:
                    content = msg.get('content', '')
                
                api_messages.append({
                    'role': msg['role'],
                    'content': content
                })
        
        payload = {
            'model': model,
            'messages': api_messages,
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"Groq API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Groq API Exception: {str(e)}")
        return None

def call_deepseek_api(messages, model="deepseek-chat"):
    """Call Deep Seek API for chat completion"""
    try:
        if not DEEPSEEK_API_KEY:
            return None
            
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        api_messages = []
        for msg in messages:
            if msg.get('role') in ['user', 'assistant', 'system']:
                content = ""
                if 'parts' in msg:
                    content = ''.join([part.get('text', '') for part in msg['parts'] if part.get('type') == 'text'])
                else:
                    content = msg.get('content', '')
                
                api_messages.append({
                    'role': msg['role'],
                    'content': content
                })
        
        payload = {
            'model': model,
            'messages': api_messages,
            'stream': False,
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"Deep Seek API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Deep Seek API Exception: {str(e)}")
        return None

def call_huggingface_api(text):
    """Call Hugging Face API for text generation"""
    try:
        if not HUGGINGFACE_API_KEY:
            return None
            
        headers = {
            'Authorization': f'Bearer {HUGGINGFACE_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'inputs': text,
            'parameters': {
                'max_length': 200,
                'temperature': 0.7,
                'do_sample': True
            }
        }
        
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').replace(text, '').strip()
            return None
        else:
            print(f"Hugging Face API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Hugging Face API Exception: {str(e)}")
        return None

def generate_fallback_response(user_message):
    """Generate fallback response when APIs are not available"""
    responses = [
        f"شكراً لك على رسالتك: '{user_message}'. أنا مساعدك الذكي المدعوم بتقنيات الذكاء الاصطناعي المتقدمة.",
        f"تلقيت رسالتك: '{user_message}'. كيف يمكنني مساعدتك أكثر؟",
        f"أفهم أنك تقول: '{user_message}'. هل يمكنك توضيح المزيد حول ما تحتاجه؟",
        f"بناءً على رسالتك: '{user_message}'، أعتقد أنني يمكنني مساعدتك. ما هو السؤال المحدد؟"
    ]
    import random
    return random.choice(responses)

@chat_enhanced_bp.route('/chat', methods=['POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['POST', 'OPTIONS'])
def chat():
    """Handle chat messages with database integration"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract message and chat ID
        message = data.get('message')
        chat_id = data.get('id', str(uuid.uuid4()))
        user_id = data.get('userId', 1)  # معرف المستخدم الافتراضي
        session_id = data.get('sessionId')  # معرف الجلسة (اختياري)
        model_preference = data.get('model', 'auto')  # تفضيل النموذج
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Extract user message text
        user_text = ""
        if 'parts' in message:
            user_text = ''.join([part.get('text', '') for part in message['parts'] if part.get('type') == 'text'])
        else:
            user_text = message.get('content', '')
        
        if not user_text.strip():
            return jsonify({'error': 'Empty message'}), 400
        
        # استرجاع سياق المحادثة من قاعدة البيانات
        conversation_context = db_integration.get_conversation_context(chat_id, limit=5)
        
        # Create user message
        user_message = {
            'id': generate_message_id(),
            'role': 'user',
            'parts': [{'type': 'text', 'text': user_text}],
            'createdAt': get_current_timestamp()
        }
        
        # Prepare messages for API call (including conversation history)
        messages_for_api = [
            {'role': 'system', 'content': 'أنت مساعد ذكي ومفيد. تجيب باللغة العربية بطريقة ودودة ومهنية. لديك ذاكرة طويلة المدى وتستطيع تذكر المحادثات السابقة.'}
        ]
        
        # إضافة السياق من قاعدة البيانات
        for ctx_msg in conversation_context:
            messages_for_api.append({
                'role': ctx_msg.get('role', 'user'),
                'content': ctx_msg.get('content', '')
            })
        
        # إضافة الرسالة الحالية
        messages_for_api.append({'role': 'user', 'content': user_text})
        
        # Try different AI APIs based on preference
        ai_response_text = None
        used_model = None
        
        if model_preference == 'openai' or model_preference == 'auto':
            ai_response_text = call_openai_api(messages_for_api)
            if ai_response_text:
                used_model = 'OpenAI GPT-4'
        
        if not ai_response_text and (model_preference == 'groq' or model_preference == 'auto'):
            ai_response_text = call_groq_api(messages_for_api)
            if ai_response_text:
                used_model = 'Groq Llama 3.3'
        
        if not ai_response_text and (model_preference == 'deepseek' or model_preference == 'auto'):
            ai_response_text = call_deepseek_api(messages_for_api)
            if ai_response_text:
                used_model = 'DeepSeek'
        
        if not ai_response_text and (model_preference == 'huggingface' or model_preference == 'auto'):
            ai_response_text = call_huggingface_api(user_text)
            if ai_response_text:
                used_model = 'HuggingFace'
        
        # If all APIs fail, use fallback
        if not ai_response_text:
            ai_response_text = generate_fallback_response(user_text)
            used_model = 'Fallback'
        
        # Create assistant message
        assistant_message = {
            'id': generate_message_id(),
            'role': 'assistant',
            'parts': [{'type': 'text', 'text': ai_response_text}],
            'createdAt': get_current_timestamp(),
            'model': used_model
        }
        
        # حفظ المحادثة في قاعدة البيانات
        db_integration.save_conversation(
            user_id=user_id,
            conversation_id=chat_id,
            user_message=user_text,
            assistant_response=ai_response_text,
            session_id=session_id
        )
        
        # تسجيل النشاط
        db_integration.log_activity(
            user_id=user_id,
            action='chat_interaction',
            resource_type='conversation',
            details={
                'conversation_id': chat_id,
                'model_used': used_model,
                'message_length': len(user_text)
            }
        )
        
        # Return both messages
        response_data = {
            'messages': [user_message, assistant_message],
            'chatId': chat_id,
            'status': 'success',
            'modelUsed': used_model
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_enhanced_bp.route('/chat/context/<conversation_id>', methods=['GET'])
@cross_origin(origins='*')
def get_context(conversation_id):
    """Get conversation context from database"""
    try:
        limit = request.args.get('limit', 10, type=int)
        context = db_integration.get_conversation_context(conversation_id, limit)
        
        return jsonify({
            'conversationId': conversation_id,
            'messages': context,
            'count': len(context)
        })
        
    except Exception as e:
        print(f"Context endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_enhanced_bp.route('/chat/save-training', methods=['POST'])
@cross_origin(origins='*')
def save_training():
    """Save conversation as training data"""
    try:
        data = request.get_json()
        
        user_id = data.get('userId', 1)
        data_name = data.get('dataName', f'Training_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        content = data.get('content', '')
        data_type = data.get('dataType', 'conversation')
        session_id = data.get('sessionId')
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        data_id = db_integration.save_training_data(
            user_id=user_id,
            data_name=data_name,
            content=content,
            data_type=data_type,
            session_id=session_id
        )
        
        return jsonify({
            'success': True,
            'dataId': data_id,
            'message': 'تم حفظ بيانات التدريب بنجاح'
        })
        
    except Exception as e:
        print(f"Save training endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_enhanced_bp.route('/health', methods=['GET'])
@cross_origin(origins='*')
def health_check():
    """Health check endpoint with enhanced info"""
    return jsonify({
        'status': 'healthy',
        'service': 'Enhanced Chat Backend with DB Integration',
        'timestamp': get_current_timestamp(),
        'apis': {
            'openai': 'configured' if OPENAI_API_KEY else 'not_configured',
            'groq': 'configured' if GROQ_API_KEY else 'not_configured',
            'deepseek': 'configured' if DEEPSEEK_API_KEY else 'not_configured',
            'huggingface': 'configured' if HUGGINGFACE_API_KEY else 'not_configured'
        },
        'database': {
            'platform_url': db_integration.api_url,
            'connected': bool(db_integration.api_key)
        }
    })
