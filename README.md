# 🚀 X4G Railway - Iran Optimized

<p align="center">
  <img src="https://img.shields.io/badge/X4G-Railway-blue?style=for-the-badge&logo=railway">
  <img src="https://img.shields.io/badge/VLESS-WebSocket-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Reality-XTLS-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/Iran-Optimized-red?style=for-the-badge">
</p>

## 📋 فهرست مطالب
- [معرفی](#معرفی)
- [ویژگی‌ها](#ویژگیها)
- [دیپلوی روی Railway](#دیپلوی-روی-railway)
- [تنظیم Cloudflare CDN](#تنظیم-cloudflare-cdn)
- [نکات بهینه‌سازی برای ایران](#نکات-بهینهسازی-برای-ایران)
- [متغیرهای محیطی](#متغیرهای-محیطی)
- [پروتکل‌های پشتیبانی‌شده](#پروتکلهای-پشتیبانishده)
- [ربات تلگرام](#ربات-تلگرام)
- [عیب‌یابی](#عیبیابی)

---

## 🎯 معرفی

X4G Railway یک **Gateway VLESS بهینه‌شده برای ایران** است که روی پلتفرم **Railway** اجرا می‌شود. این پروژه شامل:

- ✅ **پنل وب مدیریتی** با رابط کاربری مدرن
- ✅ **ربات تلگرام** برای مدیریت از راه دور
- ✅ **3 پروتکل** همزمان: WebSocket + XHTTP + Reality
- ✅ **CDN-Ready** با پشتیبانی از Cloudflare
- ✅ **Fragment & XTLS Vision** برای دور زدن DPI
- ✅ **Subscription** برای V2RayNG, Nekoray, Clash, Sing-box

---

## ✨ ویژگی‌ها

| ویژگی | توضیحات |
|-------|---------|
| 🌐 **VLESS + WS** | عبور از فیلترینگ با WebSocket + CDN |
| ⚡ **VLESS + XHTTP** | Split Mode برای سرعت بالا |
| 🔒 **VLESS + Reality** | XTLS Vision با پینگ پایین |
| 🤖 **ربات تلگرام** | ساخت کانفیگ، QR Code، وضعیت سرور |
| 📊 **داشبورد Real-time** | نمایش CPU, RAM, Disk |
| 📱 **Subscription** | Base64 + Clash YAML |
| 🎨 **UI مدرن** | Dark/Light + RTL کامل |
| 🐳 **Docker Ready** | یک دستور برای اجرا |

---

## 🚀 دیپلوی روی Railway

### مرحله ۱: Fork کردن ریپوزیتوری

```bash
# Clone کنید
git clone https://github.com/YOUR_USERNAME/X4G-Railway.git
cd X4G-Railway

# یا مستقیم از GitHub
```

### مرحله ۲: ساخت پروژه در Railway

1. به [Railway](https://railway.app) بروید و لاگین کنید
2. روی **New Project** → **Deploy from GitHub repo** کلیک کنید
3. ریپوزیتوری X4G-Railway را انتخاب کنید
4. Railway به‌صورت خودکار Dockerfile را تشخیص می‌دهد

### مرحله ۳: تنظیم متغیرهای محیطی

در بخش **Variables** پنل Railway، این متغیرها را اضافه کنید:

```
PANEL_USER=admin
PANEL_PASS=رمز_قوی_شما
DOMAIN=your-domain.railway.app
TELEGRAM_BOT_TOKEN=توکن_ربات_تلگرام
TELEGRAM_ADMIN_ID=آیدی_عددی_تلگرام
REALITY_ENABLED=true
FRAGMENT_ENABLED=true
```

> ⚠️ **مهم:** `DOMAIN` را با دامنه Railway خود جایگزین کنید (از بخش Settings → Domains کپی کنید)

### مرحله ۴: Generate Domain

1. در پنل Railway → **Settings** → **Domains**
2. روی **Generate Domain** کلیک کنید
3. دامنه به‌صورت `your-project.up.railway.app` ایجاد می‌شود
4. این دامنه را در متغیر `DOMAIN` قرار دهید

### مرحله ۵: Redeploy

بعد از تنظیم متغیرها، Railway به‌صورت خودکار Redeploy می‌کند.

---

## ☁️ تنظیم Cloudflare CDN

برای **پینگ بهتر در ایران**، حتماً از Cloudflare استفاده کنید:

### ۱. اضافه کردن دامنه به Cloudflare

1. دامنه‌ی خود را در Cloudflare ثبت کنید
2. رکورد **CNAME** بسازید:
   ```
   Name: proxy (یا هر چیزی)
   Target: your-project.up.railway.app
   Proxy Status: 🟠 Proxied
   ```

### ۲. تنظیم SSL/TLS

1. در Cloudflare → **SSL/TLS** → **Overview**
2. حالت را روی **Full (strict)** قرار دهید

### ۳. تنظیمات بهینه

| تنظیم | مقدار |
|-------|-------|
| SSL/TLS | Full (strict) |
| Always Use HTTPS | ON |
| HTTP Strict Transport Security (HSTS) | ON |
| Minimum TLS Version | 1.2 |
| Opportunistic Encryption | ON |
| TLS 1.3 | ON |
| Automatic HTTPS Rewrites | ON |

### ۴. Network Settings

```
HTTP/2: ON
HTTP/3 (QUIC): ON
0-RTT Connection Resumption: ON
WebSockets: ON
```

### ۵. Update DOMAIN Variable

متغیر `DOMAIN` را به دامنه Cloudflare خود تغییر دهید:
```
DOMAIN=proxy.yourdomain.com
```

سپس Redeploy کنید.

---

## 🇮🇷 نکات بهینه‌سازی برای ایران

### ۱. استفاده از Fragment در کلاینت

در **V2RayNG** یا **Nekoray**، Fragment را فعال کنید:

```json
{
  "fragment": {
    "packets": "tlshello",
    "length": "100-200",
    "interval": "10-20"
  }
}
```

### ۲. انتخاب پروتکل مناسب

| وضعیت اینترنت | پروتکل پیشنهادی |
|--------------|----------------|
| فیلترینگ سنگین | **WebSocket + CDN** |
| سرعت پایین | **XHTTP Split** |
| IP تمیز دارید | **Reality** |
| ناپایداری | **WebSocket + CDN** |

### ۳. استفاده از Warp/Warp+

برای عبور از محدودیت‌های بیشتر، می‌توانید Xray را با **WARP** ترکیب کنید:

```bash
# در سرور
curl -fsSL https://pkg.cloudflareclient.com/install.sh | sh
warp-cli register
warp-cli set-mode proxy
warp-cli connect
```

### ۴. تغییر دوره‌ای UUID

برای امنیت بیشتر، هر چند وقت یک‌بار UUID را تغییر دهید:

```bash
# در پنل Railway، متغیر UUID را آپدیت کنید
# یا از طریق API Railway
```

---

## 🔧 متغیرهای محیطی

| متغیر | پیش‌فرض | توضیحات |
|-------|---------|---------|
| `PANEL_USER` | `admin` | نام کاربری پنل |
| `PANEL_PASS` | `danial905749` | رمز عبور پنل |
| `UUID` | `auto` | UUID کلاینت (auto = تولید خودکار) |
| `DOMAIN` | `auto` | دامنه سرور |
| `PORT` | `8080` | پورت Railway |
| `REALITY_ENABLED` | `true` | فعال‌سازی Reality |
| `REALITY_PRIVATE` | `auto` | کلید خصوصی Reality |
| `REALITY_PUBLIC` | `auto` | کلید عمومی Reality |
| `TELEGRAM_BOT_TOKEN` | - | توکن ربات تلگرام |
| `TELEGRAM_ADMIN_ID` | - | آیدی عددی ادمین |
| `CDN_MODE` | `cloudflare` | نوع CDN |

---

## 🔌 پروتکل‌های پشتیبانی‌شده

### ۱. VLESS + WebSocket (CDN)
```
vless://UUID@DOMAIN:443?type=ws&path=/ws&host=DOMAIN&security=tls&sni=DOMAIN&fp=chrome#WS_X4G
```
- ✅ بهترین برای فیلترینگ ایران
- ✅ سازگار با Cloudflare CDN
- ✅ قابل استفاده با Fragment

### ۲. VLESS + XHTTP (Split)
```
vless://UUID@DOMAIN:443?type=xhttp&path=/xhttp&host=DOMAIN&mode=auto&security=tls#XHTTP_X4G
```
- ⚡ سرعت بالا با Split Mode
- ✅ Uplink/Downlink جداگانه
- ✅ مناسب برای شبکه‌های ناپایدار

### ۳. VLESS + Reality (Direct)
```
vless://UUID@DOMAIN:443?type=tcp&security=reality&flow=xtls-rprx-vision&sni=www.google.com&pbk=PUBLIC_KEY&sid=SHORT_ID#REALITY_X4G
```
- 🔒 پینگ پایین‌تر
- ✅ بدون نیاز به CDN
- ⚠️ نیاز به IP تمیز

---

## 🤖 ربات تلگرام

### راه‌اندازی

1. به [@BotFather](https://t.me/BotFather) بروید
2. `/newbot` را بفرستید و یک ربات بسازید
3. توکن را کپی کنید
4. آیدی عددی خود را از [@userinfobot](https://t.me/userinfobot) بگیرید
5. در Railway → Variables اضافه کنید:
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   TELEGRAM_ADMIN_ID=123456789
   ```

### دستورات ربات

| دستور | عملکرد |
|-------|--------|
| `/start` | منوی اصلی |
| `/status` | وضعیت سرور |
| `/help` | راهنما |

### دکمه‌های Inline
- 🔗 دریافت کانفیگ WS
- 🔗 دریافت کانفیگ XHTTP
- 🔗 دریافت کانفیگ Reality
- 📊 وضعیت سرور
- 📋 همه کانفیگ‌ها

---

## 🐳 اجرا با Docker (Local)

```bash
# Build
docker build -t x4g-railway .

# Run
docker run -d \
  -e PANEL_USER=admin \
  -e PANEL_PASS=yourpass \
  -e DOMAIN=localhost \
  -p 8080:8080 \
  -p 443:443 \
  x4g-railway

# Access
open http://localhost:8080
```

---

## 📱 کلاینت‌های پیشنهادی

### Android
- [v2rayNG](https://github.com/2dust/v2rayNG)
- [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid)

### iOS
- [Streisand](https://apps.apple.com/us/app/streisand/id6450534064)
- [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118)

### Windows
- [Nekoray](https://github.com/MatsuriDayo/nekoray)
- [v2rayN](https://github.com/2dust/v2rayN)

### macOS
- [V2RayXS](https://github.com/tzmax/V2RayXS)
- [Streisand](https://apps.apple.com/us/app/streisand/id6450534064)

---

## ⚠️ عیب‌یابی

### مشکل ۱: Railway Health Check Fail
```
# مطمئن شوید railway.toml درست تنظیم شده
healthcheckPath = "/health"
healthcheckTimeout = 300
```

### مشکل ۲: Cloudflare Error 525/526
```
# در Cloudflare → SSL/TLS → Overview
# حالت را به Full (strict) تغییر دهید
```

### مشکل ۳: کانفیگ کار نمی‌کند
```
# 1. DOMAIN را بررسی کنید
# 2. UUID را در پنل چک کنید
# 3. Cloudflare Proxy را خاموش/روشن کنید
# 4. از WebSocket شروع کنید (پایدارترین)
```

### مشکل ۴: ربات تلگرام کار نمی‌کند
```
# 1. TELEGRAM_BOT_TOKEN را بررسی کنید
# 2. TELEGRAM_ADMIN_ID را بررسی کنید
# 3. Webhook را غیرفعال کنید (از polling استفاده می‌کنیم)
```

---

## 📄 لایسنس

MIT License - برای استفاده شخصی و آموزشی

---

## 🙏 سپاس

- [XTLS/Xray-core](https://github.com/XTLS/Xray-core)
- [Railway](https://railway.app)
- [Cloudflare](https://cloudflare.com)

---

<p align="center">
  <b>🚀 ساخته‌شده با ❤️ برای آزادی اینترنت در ایران</b>
</p>
