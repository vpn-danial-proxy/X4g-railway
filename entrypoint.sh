#!/bin/bash
set -e

echo "🚀 X4G Railway - Iran Optimized Starting..."

# Generate UUID if not set
if [ "$UUID" = "auto" ] || [ -z "$UUID" ]; then
    export UUID=$(cat /proc/sys/kernel/random/uuid)
    echo "✅ Generated UUID: $UUID"
fi

# Generate keys for Reality if enabled
if [ "$REALITY_ENABLED" = "true" ]; then
    echo "🔑 Generating Reality keys..."
    REALITY_KEYS=$(xray x25519)
    export REALITY_PRIVATE=$(echo "$REALITY_KEYS" | grep "Private" | awk '{print $3}')
    export REALITY_PUBLIC=$(echo "$REALITY_KEYS" | grep "Public" | awk '{print $3}')
    echo "✅ Reality Public Key: $REALITY_PUBLIC"
fi

# Generate short ID for Reality
export REALITY_SHORTID=$(openssl rand -hex 4 2>/dev/null || xxd -l 4 -p /dev/urandom)

# Set domain
if [ "$DOMAIN" = "auto" ] || [ -z "$DOMAIN" ]; then
    export DOMAIN=$(hostname -I | awk '{print $1}')
    echo "⚠️  No domain set, using IP: $DOMAIN"
fi

# Generate Xray config from template
envsubst < xray_config.json > /usr/local/etc/xray/config.json

echo "📋 Xray Config Generated"
head -60 /usr/local/etc/xray/config.json

# Start Supervisor (manages Xray + Flask + Nginx)
echo "🎛️  Starting services via Supervisor..."
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
