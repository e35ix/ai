# دليل البدء السريع - منصة الدردشة الذكية

## 🚀 البدء السريع

### 1. استنساخ المستودعات

```bash
# واجهة الدردشة
git clone https://github.com/e35ix/ai.git
cd ai

# قاعدة البيانات (اختياري)
git clone https://github.com/e35ix/AI_Training_Platform.git
```

### 2. إعداد الواجهة الخلفية

```bash
cd ai/backend

# إنشاء ملف .env من النموذج
cp .env.example .env

# تحرير .env وإضافة المفاتيح الخاصة بك
nano .env

# تثبيت المتطلبات
pip install -r requirements_enhanced.txt

# تشغيل الخادم
python src/main_enhanced.py
```

الخادم سيعمل على: `http://localhost:3000`

### 3. إعداد الواجهة الأمامية

```bash
cd ai/frontend

# تثبيت المتطلبات
npm install

# تشغيل الخادم
npm run dev
```

الواجهة ستعمل على: `http://localhost:5173`

## 🔑 المفاتيح المطلوبة

أضف المفاتيح التالية في ملف `.env`:

```env
# اختر واحداً على الأقل من المفاتيح التالية
OPENAI_API_KEY=your-openai-key
GROQ_API_KEY=your-groq-key
DEEPSEEK_API_KEY=your-deepseek-key
HUGGINGFACE_API_KEY=your-huggingface-key

# للتكامل مع المنصة
PLATFORM_API_URL=https://aitrainhub-ifghcdxx.manus.space

# إعدادات Flask
FLASK_SECRET_KEY=your-secret-key
```

## 📡 اختبار API

### اختبار صحة الخدمة

```bash
curl http://localhost:3000/api/v2/health
```

### اختبار المحادثة

```bash
curl -X POST http://localhost:3000/api/v2/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": {"parts": [{"type": "text", "text": "مرحباً"}]},
    "id": "test-123"
  }'
```

### اختبار خدمات MCP

```bash
# Notion
curl http://localhost:3000/api/mcp/notion/search?query=test

# Gmail
curl http://localhost:3000/api/mcp/gmail/search?query=test

# Calendar
curl http://localhost:3000/api/mcp/calendar/list-events
```

## 🌐 الروابط المباشرة

- **الواجهة الخلفية المنشورة:** https://backend-six-plum-75.vercel.app
- **قاعدة البيانات:** https://aitrainhub-ifghcdxx.manus.space
- **مستودع الدردشة:** https://github.com/e35ix/ai
- **مستودع المنصة:** https://github.com/e35ix/AI_Training_Platform

## 📚 التوثيق الكامل

راجع الملفات التالية للمزيد من التفاصيل:

- `INTEGRATION_GUIDE.md` - دليل التكامل الشامل
- `PROJECT_COMPLETION_REPORT.md` - تقرير إكمال المشروع
- `platform-backend/UPDATES.md` - تحديثات المنصة

## 🆘 المساعدة

إذا واجهت أي مشاكل:

1. تأكد من تثبيت جميع المتطلبات
2. تحقق من ملف `.env` والمفاتيح
3. راجع سجلات الأخطاء
4. افتح Issue على GitHub

## ✨ الميزات الرئيسية

- ✅ دعم 4 مزودين للذكاء الاصطناعي
- ✅ ذاكرة قصيرة وطويلة المدى
- ✅ تكامل Notion, Gmail, Calendar
- ✅ حفظ تلقائي للمحادثات
- ✅ جمع بيانات التدريب
- ✅ تسجيل الأنشطة

---

**جاهز للاستخدام!** 🎉
