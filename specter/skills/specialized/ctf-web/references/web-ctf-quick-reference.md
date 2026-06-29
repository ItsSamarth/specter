# CTF Web Quick Reference

## Common Flag Locations

### Linux
```
/flag
/flag.txt
/flag.php
/var/www/html/flag.php
/home/ctf/flag
/root/flag
/tmp/flag
/opt/flag
/srv/flag
```

### Docker / Environment Variables
```
/proc/self/environ
/environment
/.env
```

### PHP-Specific
```php
// flag in phpinfo()
// check environment variable section
// check custom section

// Common flag filenames
flag.php
flag.txt
f1ag.php
fl4g.php
fl@g.php
th1s_1s_flag.php
```

## First-Pass Workflow

```
1. Visit target URL
   → View page source (Ctrl+U)
   → Check HTTP headers (Server, X-Powered-By, Set-Cookie)
   → Check Cookie values (base64/JWT/serialized)

2. Check hidden information
   → robots.txt
   → .git/HEAD
   → .svn/
   → Backup files: index.php.bak, www.zip, .index.php.swp, index.php~
   → DS_Store: .DS_Store

3. Directory scan
   → /flag, /admin, /login, /upload, /api, /debug
   → /phpinfo.php, /info.php, /test.php
   → /console (Flask Debug), /actuator (Spring Boot)

4. If source available → code audit
   → See php-code-audit-checklist.md

5. If no source → active probing
   → SQL injection testing
   → XSS testing
   → File upload
   → SSTI testing
   → LFI/RFI
```

## Quick Test Commands

```bash
# Check basic info
curl -I http://target/              # HTTP headers
curl http://target/robots.txt        # robots
curl http://target/.git/HEAD         # git leak

# Common injection tests
' OR 1=1 --                          # SQLi
{{7*7}}                              # SSTI
<script>alert(1)</script>            # XSS
../../../etc/passwd                  # LFI
```

## Common Response Header Hints

| Header | Meaning | Next step |
|--------|---------|-----------|
| `X-Forwarded-For: 127.0.0.1` | Requires local access | Add X-Forwarded-For header |
| `Server: nginx/1.x` | Server type | Search known CVEs |
| `X-Powered-By: PHP/7.x` | PHP version | PHP-specific vulnerabilities |
| `Set-Cookie: role=guest` | Privilege control | Modify Cookie |
| `Hint: xxx` | Direct hint | Follow the hint |
| `Flag: xxx` | Sometimes directly in header | Check all response headers |

## Common Chain Shapes

### PHP Simple Chain
```
URL → source code → find filter → bypass filter → RCE → read flag
```

### PHP Multi-Step Chain
```
Entry page → find hint → follow redirect → find new page → get source → analyze & exploit → RCE
```

### File Inclusion Chain
```
LFI → read source (php://filter) → find include point → log poisoning/session inclusion → RCE
```

### SQL Injection Chain
```
Login form → SQLi → read data → find admin password → login admin panel → upload webshell → RCE
```

### Deserialization Chain
```
Controllable serialized data → analyze available gadgets → construct exploit chain → RCE/SSRF/file read
```

## Encoding/Encryption Common Clues

| Characteristic | Likely encoding | Decode method |
|----------------|----------------|---------------|
| Ends with `=` | Base64 | `crypto_decode base64_decode` |
| `0-9a-f` even length | Hex | `crypto_decode hex_decode` |
| `%XX` | URL encoding | `crypto_decode url_decode` |
| `&#xNN;` | HTML entity | `crypto_decode html_decode` |
| `\uXXXX` | Unicode escape | `crypto_decode unicode_decode` |
| Three `.`-separated sections | JWT | `crypto_decode jwt_decode` |
| Dots and dashes | Morse | `crypto_decode morse_decode` |
| Looks like letters but unreadable | ROT13/Caesar | `crypto_decode rot13_decode` |
