# File Vulnerabilities
English: File Vulnerabilities
- Entry Count: 7
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## File Upload Bypass
- ID: file-upload-bypass
- Difficulty: intermediate
- Subcategory: File Upload
- Tags: upload, bypass, webshell
- Original Extracted Source: original extracted web-security-wiki source/file-upload-bypass.md
Description:
File upload restriction bypass techniques
Prerequisites:
- Target has a file upload function
- Upload restrictions are in place
Execution Outline:
1. Extension bypass
2. Content-Type
3. Image webshell
4. Whitespace bypass
## Arbitrary File Download
- ID: file-download
- Difficulty: beginner
- Subcategory: Download
- Tags: file-download, lfi, leak
- Original Extracted Source: original extracted web-security-wiki source/file-download.md
Description:
Exploiting path control flaws in file download functionality to download arbitrary sensitive files from the server
Prerequisites:
- Target has a file download function
- File path parameter is controllable
- Server does not strictly filter paths
Execution Outline:
1. Identify file download interface
2. Path traversal to download sensitive files
3. Download source code and database configuration
4. Automated batch sensitive file probing
## Race Condition
- ID: file-competition
- Difficulty: advanced
- Subcategory: Race Condition
- Tags: race-condition, file-upload
- Original Extracted Source: original extracted web-security-wiki source/file-competition.md
Description:
Exploiting race conditions (TOCTOU) during file upload/processing to execute malicious operations within the time window between security check and file use
Prerequisites:
- Target has a file upload function
- Server follows an upload-then-check processing flow
- High-concurrency access to uploaded files is possible
- Temporary file storage path is known
Execution Outline:
1. Identify race condition window
2. Race condition exploitation - concurrent upload and access
3. Python concurrent race exploitation script
4. .htaccess race write
## Path Traversal
- ID: file-traversal
- Difficulty: beginner
- Subcategory: Traversal
- Tags: traversal, file
- Original Extracted Source: original extracted web-security-wiki source/file-traversal.md
Description:
Using path traversal (../) sequences to break out of directory restrictions for file access, reading or writing arbitrary files outside the web root
Prerequisites:
- Target has file read/include functionality
- File path parameter is controllable
- Server path filtering is not strict
Execution Outline:
1. Basic path traversal testing
2. Encoding bypass of path filters
3. Windows-specific path traversal
4. LFI to RCE escalation
## Zip Slip
- ID: file-zip-slip
- Difficulty: intermediate
- Subcategory: Zip
- Tags: zip-slip, file, rce
- Original Extracted Source: original extracted web-security-wiki source/file-zip-slip.md
Description:
Using path traversal in maliciously crafted archive files (ZIP/TAR) to achieve arbitrary file write, overwriting critical server files or writing a webshell
Prerequisites:
- Target has ZIP/TAR file upload with automatic extraction
- Extraction library does not filter path traversal in filenames
- Web root or other critical directory path is known
Execution Outline:
1. Probe ZIP upload and extraction functionality
2. Construct Zip Slip malicious archive
3. Upload and verify Zip Slip
4. TAR archive Zip Slip variant
## MIME Type Bypass
- ID: file-mime
- Difficulty: beginner
- Subcategory: MIME
- Tags: mime, bypass
- Original Extracted Source: original extracted web-security-wiki source/file-mime.md
Description:
Bypassing file upload type checks by spoofing MIME type (Content-Type) to upload malicious executable files
Prerequisites:
- Target has a file upload function
- Server only determines file type by Content-Type
- Allowed MIME types are known
Execution Outline:
1. Probe file type checking mechanism
2. MIME type spoofing to upload webshell
3. Magic bytes spoofing
4. Verify upload result
## Null Byte Truncation
- ID: file-null-byte
- Difficulty: intermediate
- Subcategory: Null Byte
- Tags: null-byte, bypass
- Original Extracted Source: original extracted web-security-wiki source/file-null-byte.md
Description:
Using null bytes (%00/\x00) to truncate file extension validation, bypassing file upload whitelist restrictions
Prerequisites:
- Target uses whitelist to validate file extensions
- Backend language or library is affected by null byte truncation (PHP<5.3.4, older Java versions)
- Truncation point exists in server-side path concatenation
Execution Outline:
1. Null byte truncation principles and environment detection
2. File upload null byte truncation
3. File inclusion null byte truncation
4. Modern alternatives (PHP>=5.3.4)
