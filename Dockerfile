# X4G Railway Optimized - Iran Edition
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     curl wget unzip ca-certificates nginx supervisor     && rm -rf /var/lib/apt/lists/*

# Install Xray-core (latest stable)
RUN bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

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

# Environment defaults
ENV PORT=8080
ENV XRAY_PORT=443
ENV WEB_PORT=8080
ENV PANEL_USER=admin
ENV PANEL_PASS=x4g2026
ENV UUID=auto
ENV DOMAIN=auto
ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_ADMIN_ID=""
ENV CDN_MODE=cloudflare
ENV REALITY_ENABLED=true
ENV FRAGMENT_ENABLED=true

EXPOSE 8080 443 80

ENTRYPOINT ["./entrypoint.sh"]
