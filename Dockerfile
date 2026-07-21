# X4G Railway Optimized - Iran Edition
FROM python:3.11-slim

# Install system dependencies (no systemd needed)
RUN apt-get update && apt-get install -y --no-install-recommends     curl wget unzip ca-certificates nginx supervisor     && rm -rf /var/lib/apt/lists/*

# Install Xray-core manually (bypass systemd check)
ARG XRAY_VERSION=v25.6.30
RUN mkdir -p /usr/local/share/xray /usr/local/etc/xray /var/log/xray &&     ARCH=$(dpkg --print-architecture) &&     case "$ARCH" in         amd64) XRAY_ARCH="64" ;;         arm64) XRAY_ARCH="arm64-v8a" ;;         *) echo "Unsupported arch: $ARCH" && exit 1 ;;     esac &&     wget -qO /tmp/xray.zip "https://github.com/XTLS/Xray-core/releases/download/${XRAY_VERSION}/Xray-linux-${XRAY_ARCH}.zip" &&     unzip -q /tmp/xray.zip -d /usr/local/bin/ &&     chmod +x /usr/local/bin/xray &&     rm /tmp/xray.zip &&     xray version

# Set working directory
WORKDIR /app

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Make scripts executable
RUN chmod +x entrypoint.sh

# Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Environment defaults (NO sensitive tokens here!)
ENV PORT=8080
ENV XRAY_PORT=443
ENV WEB_PORT=8080
ENV PANEL_USER=admin
ENV PANEL_PASS=danial905749
ENV UUID=auto
ENV DOMAIN=auto
ENV CDN_MODE=cloudflare
ENV REALITY_ENABLED=true
ENV FRAGMENT_ENABLED=true

EXPOSE 8080 443 80

ENTRYPOINT ["./entrypoint.sh"]
