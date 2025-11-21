# دليل التكامل - منصة الدردشة الذكية المتكاملة

## نظرة عامة

تم تطوير منصة دردشة ذكية متكاملة تجمع بين:
- **واجهة الدردشة**: واجهة مستخدم حديثة للتفاعل مع الذكاء الاصطناعي
- **قاعدة البيانات**: نظام إدارة البيانات والذاكرة طويلة وقصيرة المدى
- **خدمات MCP**: تكامل مع Notion و Gmail و Google Calendar

## البنية المعمارية

```
┌─────────────────────────────────────────────────────────────┐
│                     واجهة المستخدم (Frontend)                │
│                  React + Vite + Tailwind CSS                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              الواجهة الخلفية (Backend - Flask)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Chat API    │  │  MCP Routes  │  │  DB Integration│   │
│  │  v1 & v2     │  │  Services    │  │  Manager     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌────────────────┐
│ AI Providers │ │   MCP    │ │   Platform DB  │
│ OpenAI, Groq │ │ Services │ │   (MySQL)      │
│ DeepSeek, HF │ │ N,G,GC   │ │                │
└──────────────┘ └──────────┘ └────────────────┘
```

## الميزات الرئيسية

### 1. دعم متعدد لمزودي الذكاء الاصطناعي

- **OpenAI GPT-4**: نموذج متقدم للمحادثات المعقدة
- **Groq Llama 3.3**: نموذج سريع وفعال
- **DeepSeek**: نموذج متخصص للمهام المتقدمة
- **HuggingFace**: نماذج مفتوحة المصدر

### 2. إدارة الذاكرة الذكية

#### الذاكرة قصيرة المدى
- حفظ سياق المحادثة الحالية
- استرجاع آخر N رسالة من المحادثة
- تتبع تسلسل الرسائل

#### الذاكرة طويلة المدى
- حفظ الحقائق والتفضيلات المهمة
- استخراج الأنماط من المحادثات
- تخزين المعلومات حسب الأهمية

### 3. تكامل خدمات MCP

#### Notion
- إنشاء صفحات جديدة
- حفظ المحادثات كمستندات
- البحث في الصفحات

#### Gmail
- إرسال رسائل البريد الإلكتروني
- إرسال ملخصات المحادثات
- البحث في الرسائل

#### Google Calendar
- إنشاء أحداث
- إنشاء تذكيرات
- عرض الأحداث القادمة

### 4. جمع بيانات التدريب

- حفظ المحادثات كبيانات تدريب
- تصنيف البيانات حسب النوع
- حساب عدد التوكنات
- تجنب التكرار باستخدام Hash

### 5. تسجيل الأنشطة

- تتبع جميع التفاعلات
- تسجيل الأخطاء والنجاحات
- تحليل أنماط الاستخدام

## واجهات برمجية التطبيق (API)

### Chat API v1 (الأساسية)

```
POST /api/chat
```

**Request:**
```json
{
  "message": {
    "parts": [{"type": "text", "text": "مرحباً"}]
  },
  "id": "conversation-123"
}
```

**Response:**
```json
{
  "messages": [
    {
      "id": "msg-1",
      "role": "user",
      "parts": [{"type": "text", "text": "مرحباً"}],
      "createdAt": "2025-11-21T10:00:00"
    },
    {
      "id": "msg-2",
      "role": "assistant",
      "parts": [{"type": "text", "text": "مرحباً بك!"}],
      "createdAt": "2025-11-21T10:00:01"
    }
  ],
  "chatId": "conversation-123",
  "status": "success"
}
```

### Chat API v2 (مع قاعدة البيانات)

```
POST /api/v2/chat
```

**Request:**
```json
{
  "message": {
    "parts": [{"type": "text", "text": "مرحباً"}]
  },
  "id": "conversation-123",
  "userId": 1,
  "sessionId": 5,
  "model": "auto"
}
```

**Response:**
```json
{
  "messages": [...],
  "chatId": "conversation-123",
  "status": "success",
  "modelUsed": "OpenAI GPT-4"
}
```

**الميزات الإضافية:**
- حفظ تلقائي في قاعدة البيانات
- استرجاع السياق من المحادثات السابقة
- تسجيل النشاط
- اختيار النموذج المفضل

### استرجاع السياق

```
GET /api/v2/chat/context/<conversation_id>?limit=10
```

**Response:**
```json
{
  "conversationId": "conversation-123",
  "messages": [
    {
      "role": "user",
      "content": "مرحباً",
      "createdAt": "2025-11-21T10:00:00"
    }
  ],
  "count": 1
}
```

### حفظ بيانات التدريب

```
POST /api/v2/chat/save-training
```

**Request:**
```json
{
  "userId": 1,
  "dataName": "محادثة حول البرمجة",
  "content": "المحادثة الكاملة...",
  "dataType": "conversation",
  "sessionId": 5
}
```

### Notion API

#### إنشاء صفحة
```
POST /api/mcp/notion/create-page
```

**Request:**
```json
{
  "parentId": "page-id-123",
  "title": "محادثة جديدة",
  "content": "محتوى الصفحة...",
  "properties": {}
}
```

#### حفظ محادثة
```
POST /api/mcp/notion/save-conversation
```

**Request:**
```json
{
  "parentId": "page-id-123",
  "conversationId": "conversation-123",
  "messages": [...]
}
```

#### البحث
```
GET /api/mcp/notion/search?query=محادثة&type=page
```

### Gmail API

#### إرسال بريد
```
POST /api/mcp/gmail/send
```

**Request:**
```json
{
  "to": "user@example.com",
  "subject": "الموضوع",
  "body": "المحتوى",
  "cc": [],
  "bcc": []
}
```

#### إرسال ملخص محادثة
```
POST /api/mcp/gmail/send-conversation
```

**Request:**
```json
{
  "to": "user@example.com",
  "conversationId": "conversation-123",
  "messages": [...]
}
```

#### البحث
```
GET /api/mcp/gmail/search?query=subject:محادثة&max=10
```

### Google Calendar API

#### إنشاء حدث
```
POST /api/mcp/calendar/create-event
```

**Request:**
```json
{
  "summary": "اجتماع",
  "startTime": "2025-11-21T14:00:00Z",
  "endTime": "2025-11-21T15:00:00Z",
  "description": "الوصف",
  "location": "الموقع",
  "attendees": ["user@example.com"]
}
```

#### إنشاء تذكير
```
POST /api/mcp/calendar/create-reminder
```

**Request:**
```json
{
  "summary": "تذكير مهم",
  "reminderTime": "2025-11-21T14:00:00Z",
  "description": "الوصف"
}
```

#### عرض الأحداث
```
GET /api/mcp/calendar/list-events?timeMin=2025-11-21T00:00:00Z&max=10
```

## التثبيت والتشغيل

### المتطلبات

- Python 3.11+
- Node.js 22+
- MySQL/PostgreSQL (للمنصة)

### تثبيت الواجهة الخلفية

```bash
cd chat-frontend/backend
pip install -r requirements.txt
```

### إعداد المتغيرات البيئية

```bash
cp .env.example .env
# قم بتحرير .env وإضافة المفاتيح الخاصة بك
```

### تشغيل الخادم

```bash
# الخادم الأساسي
python src/main.py

# الخادم المحسّن (مع جميع الميزات)
python src/main_enhanced.py
```

### تثبيت الواجهة الأمامية

```bash
cd chat-frontend/frontend
npm install
npm run dev
```

## النشر

### نشر الواجهة الخلفية على Vercel

```bash
cd chat-frontend/backend
vercel --prod
```

### نشر الواجهة الأمامية

```bash
cd chat-frontend/frontend
npm run build
vercel --prod
```

### ربط المنصة

تأكد من تحديث `PLATFORM_API_URL` في ملف `.env` للإشارة إلى:
```
https://aitrainhub-ifghcdxx.manus.space
```

## قاعدة البيانات

### الجداول الرئيسية

#### users
- معلومات المستخدمين
- المصادقة والأدوار

#### ai_models
- النماذج المدربة
- الإعدادات والمعاملات

#### training_sessions
- جلسات التدريب
- الحالة والتقدم

#### training_data
- بيانات التدريب
- المحتوى والتصنيف

#### short_term_memory
- الذاكرة قصيرة المدى
- سياق المحادثات

#### long_term_memory
- الذاكرة طويلة المدى
- الحقائق والأنماط

#### activity_logs
- سجلات الأنشطة
- التتبع والتحليل

#### api_configs
- إعدادات API
- المفاتيح والنقاط النهائية

## الأمان

### حماية المفاتيح
- جميع المفاتيح مخزنة في متغيرات البيئة
- عدم تضمين المفاتيح في الكود

### CORS
- مفعّل لجميع المسارات
- يمكن تخصيصه حسب الحاجة

### المصادقة
- دعم OAuth عبر Manus
- جلسات آمنة

## الاختبار

### اختبار الواجهة الخلفية

```bash
# اختبار صحة الخدمة
curl http://localhost:3000/api/health

# اختبار Chat API v2
curl -X POST http://localhost:3000/api/v2/chat \
  -H "Content-Type: application/json" \
  -d '{"message": {"parts": [{"type": "text", "text": "مرحباً"}]}, "id": "test-123"}'
```

### اختبار خدمات MCP

```bash
# اختبار صحة خدمات MCP
curl http://localhost:3000/api/mcp/health
```

## المساهمة

نرحب بالمساهمات! يرجى:
1. عمل Fork للمستودع
2. إنشاء فرع للميزة الجديدة
3. الالتزام بالتغييرات
4. فتح Pull Request

## الدعم

للمساعدة والدعم:
- افتح Issue على GitHub
- راجع التوثيق
- تواصل مع الفريق

## الترخيص

MIT License

---

**تم التطوير بواسطة:** Manus AI Platform  
**آخر تحديث:** نوفمبر 2025
