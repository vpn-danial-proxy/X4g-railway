import os
import json
import base64
import uuid
import qrcode
import io
import psutil
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, send_file
import bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32).hex())

# Config
PANEL_USER = os.environ.get('PANEL_USER', 'admin')
PANEL_PASS_HASH = bcrypt.hashpw(
    os.environ.get('PANEL_PASS', 'x4g2026').encode(),
    bcrypt.gensalt()
)
UUID = os.environ.get('UUID', str(uuid.uuid4()))
DOMAIN = os.environ.get('DOMAIN', 'localhost')
REALITY_PUBLIC = os.environ.get('REALITY_PUBLIC', '')
REALITY_SHORTID = os.environ.get('REALITY_SHORTID', '')
CDN_MODE = os.environ.get('CDN_MODE', 'cloudflare')
PORT = int(os.environ.get('PORT', 8080))

# In-memory user storage (use Redis/DB in production)
users = {}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_server_stats():
    return {
        'cpu': psutil.cpu_percent(interval=0.5),
        'ram': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'uptime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def generate_vless_link(protocol, port, path='', flow=''):
    """Generate VLESS link for different protocols"""
    if protocol == 'ws':
        # VLESS + WS (CDN compatible)
        params = {
            'type': 'ws',
            'path': path or '/ws',
            'host': DOMAIN,
            'security': 'tls',
            'sni': DOMAIN,
            'fp': 'chrome',
            'alpn': 'h2,http/1.1',
            'allowInsecure': '0'
        }
        link = f"vless://{UUID}@{DOMAIN}:{port}?"
        link += '&'.join([f"{k}={v}" for k, v in params.items()])
        link += f"#{protocol.upper()}_X4G"
        return link

    elif protocol == 'xhttp':
        # VLESS + XHTTP (Split mode)
        params = {
            'type': 'xhttp',
            'path': path or '/xhttp',
            'host': DOMAIN,
            'mode': 'auto',
            'security': 'tls',
            'sni': DOMAIN,
            'fp': 'chrome',
            'alpn': 'h2,http/1.1'
        }
        link = f"vless://{UUID}@{DOMAIN}:{port}?"
        link += '&'.join([f"{k}={v}" for k, v in params.items()])
        link += f"#{protocol.upper()}_X4G"
        return link

    elif protocol == 'reality':
        # VLESS + Reality (Direct)
        params = {
            'type': 'tcp',
            'security': 'reality',
            'flow': flow or 'xtls-rprx-vision',
            'sni': 'www.google.com',
            'fp': 'chrome',
            'pbk': REALITY_PUBLIC,
            'sid': REALITY_SHORTID,
            'spx': '/'
        }
        link = f"vless://{UUID}@{DOMAIN}:{port}?"
        link += '&'.join([f"{k}={v}" for k, v in params.items()])
        link += f"#REALITY_X4G"
        return link

    return ""

def generate_all_configs():
    """Generate all config variants"""
    return {
        'vless_ws': {
            'name': 'VLESS + WebSocket (CDN)',
            'description': 'بهترین برای ایران - از CDN استفاده کنید',
            'link': generate_vless_link('ws', 443, '/ws'),
            'port': 443,
            'path': '/ws',
            'protocol': 'ws'
        },
        'vless_xhttp': {
            'name': 'VLESS + XHTTP (Split)',
            'description': 'سرعت بالا با Split Mode',
            'link': generate_vless_link('xhttp', 443, '/xhttp'),
            'port': 443,
            'path': '/xhttp',
            'protocol': 'xhttp'
        },
        'vless_reality': {
            'name': 'VLESS + Reality (Direct)',
            'description': 'مستقیم - پینگ پایین‌تر',
            'link': generate_vless_link('reality', 443),
            'port': 443,
            'protocol': 'reality'
        }
    }

def generate_qr_code(data):
    """Generate QR code image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'X4G-Railway'})

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    configs = generate_all_configs()
    stats = get_server_stats()
    return render_template('index.html', configs=configs, stats=stats, domain=DOMAIN, uuid=UUID)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == PANEL_USER and bcrypt.checkpw(password.encode(), PANEL_PASS_HASH):
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/configs')
@login_required
def api_configs():
    return jsonify(generate_all_configs())

@app.route('/api/stats')
@login_required
def api_stats():
    return jsonify(get_server_stats())

@app.route('/qr/<config_type>')
@login_required
def qr_code(config_type):
    configs = generate_all_configs()
    if config_type not in configs:
        return "Config not found", 404
    img_io = generate_qr_code(configs[config_type]['link'])
    return send_file(img_io, mimetype='image/png')

@app.route('/sub/<token>')
def subscription(token):
    """Subscription endpoint for clients"""
    if token != UUID[:8]:  # Simple token check
        return "Unauthorized", 401

    configs = generate_all_configs()
    # Generate Base64 subscription
    links = [c['link'] for c in configs.values()]
    sub_content = base64.b64encode('\n'.join(links).encode()).decode()
    return Response(sub_content, mimetype='text/plain')

@app.route('/sub/clash/<token>')
def subscription_clash(token):
    """Clash format subscription"""
    if token != UUID[:8]:
        return "Unauthorized", 401

    configs = generate_all_configs()
    clash_config = generate_clash_config(configs)
    return Response(clash_config, mimetype='text/yaml')

def generate_clash_config(configs):
    """Generate Clash YAML config"""
    yaml = """mixed-port: 7890
allow-lan: true
bind-address: '*'
mode: rule
log-level: info
external-controller: 127.0.0.1:9090
dns:
  enabled: true
  nameserver:
    - 1.1.1.1
    - 8.8.8.8
proxies:
"""
    for key, cfg in configs.items():
        if cfg['protocol'] == 'ws':
            yaml += f"""
  - name: "{cfg['name']}"
    type: vless
    server: {DOMAIN}
    port: {cfg['port']}
    uuid: {UUID}
    network: ws
    tls: true
    servername: {DOMAIN}
    ws-opts:
      path: "{cfg['path']}"
      headers:
        Host: {DOMAIN}
"""
        elif cfg['protocol'] == 'reality':
            yaml += f"""
  - name: "{cfg['name']}"
    type: vless
    server: {DOMAIN}
    port: {cfg['port']}
    uuid: {UUID}
    network: tcp
    tls: true
    servername: www.google.com
    flow: xtls-rprx-vision
    reality-opts:
      public-key: {REALITY_PUBLIC}
      short-id: {REALITY_SHORTID}
"""

    yaml += """
proxy-groups:
  - name: "X4G-Auto"
    type: url-test
    proxies:
      - VLESS + WebSocket (CDN)
      - VLESS + XHTTP (Split)
      - VLESS + Reality (Direct)
    url: http://www.gstatic.com/generate_204
    interval: 300

rules:
  - GEOIP,IR,DIRECT
  - GEOIP,CN,DIRECT
  - MATCH,X4G-Auto
"""
    return yaml

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
