# Website Information Gathering Reference

## 1. Website Architecture Identification

### Tech Stack Inference Methods
1. **HTTP response headers** — Server, X-Powered-By, Set-Cookie features
2. **HTML source features** — meta generator, specific class/id naming
3. **JS file paths** — /static/js/app.js, /wp-content/, /assets/
4. **Cookie names** — PHPSESSID (PHP), JSESSIONID (Java), _rails_session (Rails)
5. **URL paths** — ?id= (PHP), /api/ (REST), /wp-admin/ (WordPress)

### Common Architecture Combinations
| Language | Framework | Database | Server | Signature |
|----------|-----------|----------|--------|-----------|
| PHP | Laravel | MySQL | Apache/Nginx | Set-Cookie: laravel_session |
| PHP | WordPress | MySQL | Apache | /wp-content/, /wp-admin/ |
| Python | Django | PostgreSQL | Nginx+Gunicorn | CSRF middleware cookie |
| Python | Flask | SQLite/MySQL | Nginx+uWSGI | Set-Cookie: session= |
| Java | Spring | MySQL/Oracle | Tomcat | JSESSIONID |
| Node.js | Express | MongoDB | Nginx | X-Powered-By: Express |
| Ruby | Rails | PostgreSQL | Nginx+Puma | _rails_session |

### python_execute Architecture Probing
```python
import requests

url = "https://target.com"
r = requests.get(url, timeout=10)

# 1. Response header analysis
headers = r.headers
print(f"Server: {headers.get('Server', 'N/A')}")
print(f"X-Powered-By: {headers.get('X-Powered-By', 'N/A')}")

# 2. Cookie analysis
cookies = r.cookies
for cookie in cookies:
    print(f"Cookie: {cookie.name} = {cookie.value[:20]}...")

# 3. HTML feature analysis
html = r.text
# WordPress
if 'wp-content' in html or 'wp-includes' in html:
    print("[+] WordPress detected")
# Laravel
if 'laravel_session' in str(cookies):
    print("[+] Laravel detected")
# Django
if 'csrftoken' in str(cookies) or 'csrfmiddlewaretoken' in html:
    print("[+] Django detected")
# Hexo
if 'hexo' in html.lower():
    print("[+] Hexo blog detected")
# Hugo
if 'hugo' in html.lower():
    print("[+] Hugo blog detected")
```

## 2. Web Fingerprinting

### CMS Fingerprint Signatures
| CMS | Signature Path | Signature String |
|-----|---------------|-----------------|
| WordPress | /wp-login.php, /wp-content/ | wp-content, xmlrpc.php |
| Joomla | /administrator/ | /media/jui/ |
| Drupal | /misc/drupal.js | Drupal.settings |
| Discuz | /forum.php | discuz_uid |
| Typecho | /admin/login.php | typecho |
| Hexo | /archives/ | hexo |
| Ghost | /ghost/ | ghost-frontend |

### Frontend Framework Signatures
| Framework | Signature |
|-----------|-----------|
| React | data-reactroot, __NEXT_DATA__ |
| Vue.js | data-v-xxx, __vue__ |
| Angular | ng-version, _nghost |
| jQuery | jQuery in scripts |
| Bootstrap | bootstrap.css/js |

### python_execute Fingerprinting
```python
import requests, re

url = "https://target.com"
r = requests.get(url, timeout=10)
html = r.text

# CMS detection
cms_signatures = {
    "WordPress": ["wp-content", "wp-includes", "wp-admin"],
    "Joomla": ["/administrator/", "media/jui"],
    "Drupal": ["Drupal.settings", "/misc/drupal"],
    "Hexo": ["hexo", "/archives/"],
    "Hugo": ["hugo", "gohugo"],
    "Ghost": ["ghost-frontend", "/ghost/"],
}

for cms, sigs in cms_signatures.items():
    if any(sig in html for sig in sigs):
        print(f"[+] CMS: {cms}")

# Frontend framework detection
fw_signatures = {
    "React": ["data-reactroot", "__NEXT_DATA__", "react"],
    "Vue.js": ["data-v-", "__vue__", "vue"],
    "Angular": ["ng-version", "_nghost", "angular"],
    "jQuery": ["jquery", "jQuery"],
    "Bootstrap": ["bootstrap"],
}

for fw, sigs in fw_signatures.items():
    if any(sig.lower() in html.lower() for sig in sigs):
        print(f"[+] Frontend framework: {fw}")

# JS file extraction
js_files = re.findall(r'src=["\']([^"\']*\.js[^"\']*)["\']', html)
print(f"JS files: {js_files[:10]}")
```

## 3. WAF Detection

### Common WAF Signatures
| WAF | Block Signature |
|-----|----------------|
| Cloudflare | Server: cloudflare, CF-Ray header |
| AWS WAF | Server: AmazonS3, x-amz-request-id |
| Alibaba Cloud WAF | Set-Cookie contains acw_tc |
| Tencent Cloud WAF | Specific block page |
| aaPanel WAF | Block page contains "aaPanel" |
| SafeDog | Block page contains "safedog" |
| ModSecurity | Specific 403 response |

### python_execute WAF Detection
```python
import requests

url = "https://target.com"

# 1. Normal request
r1 = requests.get(url)

# 2. Requests that trigger WAF
waf_payloads = [
    "/?id=1' OR 1=1--",
    "/?search=<script>alert(1)</script>",
    "/../../../etc/passwd",
    "/?file=php://filter/convert.base64-encode/resource=index",
]

for payload in waf_payloads:
    r2 = requests.get(url + payload, allow_redirects=False)
    # Status code change
    if r2.status_code in [403, 406, 429, 501]:
        print(f"[!] WAF detected: {payload} → {r2.status_code}")
    # Significant response length change
    if abs(len(r2.text) - len(r1.text)) > 500:
        print(f"[!] Response length change: normal={len(r1.text)}, attack={len(r2.text)}")

# 3. Check specific WAF response headers
waf_headers = {
    "cloudflare": ["cf-ray", "server: cloudflare"],
    "aws": ["x-amz-request-id", "x-amz-cf-id"],
    "alibaba-cloud": ["acw_tc"],
}
for waf_name, sigs in waf_headers.items():
    for sig in sigs:
        if sig in str(r1.headers).lower():
            print(f"[+] WAF detected: {waf_name}")
```

## 4. Sensitive Directories & Files

### Common Sensitive Paths
```
/robots.txt
/sitemap.xml
/.git/
/.svn/
/.env
/.DS_Store
/web.config
/config.php
/config.yml
/backup/
/admin/
/login/
/api/
/swagger/
/graphql
/phpinfo.php
/test/
/debug/
/console/
/actuator/
/.well-known/
```

### python_execute Directory Scan
```python
import requests

target = "https://target.com"
paths = [
    "/robots.txt", "/sitemap.xml", "/.git/", "/.env", "/.DS_Store",
    "/admin/", "/backup/", "/config.php", "/api/", "/phpinfo.php",
    "/.git/config", "/.git/HEAD", "/wp-config.php",
    "/swagger/", "/graphql", "/actuator/",
]

for path in paths:
    try:
        r = requests.get(target + path, timeout=5, allow_redirects=False)
        if r.status_code in [200, 301, 302, 401, 403]:
            print(f"[{r.status_code}] {path}")
    except:
        pass
```

## 5. Source Code Leak Detection

### Common Source Code Leak Types
| Type | Path | Detection Method |
|------|------|-----------------|
| Git repository | /.git/config, /.git/HEAD | 200 with git content |
| SVN repository | /.svn/entries | 200 with svn content |
| .DS_Store | /.DS_Store | Download and parse |
| .env file | /.env | Contains DB_PASSWORD etc. |
| web.config | /web.config | IIS config |
| Backup files | /.bak, /.swp, /.old, /~ | Direct download |
| Docker | /Dockerfile, /docker-compose.yml | Container config |
| package.json | /package.json | Node.js dependencies |
| composer.json | /composer.json | PHP dependencies |

### Git Repository Leak Exploitation
```python
import requests

target = "https://target.com"

# 1. Check .git/HEAD
r = requests.get(f"{target}/.git/HEAD")
if r.status_code == 200 and "ref:" in r.text:
    print("[!] Git repository leak detected!")
    # 2. Try to get the ref
    ref_path = r.text.strip().split("ref: ")[1] if "ref: " in r.text else ""
    if ref_path:
        r2 = requests.get(f"{target}/.git/{ref_path}")
        if r2.status_code == 200:
            print(f"[+] Git ref: {r2.text.strip()}")

# 3. Try to get config
r3 = requests.get(f"{target}/.git/config")
if r3.status_code == 200:
    print(f"[+] Git config:\n{r3.text}")
```

## 6. Related Site Lookup (Reverse IP to Domain)

### Lookup Methods
1. **Webmaster Tools** — https://stool.chinaz.com/same
2. **ThreatBook** — https://x.threatbook.cn
3. **crt.sh** — query certificate-associated domains by IP
4. **Censys** — https://search.censys.io

### python_execute Related Site Lookup
```python
import requests, json

ip = "1.2.3.4"

# Method 1: crt.sh query for certs on same IP
r = requests.get(f"https://crt.sh/?q={ip}&output=json", timeout=15)
if r.status_code == 200:
    domains = set()
    for entry in r.json():
        for name in entry.get('name_value', '').split('\n'):
            if name.strip() and '*' not in name:
                domains.add(name.strip())
    print(f"[+] Domains on same IP ({len(domains)}):")
    for d in sorted(domains):
        print(f"  - {d}")
```

## 7. C-Segment Scan (Live Hosts on Same Subnet)

### python_execute C-Segment Scan
```python
import requests, socket
from concurrent.futures import ThreadPoolExecutor

# Get IP from domain
domain = "target.com"
ip = socket.gethostbyname(domain)
# Extract C-segment
c_segment = ".".join(ip.split(".")[:3])

def check_host(ip, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, 80))
        s.close()
        if result == 0:
            return ip
    except:
        pass
    return None

# Scan C-segment (1-254)
alive_hosts = []
with ThreadPoolExecutor(max_workers=50) as executor:
    ips = [f"{c_segment}.{i}" for i in range(1, 255)]
    results = executor.map(check_host, ips)
    alive_hosts = [ip for ip in results if ip]

print(f"[+] Live hosts in C-segment: {alive_hosts}")
```
