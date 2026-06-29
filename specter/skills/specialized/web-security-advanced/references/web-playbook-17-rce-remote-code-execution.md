# RCE Remote Code Execution
English: RCE Remote Code Execution
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Command Injection
- ID: rce-command-injection
- Difficulty: intermediate
- Subcategory: Command Injection
- Tags: rce, command, injection, os
- Original Extracted Source: original extracted web-security-wiki source/rce-command-injection.md
Description:
Operating system command injection attack techniques
Prerequisites:
- A system command execution feature exists
- User input is not filtered
Execution Outline:
1. 1. Detect command injection
2. 2. Linux command injection
3. 3. Windows command injection
4. 4. Blind command injection
## PHP Code Execution
- ID: rce-php
- Difficulty: intermediate
- Subcategory: PHP Code Execution
- Tags: rce, php, code, execution
- Original Extracted Source: original extracted web-security-wiki source/rce-php.md
Description:
PHP code execution vulnerability exploitation techniques
Prerequisites:
- A PHP code execution point exists
- User input can control the code
Execution Outline:
1. 1. Common dangerous functions
2. 2. Command execution
3. 3. One-line webshell
4. 4. AV-evading one-line webshell
## PHP Filter Chain RCE
- ID: rce-php-filter
- Difficulty: advanced
- Subcategory: PHP Filter Chain
- Tags: rce, php, filter, chain
- Original Extracted Source: original extracted web-security-wiki source/rce-php-filter.md
Description:
Construct RCE using a PHP filter chain
Prerequisites:
- A file inclusion vulnerability exists
- The PHP version supports filter chains
Execution Outline:
1. 1. Filter chain principles
2. 2. Construct the filter chain
3. 3. Generate using tools
4. 4. Complete exploitation example
## Blind Command Injection
- ID: rce-cmd-blind
- Difficulty: intermediate
- Subcategory: Blind Command Injection
- Tags: rce, blind, command, injection
- Original Extracted Source: original extracted web-security-wiki source/rce-cmd-blind.md
Description:
Exploitation techniques for command injection without output
Prerequisites:
- A command injection point exists
- No direct output
Execution Outline:
1. 1. Time-based blind injection
2. 2. DNS exfiltration
3. 3. HTTP exfiltration
4. 4. ICMP exfiltration
## Deserialization Vulnerability
- ID: rce-deserialize
- Difficulty: advanced
- Subcategory: Deserialization
- Tags: rce, deserialize, java, php
- Original Extracted Source: original extracted web-security-wiki source/rce-deserialize.md
Description:
Achieve RCE by exploiting a deserialization vulnerability
Prerequisites:
- A deserialization point exists
- An exploitable gadget chain exists
Execution Outline:
1. 1. Java deserialization
2. 2. PHP deserialization
3. 3. Python deserialization
4. 4. .NET deserialization
## PHP Deserialization
- ID: rce-deserialize-php
- Difficulty: advanced
- Subcategory: PHP Deserialization
- Tags: rce, php, deserialize, unserialize
- Original Extracted Source: original extracted web-security-wiki source/rce-deserialize-php.md
Description:
PHP deserialization vulnerability exploitation techniques
Prerequisites:
- An unserialize call exists
- An exploitable class exists
Execution Outline:
1. 1. Magic methods
2. 2. Construct a POP chain
3. 3. Phar deserialization
4. 4. Session deserialization
## Java Deserialization
- ID: rce-deserialize-java
- Difficulty: advanced
- Subcategory: Java Deserialization
- Tags: rce, java, deserialize, ysoserial
- Original Extracted Source: original extracted web-security-wiki source/rce-deserialize-java.md
Description:
Java deserialization vulnerability exploitation techniques
Prerequisites:
- A Java deserialization point exists
- A gadget chain exists
Execution Outline:
1. 1. Common gadget chains
2. 2. Using ysoserial
3. 3. JRMP attack
4. 4. In-memory webshell injection
## File Upload Vulnerability
- ID: rce-file-upload
- Difficulty: intermediate
- Subcategory: File Upload
- Tags: rce, upload, webshell, file
- Original Extracted Source: original extracted web-security-wiki source/rce-file-upload.md
Description:
Obtain RCE by exploiting a file upload vulnerability
Prerequisites:
- A file upload feature exists
- Executable files can be uploaded
Execution Outline:
1. 1. Basic upload
2. 2. Front-end bypass
3. 3. Back-end bypass
4. 4. Image webshell
## File Inclusion RCE
- ID: rce-include
- Difficulty: intermediate
- Subcategory: File Inclusion
- Tags: rce, include, lfi, rfi
- Original Extracted Source: original extracted web-security-wiki source/rce-include.md
Description:
Achieve RCE by exploiting a file inclusion vulnerability
Prerequisites:
- A file inclusion vulnerability exists
- A malicious file can be included
Execution Outline:
1. 1. Log poisoning
2. 2. Session file inclusion
3. 3. /proc/self/environ
4. 4. PHP wrappers
## Log Poisoning RCE
- ID: rce-log-poison
- Difficulty: intermediate
- Subcategory: Log Poisoning
- Tags: rce, log, poison, lfi
- Original Extracted Source: original extracted web-security-wiki source/rce-log-poison.md
Description:
Achieve RCE through log poisoning
Prerequisites:
- A file inclusion vulnerability exists
- Log files can be read
Execution Outline:
1. 1. Apache log poisoning
2. 2. Nginx log poisoning
## Image Webshell RCE
- ID: rce-image
- Difficulty: intermediate
- Subcategory: Image Webshell
- Tags: rce, image, webshell, upload
- Original Extracted Source: original extracted web-security-wiki source/rce-image.md
Description:
Achieve RCE using an image webshell
Prerequisites:
- A file upload exists
- A file inclusion exists
Execution Outline:
1. 1. Create the image webshell
2. 2. Image webshell content
3. 3. Execute via file inclusion
4. 4. Combine with .htaccess
## .htaccess Exploitation
- ID: rce-htaccess
- Difficulty: intermediate
- Subcategory: .htaccess
- Tags: rce, htaccess, apache, upload
- Original Extracted Source: original extracted web-security-wiki source/rce-htaccess.md
Description:
Achieve RCE using an .htaccess file
Prerequisites:
- Apache server
- An .htaccess file can be uploaded
Execution Outline:
1. 1. Parse other extensions
2. 2. Auto-prepend inclusion
3. 3. Rewrite-rule RCE
4. 4. Error page inclusion
