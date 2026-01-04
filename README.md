# URSH – بوابة البحث العلمي (Enterprise Package)

هذه الحزمة تحول تطبيق Streamlit أحادي الملف إلى مشروع مؤسساتي بمعمارية:
- UI (Streamlit) منفصل
- Backend (FastAPI) + Services + Models + Core
- Docker جاهز
- Tests جاهزة

## التشغيل (Docker)
```bash
docker compose up --build
```

- الواجهة: http://localhost:8501
- الـ API: http://localhost:8000/docs

## بيانات الدخول الافتراضية (بعد الإقلاع)
- admin / 12345

> يتم إنشاء الأقسام + المستخدمين الأساسيين تلقائياً عند الإقلاع (init_data.py)

## هيكلة المشروع
- `backend/app/core`: الإعدادات + DB + Security
- `backend/app/models`: SQLAlchemy Models (مطابقة لقاعدة بياناتك)
- `backend/app/services`: منطق الأعمال
- `backend/app/api`: Routes + Dependencies + RBAC
- `frontend`: Streamlit UI فقط + API client

## تشغيل الاختبارات (Backend)
```bash
cd backend
pytest -q
```

## ملاحظات مؤسساتية
- المصادقة JWT (Stateless)
- صلاحيات Role-based (admin / dept_head / leader / researcher)
- تصدير Excel و CV PDF عبر API
