# Server Information Gathering Reference

## 1. Open Ports & Service Version Identification

### Common nmap commands
```bash
# Full port scan (slow but comprehensive)
nmap -p- -sV <target>

# Quick scan of common ports
nmap -sV -top-ports 1000 <target>

# UDP port scan
nmap -sU --top-ports 100 <target>

# Service version identification + OS detection
nmap -sV -O <target>
```

### python_execute method (when nmap is unavailable)
```python
import socket

def scan_port(host, port, timeout=2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

host = "target.com"
common_ports = [21,22,23,25,53,80,110,143,443,445,993,995,1433,1521,3306,3389,5432,6379,8080,8443,9200,27017]
open_ports = [p for p in common_ports if scan_port(host, p)]
print(f"Open ports: {open_ports}")
```

### Service version identification (Banner Grabbing)
```python
import socket

def grab_banner(host, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        # For HTTP services, send a request to obtain the banner
        if port in [80, 443, 8080, 8443]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
        else:
            s.send(b"\r\n")
        banner = s.recv(1024).decode('utf-8', errors='ignore')
        s.close()
        return banner[:200]
    except:
        return None
```

## 2. Real IP Detection (Origin Server IP Behind a CDN)

### Method 1: DNS history records
- SecurityTrails (https://securitytrails.com/dns-trials)
- DNSHistory (https://dnshistory.org)
- ViewDNS (https://viewdns.info/iphistory/)
- Netcraft Site Report (https://sitereport.netcraft.com/)

### Method 2: Global Ping
```python
import requests
# Use multi-location Ping services
urls = [
    f"https://www.whatsmydns.net/#A/{domain}",
    f"https://ping.pe/{domain}",
    f"https://tools.keycdn.com/curl?url={domain}",
]
# If different regions resolve to different IPs, a CDN is in use
# If multiple regions resolve to the same IP, that IP may be the real origin server
```

### Method 3: Email header extraction
- Register/log in to the target site and receive an email
- Inspect the `Received:` field in the email headers
- May expose the real IP of the mail server

### Method 4: Subdomain resolution
- A CDN usually only serves the main domain
- Subdomains (e.g. mail.ftp.dev.staging) may resolve directly to the origin server IP
- Check the A records of all subdomains and exclude CDN IPs

### Method 5: SSL certificate search
```python
import requests
domain = "target.com"
r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json")
if r.status_code == 200:
    # Find IPs associated with certificates of different subdomains
    for entry in r.json():
        print(entry.get('name_value', ''))
```

## 3. Operating System Fingerprinting

### TTL inference
| TTL value | Likely operating system |
|--------|-------------|
| ≈ 64 | Linux / Unix / macOS |
| ≈ 128 | Windows |
| ≈ 255 | Network device / legacy Unix |

```python
import subprocess
# Ping to obtain the TTL
result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True)
# Windows: ping -n 1 host
# Extract the TTL from the output
import re
ttl_match = re.search(r'TTL[=:]\s*(\d+)', result.output, re.I)
if ttl_match:
    ttl = int(ttl_match.group(1))
    if ttl <= 64:
        print("Guess: Linux/Unix")
    elif ttl <= 128:
        print("Guess: Windows")
    else:
        print("Guess: network device")
```

### nmap OS detection
```bash
nmap -O <target>
# More aggressive (requires root)
sudo nmap -O --osscan-guess <target>
```

## 4. Middleware Version Identification

### HTTP response header analysis
```
Server: Apache/2.4.49 (Ubuntu)
Server: nginx/1.18.0
Server: Microsoft-IIS/10.0
X-Powered-By: PHP/7.4.3
X-Powered-By: Express
X-AspNet-Version: 4.0.30319
```

### Error page characteristics
- Apache: default 404 page contains the word "Apache"
- Nginx: default 404 page contains the word "nginx"
- IIS: default error page contains the IIS version
- Tomcat: default 404 page contains the Apache Tomcat version

### Signature file probing
```python
import requests
target = "https://target.com"
# Apache
r = requests.get(f"{target}/server-status")  # 403 = exists
r = requests.get(f"{target}/server-info")    # 403 = exists
# Nginx
r = requests.get(f"{target}/nginx_status")   # may expose status
# Tomcat
r = requests.get(f"{target}/manager/html")   # management interface
# IIS
r = requests.get(f"{target}/aspnet_client/") # ASP.NET signature
```

## 5. Database Identification

### Port probing
| Database | Default port | Notes |
|--------|---------|------|
| MySQL | 3306 | Most common |
| PostgreSQL | 5432 | Common with Rails/Django |
| MSSQL | 1433 | Windows environments |
| MongoDB | 27017 | NoSQL |
| Redis | 6379 | Cache/message queue |
| Oracle | 1521 | Enterprise-grade |
| Memcached | 11211 | Cache |

### Error message characteristics
- MySQL: `You have an error in your SQL syntax`
- PostgreSQL: `ERROR: syntax error at or near`
- MSSQL: `Microsoft SQL Server`
- Oracle: `ORA-01756`

### python_execute 检测
```python
import socket

def check_db(host, port, timeout=2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        # Try to read the banner
        s.send(b"\r\n")
        banner = s.recv(1024)
        s.close()
        return banner.hex()[:40], banner[:100]
    except:
        return None, None

db_ports = {
    3306: "MySQL", 5432: "PostgreSQL", 1433: "MSSQL",
    27017: "MongoDB", 6379: "Redis", 1521: "Oracle",
}
for port, name in db_ports.items():
    hex_banner, banner = check_db(host, port)
    if hex_banner:
        print(f"[+] {name} ({port}): {banner}")
```
