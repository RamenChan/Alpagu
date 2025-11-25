# PyGuardian Home Edition - Hızlı Başlangıç

## 🚀 5 Dakikada Başlatın

### 1. Servisleri Başlatın

```bash
docker-compose -f docker-compose.home.yml up -d
```

### 2. Web Arayüzüne Gidin

http://localhost:3000

### 3. Hesap Oluşturun

- "Create account" butonuna tıklayın
- Email, kullanıcı adı ve şifre girin
- Kayıt olduktan sonra otomatik giriş yapılacak

### 4. Test Alert'leri Oluşturun (Opsiyonel)

```bash
docker-compose -f docker-compose.home.yml exec api python scripts/create_test_alert.py
```

Bu komut, hesabınız için örnek alert'ler oluşturur.

## 📋 Özellikler

✅ Kullanıcı kayıt ve giriş sistemi  
✅ Dashboard ile ağ izleme  
✅ Alarm yönetimi  
✅ Email ve webhook bildirimleri  
✅ Basit ve kullanıcı dostu arayüz  

## 🔧 Servisler

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

## 📚 Daha Fazla Bilgi

Detaylı dokümantasyon için [HOME_EDITION_README.md](HOME_EDITION_README.md) dosyasına bakın.

