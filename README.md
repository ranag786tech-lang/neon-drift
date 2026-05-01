# 🚀 Empowerment Platform - Quick Start Guide

## ایک لمحے میں پورا سسٹم چلائیں!

### ضروریات (Prerequisites)
- Docker & Docker Compose
- 4GB RAM کم از کم
- 10GB خالی جگہ

---

## 🔥 تیز شروعات (Quick Start)

### مرحلہ 1: سسٹم کو ایک کمانڈ سے چلائیں
```bash
cd /workspace
docker-compose up -d --build
```

### مرحلہ 2: سروسز کی جانچ کریں
```bash
docker-compose ps
```

### مرحلہ 3: ڈیمو کہانی دیکھیں
```bash
python3 demo_story.py
```

---

## 🌐 دستیاب پورٹس

| سروس | URL | تفصیل |
|------|-----|--------|
| **Frontend** | http://localhost:3000 | React Dashboard |
| **API** | http://localhost:8000 | FastAPI Backend |
| **PostgreSQL** | localhost:5432 | Structured Data |
| **MongoDB** | localhost:27017 | Document Store |
| **Redis** | localhost:6379 | Caching |
| **Grafana** | http://localhost:3001 | Monitoring (admin/admin) |
| **Prometheus** | http://localhost:9090 | Metrics |

---

## 🧪 API ٹیسٹنگ

### Health Check
```bash
curl http://localhost:8000/health
```

### AI Explanation Generate کریں
```bash
curl -X POST http://localhost:8000/api/v1/explain \
  -H "Content-Type: application/json" \
  -d '{
    "decision_type": "loan_approval",
    "input_features": {"income": 50000, "credit_score": 720},
    "outcome": "approved"
  }'
```

### Fairness Audit چلائیں
```bash
curl -X POST http://localhost:8000/api/v1/audit/run \
  -H "Content-Type: application/json" \
  -d '{"dataset_id": "test_001"}'
```

---

## 🛑 سسٹم روکیں
```bash
docker-compose down
```

### ڈیٹا سمیت سب کچھ صاف کریں
```bash
docker-compose down -v
```

---

## 📊 لاگز دیکھیں
```bash
# تمام لاگز
docker-compose logs -f

# صرف API لاگز
docker-compose logs -f api-service
```

---

## 🏗️ تعمیر نو (Rebuild)
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎯 کیا شامل ہے؟

✅ **Trust & Transparency Dashboard** - AI فیصلوں کی وضاحت  
✅ **Unified Knowledge Hub** - تمام ڈیٹا ایک جگہ  
✅ **Adaptive Learning Engine** - خودکار ورک فلوز  
✅ **Global Collaboration Bridge** - کثیر لسانی ترجمہ  
✅ **Sustainability Optimizer** - توانائی کی بچت  
✅ **Production Database** - PostgreSQL + MongoDB  
✅ **Authentication** - JWT سکیورٹی  
✅ **Monitoring** - Prometheus + Grafana  

---

## 📝 نوٹس

- پہلی بار چلانے میں 5-10 منٹ لگ سکتے ہیں (images download ہونے میں)
- Default credentials: `admin/admin` (Grafana)
- Production میں JWT_SECRET اور passwords ضرور تبدیل کریں

---

**بنایا گیا ہے Microsoft کے وژن کے ساتھ:**  
*ہر شخص اور ہر تنظیم کو زیادہ حاصل کرنے کے لیے بااختیار بنانا۔*
