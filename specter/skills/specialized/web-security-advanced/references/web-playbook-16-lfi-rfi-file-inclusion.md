# LFI/RFI File Inclusion
English: LFI/RFI File Inclusion
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Local File Inclusion
- ID: lfi-basic
- Difficulty: intermediate
- Subcategory: Local Inclusion
- Tags: lfi, local, file, inclusion
- Original Extracted Source: original extracted web-security-wiki source/lfi-basic.md
Description:
Local file inclusion vulnerability exploitation techniques
Prerequisites:
- File inclusion functionality exists
- User can control the inclusion path
Execution Outline:
1. 1. Probe for LFI
2. 2. Read sensitive files
3. 3. PHP pseudo-protocols
4. 4. Log poisoning
## Remote File Inclusion
- ID: rfi-basic
- Difficulty: intermediate
- Subcategory: Remote Inclusion
- Tags: rfi, remote, file, inclusion
- Original Extracted Source: original extracted web-security-wiki source/rfi-basic.md
Description:
Remote file inclusion vulnerability exploitation techniques
Prerequisites:
- File inclusion functionality exists
- allow_url_include=On
- User can control the inclusion path
Execution Outline:
1. 1. Probe for RFI
2. 2. Host malicious file
3. 3. Reverse shell
4. 4. Use data protocol
## Log Poisoning LFI
- ID: lfi-log-poison
- Difficulty: intermediate
- Subcategory: Log Poisoning
- Tags: lfi, log, poison, rce
- Original Extracted Source: original extracted web-security-wiki source/lfi-log-poison.md
Description:
Achieving LFI to RCE via log poisoning
Prerequisites:
- LFI vulnerability exists
- Log files can be included
- Log files are writable
Execution Outline:
1. 1. Probe log file location
2. 2. Poison User-Agent
3. 3. Poison request path
4. 4. Execute commands
## PHP Pseudo-Protocol Exploitation
- ID: lfi-wrapper
- Difficulty: intermediate
- Subcategory: Pseudo-Protocol
- Tags: lfi, wrapper, php, protocol
- Original Extracted Source: original extracted web-security-wiki source/lfi-wrapper.md
Description:
Using PHP pseudo-protocols for LFI attacks
Prerequisites:
- LFI vulnerability exists
- PHP environment
- Pseudo-protocols are not disabled
Execution Outline:
1. 1. php://filter
2. 2. php://input
3. 3. data:// protocol
4. 4. phar:// protocol
## Directory Traversal Techniques
- ID: lfi-traversal
- Difficulty: beginner
- Subcategory: Directory Traversal
- Tags: lfi, traversal, bypass, path
- Original Extracted Source: original extracted web-security-wiki source/lfi-traversal.md
Description:
LFI directory traversal bypass techniques
Prerequisites:
- LFI vulnerability exists
- Path filtering is in place
Execution Outline:
1. 1. Basic traversal
2. 2. Bypass deletion of ../
3. 3. URL encoding bypass
4. 4. Unicode encoding bypass
## PHP Filter Chain Attack
- ID: lfi-php-filter
- Difficulty: intermediate
- Subcategory: PHP Filter
- Tags: lfi, php, filter, chain
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-filter.md
Description:
Using PHP filter chains for LFI attacks
Prerequisites:
- LFI vulnerability exists
- PHP environment
- filter pseudo-protocol is available
Execution Outline:
1. 1. Read source code
2. 2. Multiple filters
3. 3. Filter chain RCE
4. 4. Read configuration files
## PHP Input Execution
- ID: lfi-php-input
- Difficulty: intermediate
- Subcategory: PHP Input
- Tags: lfi, php, input, rce
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-input.md
Description:
Executing PHP code using php://input
Prerequisites:
- LFI vulnerability exists
- allow_url_include=On
- POST method is available
Execution Outline:
1. 1. Basic execution
2. 2. Command execution
3. 3. File operations
4. 4. Reverse shell
## PHP Data Protocol Attack
- ID: lfi-php-data
- Difficulty: intermediate
- Subcategory: PHP Data
- Tags: lfi, php, data, protocol
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-data.md
Description:
Executing PHP code using data:// protocol
Prerequisites:
- LFI vulnerability exists
- allow_url_include=On
- data protocol is available
Execution Outline:
1. 1. Basic execution
2. 2. Base64 encoding
3. 3. Command execution
4. 4. Reverse shell
## PHP Zip Protocol Attack
- ID: lfi-php-zip
- Difficulty: intermediate
- Subcategory: PHP Zip
- Tags: lfi, php, zip, archive
- Original Extracted Source: original extracted web-security-wiki source/lfi-php-zip.md
Description:
Using zip:// protocol for LFI attacks
Prerequisites:
- LFI vulnerability exists
- Zip file upload is possible
- zip protocol is available
Execution Outline:
1. 1. Create malicious zip
2. 2. Upload zip file
3. 3. Include zip file
4. 4. Image webshell
## Phar Deserialization Attack
- ID: lfi-phar
- Difficulty: advanced
- Subcategory: Phar Deserialization
- Tags: lfi, phar, deserialization, rce
- Original Extracted Source: original extracted web-security-wiki source/lfi-phar.md
Description:
Achieving RCE via Phar deserialization
Prerequisites:
- LFI vulnerability exists
- PHP environment
- phar extension is available
Execution Outline:
1. 1. Create Phar file
2. 2. Trigger deserialization
3. 3. Image webshell via Phar
4. 4. Common gadget chains
## Session File Inclusion
- ID: lfi-session
- Difficulty: intermediate
- Subcategory: Session Inclusion
- Tags: lfi, session, file, inclusion
- Original Extracted Source: original extracted web-security-wiki source/lfi-session.md
Description:
Using session files for LFI attacks
Prerequisites:
- LFI vulnerability exists
- Session content is controllable
- Session path is known
Execution Outline:
1. 1. Probe session path
2. 2. Control session content
3. 3. Include session file
4. 4. Session race condition
## Proc Filesystem Exploitation
- ID: lfi-proc
- Difficulty: intermediate
- Subcategory: Proc Filesystem
- Tags: lfi, proc, linux, environ
- Original Extracted Source: original extracted web-security-wiki source/lfi-proc.md
Description:
Using /proc filesystem for LFI attacks
Prerequisites:
- LFI vulnerability exists
- Linux system
- /proc is accessible
Execution Outline:
1. 1. Read process information
2. 2. Read environment variables
3. 3. Read logs via fd
4. 4. Read other processes
