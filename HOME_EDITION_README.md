# PyGuardian Home Edition

Ev kullanıcıları için basitleştirilmiş ağ izleme ve anomali tespit platformu.

## 🏠 Özellikler

- **Kullanıcı Hesapları**: Kendi hesabınızı oluşturun ve giriş yapın
- **Ağ İzleme**: İç ağınızı gerçek zamanlı olarak izleyin
- **Anomali Tespiti**: Şüpheli aktiviteleri otomatik olarak tespit edin
- **Alarm Sistemi**: Anomali durumunda email veya webhook ile bildirim alın
- **Basit Dashboard**: Kolay kullanımlı web arayüzü
- **Hafif Kurulum**: Minimal kaynak kullanımı ile ev ortamına uygun

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Docker ve Docker Compose
- 2GB RAM minimum (4GB önerilir)
- 10GB disk alanı
- İnternet bağlantısı

### Kurulum

1. **Projeyi klonlayın veya indirin**

```bash
git clone <repository-url>
cd Alpagu
```

2. **Docker Compose ile başlatın**

```bash
# Home edition için özel docker-compose dosyasını kullanın
docker-compose -f docker-compose.home.yml up -d
```

3. **Servislerin çalıştığını kontrol edin**

```bash
docker-compose -f docker-compose.home.yml ps
```

4. **Web arayüzüne erişin**

- **Web Arayüzü**: http://localhost:3000
- **API Dokümantasyonu**: http://localhost:8000/docs

### İlk Kullanım

1. Web arayüzüne gidin: http://localhost:3000
2. "Create account" butonuna tıklayın
3. Hesap bilgilerinizi girin:
   - Email adresi
   - Kullanıcı adı
   - Şifre (en az 8 karakter)
   - İsim (opsiyonel)
4. Kayıt olduktan sonra otomatik olarak giriş yapılacaksınız
5. Dashboard'da ağ izleme verilerinizi görebilirsiniz

## 📊 Kullanım

### Dashboard

Dashboard'da şunları görebilirsiniz:
- Toplam alarm sayısı
- Yeni alarmlar
- Kritik ve yüksek öncelikli alarmlar
- Bugün ve bu hafta oluşan alarmlar
- Son alarmlar listesi

### Alarmlar

Alarmlar sayfasında:
- Tüm alarmları görüntüleyebilirsiniz
- Alarm durumlarını filtreleyebilirsiniz (yeni, kabul edildi, çözüldü, yanlış pozitif)
- Şiddet seviyesine göre filtreleyebilirsiniz (kritik, yüksek, orta, düşük)
- Alarmları kabul edebilir veya çözüldü olarak işaretleyebilirsiniz

### Ayarlar

Ayarlar sayfasında üç sekme bulunur:

#### Profil
- İsim ve email bilgilerinizi güncelleyebilirsiniz

#### Bildirimler
- Email bildirimlerini açıp kapatabilirsiniz
- Email adresinizi ayarlayabilirsiniz
- Webhook bildirimlerini yapılandırabilirsiniz
- Hangi şiddet seviyesindeki alarmlar için bildirim almak istediğinizi seçebilirsiniz
- Sessiz saatler ayarlayabilirsiniz (belirli saatlerde bildirim almayın)

#### Şifre
- Şifrenizi değiştirebilirsiniz

## 🔔 Bildirim Sistemi

### Email Bildirimleri

Email bildirimlerini etkinleştirmek için:
1. Ayarlar > Bildirimler sekmesine gidin
2. "Enable email notifications" seçeneğini işaretleyin
3. Email adresinizi girin
4. Hangi şiddet seviyelerinde bildirim almak istediğinizi seçin

**Not**: Production ortamında SMTP ayarlarını yapılandırmanız gerekir. Şu anda bildirimler konsola yazdırılmaktadır.

### Webhook Bildirimleri

Webhook bildirimlerini kullanmak için:
1. Ayarlar > Bildirimler sekmesine gidin
2. "Enable webhook notifications" seçeneğini işaretleyin
3. Webhook URL'nizi girin
4. Hangi şiddet seviyelerinde bildirim almak istediğinizi seçin

Webhook payload formatı:
```json
{
  "alert_id": "uuid",
  "title": "Alert Title",
  "description": "Alert Description",
  "severity": "critical|high|medium|low",
  "risk_score": 85.5,
  "source_ip": "192.168.1.100",
  "dest_ip": "203.0.113.45",
  "created_at": "2024-01-15T10:30:45.123Z"
}
```

## 🛠️ Yapılandırma

### Ortam Değişkenleri

Backend için önemli ortam değişkenleri:

```bash
# Database
DATABASE_URL=postgresql://user:password@postgres:5432/dbname

# Security (Production'da mutlaka değiştirin!)
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
JWT_EXPIRE_MINUTES=43200  # 30 days

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false  # Production'da false yapın
LOG_LEVEL=INFO
```

### Production Kullanımı

Production ortamında:

1. **Güvenlik ayarlarını değiştirin**:
   - `SECRET_KEY` ve `JWT_SECRET` değerlerini güçlü, rastgele değerlerle değiştirin
   - `DEBUG=false` yapın

2. **Email bildirimleri için SMTP ayarlarını yapılandırın**:
   - `backend/api/notifications.py` dosyasındaki email gönderme fonksiyonunu güncelleyin
   - SMTP sunucu bilgilerinizi ekleyin

3. **HTTPS kullanın**:
   - Reverse proxy (nginx, traefik) kullanarak HTTPS sağlayın
   - SSL sertifikası yapılandırın

4. **Veritabanı yedekleme**:
   - PostgreSQL veritabanını düzenli olarak yedekleyin

## 📝 API Kullanımı

API dokümantasyonuna http://localhost:8000/docs adresinden erişebilirsiniz.

### Örnek API Kullanımı

**Kayıt Olma**:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "user123",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Giriş Yapma**:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Alarmları Listeleme** (Token gerekli):
```bash
curl -X GET "http://localhost:8000/api/alerts/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔧 Sorun Giderme

### Servisler başlamıyor

```bash
# Logları kontrol edin
docker-compose -f docker-compose.home.yml logs

# Servisleri yeniden başlatın
docker-compose -f docker-compose.home.yml restart
```

### Veritabanı bağlantı hatası

```bash
# PostgreSQL'in çalıştığını kontrol edin
docker-compose -f docker-compose.home.yml ps postgres

# Veritabanını sıfırlayın (dikkat: tüm veriler silinir!)
docker-compose -f docker-compose.home.yml down -v
docker-compose -f docker-compose.home.yml up -d
```

### Frontend API'ye bağlanamıyor

- `REACT_APP_API_URL` ortam değişkeninin doğru olduğundan emin olun
- Backend servisinin çalıştığını kontrol edin: http://localhost:8000/health
- CORS ayarlarını kontrol edin

## 📚 Daha Fazla Bilgi

- [Ana Proje README](README.md)
- [Mimari Dokümantasyon](ARCHITECTURE.md)
- [Güvenlik Rehberi](SECURITY.md)

## 🆘 Destek

Sorularınız için:
- GitHub Issues: [Proje Issues](https://github.com/your-repo/issues)
- Email: anillemree@gmail.com

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

**Not**: Bu Home Edition versiyonu, enterprise özelliklerin basitleştirilmiş bir versiyonudur. Daha gelişmiş özellikler için enterprise versiyonunu kullanabilirsiniz.

