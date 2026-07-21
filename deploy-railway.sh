#!/bin/bash
# X4G Railway Deploy Helper

echo "🚀 X4G Railway Deploy Script"
echo "============================="

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login
echo "🔑 Logging into Railway..."
railway login

# Link project
echo "🔗 Linking to Railway project..."
railway link

# Set variables
echo "⚙️  Setting environment variables..."
railway variables set PANEL_USER=admin
railway variables set PANEL_PASS=$(openssl rand -base64 12)
railway variables set UUID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen)
railway variables set REALITY_ENABLED=true
railway variables set FRAGMENT_ENABLED=true

echo "✅ Variables set!"
echo ""
echo "📝 Next steps:"
echo "1. Go to Railway Dashboard → Settings → Domains"
echo "2. Generate a domain"
echo "3. Set DOMAIN variable to your generated domain"
echo "4. (Optional) Set TELEGRAM_BOT_TOKEN and TELEGRAM_ADMIN_ID"
echo "5. Redeploy"
