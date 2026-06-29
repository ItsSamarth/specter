---
name: osint-recon
description: OSINT open-source intelligence knowledge base — four-dimensional information gathering model (server → website → domain → personnel); dimension four (personnel) is conditionally triggered
---

# OSINT Open-Source Intelligence Knowledge Base

A practical knowledge base for information gathering, reconnaissance, and social engineering scenarios. Provides the **four-dimensional information gathering model** (server info → website info → domain info → personnel info), along with specific tool usage methods and data extraction techniques.

**Difference from the `recon` Skill**:
- `recon` → technical-level reconnaissance (port scanning, DNS, directory enumeration) — basic version
- `osint-recon` → full-dimension reconnaissance (server + website + domain + personnel/social engineering) — deep version

## Core Principles

1. **Full four-dimension coverage** — server/website/domain dimensions always executed; personnel dimension conditionally triggered
2. **Extract everything extractable from pages** — not just HTTP headers; also check HTML content, JS files, and comments
3. **Passive before active** — first check response headers, DNS, WHOIS (passive), then do port scanning/directory enumeration (active)
4. **Dimension completeness self-check** — each round check which dimensions are complete ✅ and which are not ❌; only allow [DONE] when all are complete
5. **External links are leads** — every external link on a page is a potential intelligence source
6. **Structured output** — consolidate all findings into a Markdown report

## Four-Dimensional Information Gathering Model

### Dimension 1: Server Information
| Check Item | Tool/Method | Notes |
|------------|-------------|-------|
| Open ports & service versions | MCP nmap / `python_execute` + socket | Full port scan or common ports (21/22/80/443/3306/6379/8080/8443) |
| Real IP detection | DNS history / global ping / email header extraction | Origin IP behind CDN — SecurityTrails/DNSHistory/global ping |
| OS fingerprinting | TTL inference + nmap OS detection | Linux TTL≈64, Windows TTL≈128, Unix TTL≈255 |
| Middleware version | Response header Server + error pages + signature files | Apache/Nginx/IIS/Tomcat version identification |
| Database identification | Port probing + error messages + characteristic behavior | MySQL(3306)/Redis(6379)/MongoDB(27017)/MSSQL(1433) |

### Dimension 2: Website Information
| Check Item | Tool/Method | Notes |
|------------|-------------|-------|
| Website architecture | Response headers + page features + JS libraries | OS + middleware + database + language + framework → complete tech stack |
| Web fingerprinting | `fetch` + response feature matching | CMS type, frontend framework, JS libraries, template engine |
| WAF detection | wafw00f logic + response features | Interception pages / special response headers / abnormal status codes |
| Sensitive directories & files | `python_execute` + common path wordlists | /admin /backup /config /api /robots.txt /sitemap.xml |
| Source code leaks | Check common leak paths | .git/.svn/.DS_Store/.env/web.config/backup files (.bak/.swp/.old) |
| Related site lookup | Reverse lookup domains on same IP | Webmaster tools / ThreatBook / crt.sh same-IP query |
| C-segment scan | Live host scan on same subnet | nmap -sn scan /24 subnet |

### Dimension 3: Domain Information
| Check Item | Tool/Method | Notes |
|------------|-------------|-------|
| WHOIS registration info | `python_execute` + whois API/command | Registrant / registrar / NS servers / registration date / expiration date |
| ICP filing info | MIIT filing query API | Only needed for mainland China domains; overseas domains have no ICP filing |
| Subdomain discovery | crt.sh + brute force + search engines + DNS zone transfer | Multi-method cross-validation for comprehensive coverage |
| Full DNS records | `python_execute` + dnspython/socket | A/CNAME/MX/TXT/NS/SPF/SOA full query |
| Certificate transparency logs | crt.sh / Censys / certspotter | Discover historical certificates, subdomains, related domains |

### Dimension 4: Personnel Information ⚡ Conditionally Triggered
**⚠️ This dimension is only executed when at least one of the following conditions is met:**
- The user's command explicitly mentions "social engineering / social recon / personnel info / author tracking / personal profile" etc.
- The target website has explicit author information (meta author, about page, contact info)

**When NOT to do social engineering**: ordinary corporate website with no individual authors / user only requests "scan the target" / target is an IP/internal address

| Tracking Direction | Method | Notes |
|--------------------|--------|-------|
| Author identifier extraction | Page meta author, about page | Username, nickname, email |
| GitHub tracking | `fetch` + GitHub API | Repos, language preferences, contribution history, email |
| Social media | Extract links from page → visit | Bilibili, Weibo, Zhihu, Twitter, LinkedIn |
| Cross-platform correlation | Search other platforms by username/email | Same ID cross-platform search |
| Historical commits | GitHub commits → commit email | Associate other projects and identities |
| Leak detection | GitHub historical code search | .env, config, key leaks |

## First-Pass Workflow

1. **Visit target** → `fetch` home page, extract HTTP headers + HTML content
2. **Dimension 1: Server info** → port scan, real IP, OS fingerprint, middleware/database identification
3. **Dimension 2: Website info** → web fingerprint, WAF detection, sensitive dirs/source leaks, related sites/C-segment
4. **Dimension 3: Domain info** → WHOIS, ICP filing, subdomains, DNS records, certificate transparency
5. **Dimension 4 (conditionally triggered)** → extract author info, cross-platform tracking, info summary
6. **Dimension completeness self-check** → confirm each dimension has been checked at least once
7. **Summary report** → generate Markdown-format recon report

## Scene Routing

| Scene | Reference Doc | Core Content |
|-------|--------------|--------------|
| Server information gathering | `server-recon.md` | Port scanning, real IP, OS fingerprint, middleware/database identification |
| Website information gathering | `website-recon.md` | Architecture/fingerprint/WAF/sensitive dirs/source leaks/related sites/C-segment |
| Web fingerprinting | `web-fingerprinting.md` | Framework detection, version identification, tech stack inference |
| Author tracking | `author-tracking.md` | Extract author from page → cross-platform tracking → info summary |
| OSINT tool usage | `osint-toolkit.md` | crt.sh, GitHub API, search engine dorks, related sites/C-segment/ICP |
| Social engineering intel summary | `social-engineering-intel.md` | Personal profile, relationship network, information cross-validation |
| Recon report template | `recon-report-template.md` | Standard Markdown report format (four dimensions) |

## ⭐ Common Extraction Code Snippets

### Extract all external links from HTML
```python
import re
html = "..."  # HTML fetched from target
links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
for link in set(links):
    print(link)
```

### Extract author info from HTML
```python
import re
# meta author
author = re.findall(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', html)
# about page links
about_links = re.findall(r'href=["\']([^"\']*(?:about|me|contact)[^"\']*)["\']', html, re.I)
```

### Query crt.sh for subdomains
```python
import requests
domain = "example.com"
r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json")
if r.status_code == 200:
    for entry in r.json():
        print(entry['name_value'])
```

### GitHub user information
```python
import requests
username = "target_user"
r = requests.get(f"https://api.github.com/users/{username}")
if r.status_code == 200:
    data = r.json()
    print(f"Name: {data.get('name')}")
    print(f"Bio: {data.get('bio')}")
    print(f"Email: {data.get('email')}")
    print(f"Blog: {data.get('blog')}")
    print(f"Location: {data.get('location')}")
    print(f"Company: {data.get('company')}")
```

### WAF detection (response feature method)
```python
import requests
url = "https://target.com"
# Normal request
r1 = requests.get(url)
# Request that triggers WAF (with attack signature)
r2 = requests.get(url + "/?id=1' OR 1=1--")
# Compare responses
if r1.status_code != r2.status_code or len(r1.text) != len(r2.text):
    print("[!] WAF may be present")
    print(f"Normal status: {r1.status_code}, Attack status: {r2.status_code}")
```

### Related site lookup (reverse lookup by IP)
```python
import requests
ip = "1.2.3.4"
# Use chinaz API or other reverse lookup interfaces
# Can also query certificates on the same IP via crt.sh
r = requests.get(f"https://crt.sh/?q={ip}&output=json")
```
