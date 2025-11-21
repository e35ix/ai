from flask import Blueprint, request, jsonify, Response
from flask_cors import cross_origin
import json
import time
import uuid
from datetime import datetime
import requests
import os

chat_bp = Blueprint('chat', __name__)

# Deep Seek API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'your-deepseek-api-key')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# Hugging Face API Configuration  
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', 'your-huggingface-api-key')
HUGGINGFACE_API_URL = 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium'

def generate_message_id():
    """Generate unique message ID"""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def call_deepseek_api(messages, model="deepseek-chat"):
    """Call Deep Seek API for chat completion"""
    try:
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Convert UI messages to API format
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
            'max_tokens': 1000
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
        f"شكراً لك على رسالتك: '{user_message}'. أنا TR5، روبوت الدردشة الذكي المدعوم بـ Deep Seek و Hugging Face.",
        f"تلقيت رسالتك: '{user_message}'. كيف يمكنني مساعدتك أكثر؟",
        f"أفهم أنك تقول: '{user_message}'. هل يمكنك توضيح المزيد حول ما تحتاجه؟",
        f"بناءً على رسالتك: '{user_message}'، أعتقد أنني يمكنني مساعدتك. ما هو السؤال المحدد؟"
    ]
    import random
    return random.choice(responses)

@chat_bp.route('/chat', methods=['POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['POST', 'OPTIONS'])
def chat():
    """Handle chat messages"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract message and chat ID
        message = data.get('message')
        chat_id = data.get('id', str(uuid.uuid4()))
        
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
        
        # Create user message
        user_message = {
            'id': generate_message_id(),
            'role': 'user',
            'parts': [{'type': 'text', 'text': user_text}],
            'createdAt': get_current_timestamp()
        }
        
        # Prepare messages for API call (including conversation history if available)
        messages_for_api = [
            {'role': 'system', 'content': 'أنت TR5، روبوت دردشة ذكي ومفيد. تجيب باللغة العربية بطريقة ودودة ومهنية.'},
            {'role': 'user', 'content': user_text}
        ]
        
        # Try Deep Seek API first
        ai_response_text = call_deepseek_api(messages_for_api)
        
        # If Deep Seek fails, try Hugging Face
        if not ai_response_text:
            ai_response_text = call_huggingface_api(user_text)
        
        # If both APIs fail, use fallback
        if not ai_response_text:
            ai_response_text = generate_fallback_response(user_text)
        
        # Create assistant message
        assistant_message = {
            'id': generate_message_id(),
            'role': 'assistant',
            'parts': [{'type': 'text', 'text': ai_response_text}],
            'createdAt': get_current_timestamp()
        }
        
        # Return both messages
        response_data = {
            'messages': [user_message, assistant_message],
            'chatId': chat_id,
            'status': 'success'
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@chat_bp.route('/chat/stream', methods=['POST', 'OPTIONS'])
@cross_origin(origins='*', methods=['POST', 'OPTIONS'])
def chat_stream():
    """Handle streaming chat messages (for future implementation)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    def generate_stream():
        try:
            data = request.get_json()
            message = data.get('message', '')
            
            # Simulate streaming response
            response_text = f"هذه استجابة متدفقة من TR5 لرسالتك: {message}"
            
            for i, char in enumerate(response_text):
                chunk_data = {
                    'type': 'text',
                    'content': char,
                    'index': i
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
                time.sleep(0.05)  # Simulate typing delay
            
            # Send completion signal
            completion_data = {
                'type': 'complete',
                'message_id': generate_message_id(),
                'timestamp': get_current_timestamp()
            }
            yield f"data: {json.dumps(completion_data)}\n\n"
            
        except Exception as e:
            error_data = {
                'type': 'error',
                'error': str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return Response(
        generate_stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        }
    )

@chat_bp.route('/health', methods=['GET'])
@cross_origin(origins='*')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TR5 Chat Backend',
        'timestamp': get_current_timestamp(),
        'apis': {
            'deepseek': 'configured' if DEEPSEEK_API_KEY != 'your-deepseek-api-key' else 'not_configured',
            'huggingface': 'configured' if HUGGINGFACE_API_KEY != 'your-huggingface-api-key' else 'not_configured'
        }
    })

