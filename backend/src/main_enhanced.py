import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.chat import db
from src.routes.chat import chat_bp
from src.routes.chat_enhanced import chat_enhanced_bp
from src.routes.mcp_routes import mcp_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Enable CORS for all routes
CORS(app, origins='*', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Register blueprints
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(chat_enhanced_bp, url_prefix='/api/v2')
app.register_blueprint(mcp_bp, url_prefix='/api/mcp')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 500

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/info', methods=['GET'])
def api_info():
    """معلومات عن API"""
    return {
        'name': 'Enhanced AI Chat Platform',
        'version': '2.0.0',
        'description': 'منصة دردشة ذكية متكاملة مع قاعدة بيانات وخدمات MCP',
        'endpoints': {
            'chat': {
                'v1': '/api/chat',
                'v2': '/api/v2/chat (with database integration)'
            },
            'mcp_services': {
                'notion': '/api/mcp/notion/*',
                'gmail': '/api/mcp/gmail/*',
                'calendar': '/api/mcp/calendar/*'
            },
            'database': {
                'context': '/api/v2/chat/context/<conversation_id>',
                'training': '/api/v2/chat/save-training'
            }
        },
        'features': [
            'Multi-AI Provider Support (OpenAI, Groq, DeepSeek, HuggingFace)',
            'Database Integration with Platform',
            'Conversation Memory (Short & Long Term)',
            'Notion Integration',
            'Gmail Integration',
            'Google Calendar Integration',
            'Training Data Collection',
            'Activity Logging'
        ]
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
