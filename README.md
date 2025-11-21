# TR5 - روبوت الدردشة الذكي

## نظرة عامة

TR5 هو روبوت دردشة ذكي متطور يستخدم تقنيات الذكاء الاصطناعي المتقدمة من Deep Seek و Hugging Face. يتميز بتصميم داكن أنيق وواجهة مستخدم تفاعلية باللغة العربية.

## الميزات الرئيسية

- 🤖 **ذكاء اصطناعي متقدم**: مدعوم بـ Deep Seek و Hugging Face
- 🎨 **تصميم داكن احترافي**: واجهة مستخدم أنيقة بألوان داكنة
- ✨ **أنيميشن سلس**: تأثيرات بصرية متطورة وتفاعلات سلسة
- 🌐 **دعم اللغة العربية**: واجهة مستخدم كاملة باللغة العربية
- 💾 **قاعدة بيانات متكاملة**: حفظ المحادثات والإعدادات
- 📱 **تصميم متجاوب**: يعمل على جميع الأجهزة

## التقنيات المستخدمة

### الواجهة الأمامية (Frontend)
- **React 18**: مكتبة JavaScript للواجهات التفاعلية
- **Framer Motion**: مكتبة الأنيميشن المتقدمة
- **Tailwind CSS**: إطار عمل CSS للتصميم السريع
- **Lucide Icons**: مجموعة أيقونات حديثة
- **Vite**: أداة البناء السريعة

### الواجهة الخلفية (Backend)
- **Flask**: إطار عمل Python للخوادم
- **SQLAlchemy**: ORM لقاعدة البيانات
- **Flask-CORS**: دعم CORS للتطبيقات المتعددة المصادر
- **SQLite**: قاعدة بيانات خفيفة وسريعة

### الذكاء الاصطناعي
- **Deep Seek API**: نموذج الذكاء الاصطناعي الرئيسي
- **Hugging Face API**: نموذج احتياطي للذكاء الاصطناعي

## هيكل المشروع

### Setup & Development

- **Install dependencies**: `npm install`
- **Run dev server**: `npm run dev` (full UI)
- **UI variants**: `npm run dev:left` (left sidebar), `npm run dev:right` (right sidebar), `npm run dev:chat` (chat only)
- **Lint**: `npm run lint`
- **Build**: `npm run build` (full UI), see package.json for variants

### Code Style

- **TypeScript**: Strict mode with proper interfaces
- **Components**: Function components with React hooks
- **Formatting**: Follow ESLint Next.js configuration
- **UI components**: Use shadcn/ui components library

## Financial Data Analyst

### Setup & Development

- **Install dependencies**: `npm install`
- **Run dev server**: `npm run dev`
- **Lint**: `npm run lint`
- **Build**: `npm run build`

### Code Style

- **TypeScript**: Strict mode with proper type definitions
- **Components**: Function components with type annotations
- **Visualization**: Use Recharts library for data visualization
- **State management**: React hooks for state
