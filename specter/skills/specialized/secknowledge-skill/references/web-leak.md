# Web Security - Information Disclosure

> Source: WooYun Vulnerability Database | Split from web-file-infra.md

## III. Information Disclosure

### 3.1 Vulnerability Essence

```
Information disclosure essence: Attack surface exposure -> Trust chain breach -> In-depth penetration
Pattern: A single leak point can cause the entire trust chain to collapse
         Source code -> Config -> Database -> Internal network -> Total compromise
```

### 3.2 Sensitive File Path Dictionary

Version control disclosure:

```bash
# Git disclosure (highest detection priority)
/.git/config          # Contains remote repository URL
/.git/HEAD            # Current branch
/.git/index           # Staging area index
/.git/logs/HEAD       # Operation log

# SVN disclosure
/.svn/entries         # SVN 1.6 and below
/.svn/wc.db           # SVN 1.7+ SQLite database

# Exploitation tools: dvcs-ripper, GitHack, svn-extractor
```

Backup file disclosure:

```bash
# Archive backups (530 hits)
/wwwroot.rar | /www.zip | /web.rar | /backup.zip | /site.tar.gz
/{domain}.zip | /{domain}.rar

# SQL backups (136 hits)
/backup.sql | /database.sql | /db.sql | /dump.sql

# Config backups (101 hits)
/config.php.bak | /web.config.bak | /.env.bak
/config_global.php.bak
```

Configuration file disclosure:

```bash
# General
/.env | /.env.local | /.env.production
/config.yml | /config.json | /appsettings.json

# PHP
/config.php | /include/config.php | /data/config.php

# Java/Spring
/WEB-INF/web.xml | /WEB-INF/classes/application.properties
/WEB-INF/classes/jdbc.properties

# .NET
/web.config | /connectionStrings.config
```

Probe / debug / log files:

```bash
# Probe files
/phpinfo.php | /info.php | /test.php | /probe.php

# Log files
/ctp.log | /logs/ctp.log | /debug.log | /storage/logs/

# Admin interfaces
/phpmyadmin/ | /pma/ | /adminer.php
/swagger-ui.html | /api-docs
/actuator/env                    # Spring Boot
```

### 3.3 Detection Methodology

```
Phase 1 Passive collection: Response headers (Server/X-Powered-By) -> Error pages -> robots.txt -> Source code comments/JS
Phase 2 Targeted probing: Version control (.git/.svn) -> Backup files (domain/date) -> Sensitive paths
Phase 3 Search engines: Google Hacking syntax
```

Google Hacking quick reference:

```
site:target.com filetype:sql | filetype:bak | filetype:zip
site:target.com filetype:env | filetype:log
site:target.com inurl:.git | inurl:.svn
site:target.com inurl:phpinfo | intitle:phpinfo
site:target.com "db_password" | "mysql_connect"
```

### 3.4 Information Exploitation Chain

```
Source code leak  -> Config file    -> DB credentials  -> DB takeover    -> Server privilege escalation
Version control   -> Source audit   -> SQL injection    -> Admin access   -> File upload to get shell
Config leak       -> DB connection  -> Database        -> User data      -> Business takeover
Log leak          -> Session        -> Identity hijack -> Business data  -> Lateral movement
API interface     -> Credentials    -> Decryption      -> Mass control   -> Full penetration
Third-party creds -> SMS/OSS        -> Verification    -> Account takeover -> Data breach
```

### 3.5 Defense Measures

Nginx security configuration:

```nginx
location ~ /\.(git|svn|env|htaccess|htpasswd) { deny all; return 404; }
location ~ \.(bak|sql|log|config|ini|yml)$ { deny all; return 404; }
location ~* /(backup|bak|old|temp|test|dev)/ { deny all; return 404; }
autoindex off;
server_tokens off;
```

Apache security configuration:

```apache
<FilesMatch "\.(git|svn|env|bak|sql|log|config)">
    Order Allow,Deny
    Deny from all
</FilesMatch>
Options -Indexes
ServerSignature Off
```

CI/CD integration: Scan for sensitive files before deployment -> Prohibit deploying .git/.svn -> Encrypt config files

---
