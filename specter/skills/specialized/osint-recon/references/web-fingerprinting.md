# Web Fingerprinting

## Checklist

### HTTP Response Header Fingerprints
| Response header | Inferred information | Example |
|--------|---------|------|
| `Server` | Web server | `nginx/1.18.0`, `Apache/2.4.41`, `GitHub.com` |
| `X-Powered-By` | Backend language/framework | `PHP/7.4.3`, `Express`, `Next.js` |
| `X-AspNet-Version` | .NET version | `4.0.30319` |
| `Set-Cookie` | Framework signature | `PHPSESSID`→PHP, `JSESSIONID`→Java, `csrf_token`→Django |
| `X-Generator` | CMS | `Hugo`, `WordPress`, `Ghost` |
| `X-DRupal-Cache` | CMS | Drupal |
| `Via` | Proxy/CDN | `1.1 varnish`→Varnish CDN |

### HTML Source Fingerprints
```python
import re

# WordPress
wp_signs = ['wp-content', 'wp-includes', 'wordpress']
# Hexo
hexo_signs = ['hexo', 'hexo-theme']
# Hugo
hugo_signs = ['hugo', 'gohugo']
# Jekyll
jekyll_signs = ['jekyll']
# Next.js
next_signs = ['__NEXT_DATA__', '_next/']
# Vue
vue_signs = ['data-v-', '__vue__']
# React
react_signs = ['data-reactroot', '__react']

def detect_framework(html):
    html_lower = html.lower()
    frameworks = []
    checks = {
        'WordPress': wp_signs,
        'Hexo': hexo_signs,
        'Hugo': hugo_signs,
        'Jekyll': jekyll_signs,
        'Next.js': next_signs,
        'Vue': vue_signs,
        'React': react_signs,
    }
    for name, signs in checks.items():
        if any(s in html_lower for s in signs):
            frameworks.append(name)
    return frameworks
```

### JavaScript File Fingerprints
- Framework-specific JS file paths: `/wp-includes/js/` → WordPress
- Vue/React DevTools detection: `__VUE_DEVTOOLS_GLOBAL_HOOK__`, `__REACT_DEVTOOLS_GLOBAL_HOOK__`
- Framework version is usually in JS comments or variables

### CSS Fingerprints
- `/wp-content/themes/` → WordPress
- Hexo theme-specific class names
- Bootstrap/Tailwind class signatures

### Signature Files
| File path | Inferred information |
|---------|---------|
| `/robots.txt` | CMS information, hidden paths |
| `/sitemap.xml` | Site structure |
| `/favicon.ico` | Framework default icon |
| `/.well-known/security.txt` | Security contact |
| `/humans.txt` | Developer information |
| `/.git/HEAD` | Git repository leak |
| `/.env` | Environment variable leak |

## GitHub Pages Signatures
- Response header `Server: GitHub.com`
- `X-GitHub-Request-Id` present
- `X-Cache: HIT` + `X-Fastly-Request-ID` → Fastly CDN
- `Via: 1.1 varnish` → Varnish cache
- Common frameworks: Jekyll, Hexo, Hugo

---

## WAF Detection

### Common WAF Identification Signatures
| WAF | Response header/page signature | Block status code |
|-----|----------------|-----------|
| Cloudflare | `Server: cloudflare`, `CF-Ray` | 403 |
| AWS WAF | `x-amz-request-id`, `x-amz-cf-id` | 403 |
| Alibaba Cloud WAF | Cookie contains `acw_tc` | 405/403 |
| Tencent Cloud WAF | Specific JSON block page | 403 |
| aaPanel WAF | Block page contains "宝塔" | 403 |
| SafeDog | Block page contains "safedog" | 403/404 |
| ModSecurity | Specific 403 + Server header | 403 |
| Nginx WAF | `HTTP/1.1 444` or special 403 | 444/403 |

### WAF Detection Methods
1. **Normal request vs attack request comparison** — send a request with attack signatures and observe response differences
2. **Response header inspection** — some WAFs add specific response headers
3. **Cookie inspection** — some WAFs set tracking cookies
4. **Status code anomalies** — attack requests return abnormal status codes (403/406/429/444)

### Common WAF Bypass Trigger Payloads
```
/?id=1' OR 1=1--
/?search=<script>alert(1)</script>
/../../../etc/passwd
/?file=php://filter/convert.base64-encode/resource=index
```

---

## 源码泄露检查

### 常见源码泄露类型与检测
| 类型 | 路径 | 检测方法 | 危害等级 |
|------|------|---------|---------|
| Git 仓库 | `/.git/config`, `/.git/HEAD` | 200 且含 git 内容 | 🔴 Critical |
| SVN 仓库 | `/.svn/entries` | 200 且含 svn 内容 | 🔴 Critical |
| .DS_Store | `/.DS_Store` | 下载后解析目录结构 | 🟡 Medium |
| .env 文件 | `/.env` | 含 DB_PASSWORD 等 | 🔴 Critical |
| web.config | `/web.config` | IIS 配置泄露 | 🟡 Medium |
| 备份文件 | `/.bak`, `/.swp`, `/.old`, `/.tar.gz` | 直接下载 | 🟡 Medium |
| Docker | `/Dockerfile`, `/docker-compose.yml` | 容器配置 | 🟡 Medium |
| package.json | `/package.json` | Node.js 依赖 | 🟢 Low |
| composer.json | `/composer.json` | PHP 依赖 | 🟢 Low |
| webpack | `/webpack.json`, `/map Files` | 源码映射 | 🟡 Medium |

### Git 泄露利用流程
1. 访问 `/.git/HEAD` → 获取 ref 路径
2. 访问 `/.git/config` → 获取远程仓库信息
3. 访问 `/.git/objects/` → 遍历 Git 对象
4. 使用 GitHack/scrabble 工具自动恢复源码

### 敏感文件扫描路径列表
```
/.git/config
/.git/HEAD
/.svn/entries
/.DS_Store
/.env
/.env.bak
/.env.local
/web.config
/config.php
/config.yml
/backup.sql
/database.sql
/db.sql
/phpinfo.php
/test/
/debug/
/console/
/admin/
/wp-config.php
/robots.txt
/sitemap.xml
/.well-known/security.txt
```
