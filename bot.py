import os
import asyncio
import base64
import qrcode
import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

# Config
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
ADMIN_ID = os.environ.get('TELEGRAM_ADMIN_ID', '')
UUID = os.environ.get('UUID', '')
DOMAIN = os.environ.get('DOMAIN', 'localhost')
REALITY_PUBLIC = os.environ.get('REALITY_PUBLIC', '')
REALITY_SHORTID = os.environ.get('REALITY_SHORTID', '')

def is_admin(user_id: int) -> bool:
    if not ADMIN_ID:
        return True
    return str(user_id) == ADMIN_ID

def generate_vless_link(protocol):
    if protocol == 'ws':
        params = f"type=ws&path=/ws&host={DOMAIN}&security=tls&sni={DOMAIN}&fp=chrome&alpn=h2,http/1.1"
        return f"vless://{UUID}@{DOMAIN}:443?{params}#WS_X4G"
    elif protocol == 'xhttp':
        params = f"type=xhttp&path=/xhttp&host={DOMAIN}&mode=auto&security=tls&sni={DOMAIN}&fp=chrome"
        return f"vless://{UUID}@{DOMAIN}:443?{params}#XHTTP_X4G"
    elif protocol == 'reality':
        params = f"type=tcp&security=reality&flow=xtls-rprx-vision&sni=www.google.com&fp=chrome&pbk={REALITY_PUBLIC}&sid={REALITY_SHORTID}&spx=/"
        return f"vless://{UUID}@{DOMAIN}:443?{params}#REALITY_X4G"
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("⛔ شما دسترسی ندارید.")
        return

    keyboard = [
        [InlineKeyboardButton("🔗 دریافت کانفیگ WS", callback_data='config_ws')],
        [InlineKeyboardButton("🔗 دریافت کانفیگ XHTTP", callback_data='config_xhttp')],
        [InlineKeyboardButton("🔗 دریافت کانفیگ Reality", callback_data='config_reality')],
        [InlineKeyboardButton("📊 وضعیت سرور", callback_data='status')],
        [InlineKeyboardButton("📋 همه کانفیگ‌ها", callback_data='all_configs')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome = f"""🚀 <b>X4G Railway Panel</b>

👋 سلام {user.first_name}!

🔰 <b>دامنه:</b> <code>{DOMAIN}</code>
🔰 <b>UUID:</b> <code>{UUID}</code>

✅ از دکمه‌های زیر استفاده کنید:"""

    await update.message.reply_text(welcome, reply_markup=reply_markup, parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.edit_message_text("⛔ شما دسترسی ندارید.")
        return

    data = query.data

    if data.startswith('config_'):
        protocol = data.replace('config_', '')
        link = generate_vless_link(protocol)

        # Generate QR
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        caption = f"""✅ <b>کانفیگ {protocol.upper()}</b>

<code>{link}</code>

📋 برای کپی روی لینک کلیک کنید."""

        await query.message.reply_photo(photo=img_io, caption=caption, parse_mode='HTML')

    elif data == 'all_configs':
        text = "📋 <b>همه کانفیگ‌ها:</b>

"
        for proto in ['ws', 'xhttp', 'reality']:
            link = generate_vless_link(proto)
            text += f"<b>{proto.upper()}:</b>
<code>{link}</code>

"

        # Subscription link
        sub_link = f"https://{DOMAIN}/sub/{UUID[:8]}"
        text += f"🔗 <b>لینک سابسکریپشن:</b>
<code>{sub_link}</code>"

        await query.edit_message_text(text, parse_mode='HTML')

    elif data == 'status':
        try:
            r = requests.get('http://127.0.0.1:5000/api/stats', timeout=5)
            stats = r.json()
            text = f"""📊 <b>وضعیت سرور:</b>

🖥️ CPU: {stats.get('cpu', 'N/A')}%
💾 RAM: {stats.get('ram', 'N/A')}%
💿 Disk: {stats.get('disk', 'N/A')}%
⏰ Uptime: {stats.get('uptime', 'N/A')}"""
        except:
            text = "❌ خطا در دریافت وضعیت سرور"

        await query.edit_message_text(text, parse_mode='HTML')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    help_text = """🤖 <b>راهنمای ربات X4G:</b>

/start - شروع و منوی اصلی
/help - این راهنما
/status - وضعیت سرور
/config - دریافت کانفیگ‌ها

🔗 <b>لینک پنل:</b>
https://DOMAIN

⚠️ توکن ربات را در متغیر TELEGRAM_BOT_TOKEN تنظیم کنید.""".replace('DOMAIN', DOMAIN)

    await update.message.reply_text(help_text, parse_mode='HTML')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    try:
        r = requests.get('http://127.0.0.1:5000/api/stats', timeout=5)
        stats = r.json()
        text = f"""📊 <b>وضعیت سرور X4G:</b>

🖥️ CPU: {stats.get('cpu', 'N/A')}%
💾 RAM: {stats.get('ram', 'N/A')}%
💿 Disk: {stats.get('disk', 'N/A')}%
⏰ Update: {stats.get('uptime', 'N/A')}"""
    except Exception as e:
        text = f"❌ خطا: {str(e)}"

    await update.message.reply_text(text, parse_mode='HTML')

def main():
    if not BOT_TOKEN:
        print("⚠️  TELEGRAM_BOT_TOKEN not set. Bot will not start.")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Telegram Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
