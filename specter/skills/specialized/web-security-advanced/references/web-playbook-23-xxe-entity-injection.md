# XXE Entity Injection
English: XXE Entity Injection
- Entry Count: 9
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## XXE Basic Attack
- ID: xxe-basic
- Difficulty: intermediate
- Subcategory: Basic Attack
- Tags: xxe, xml, external, entity
- Original Extracted Source: original extracted web-security-wiki source/xxe-basic.md
Description:
Basic XML external entity injection attack techniques
Prerequisites:
- XML parsing functionality exists
- External entities are not disabled
Execution Outline:
1. 1. Probe for XXE
2. 2. Read files
3. 3. Read PHP source code
4. 4. SSRF attack
## Blind XXE Attack
- ID: xxe-blind
- Difficulty: intermediate
- Subcategory: Blind XXE
- Tags: xxe, blind, oob, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-blind.md
Description:
XXE attack techniques with no direct output
Prerequisites:
- XML parsing exists
- No direct output/reflection
Execution Outline:
1. 1. External entity probing
2. 2. Parameter entities
3. 3. OOB out-of-band data exfiltration
## XXE OOB Out-of-Band Attack
- ID: xxe-oob
- Difficulty: intermediate
- Subcategory: OOB Out-of-Band
- Tags: xxe, oob, exfiltration, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-oob.md
Description:
Using OOB techniques to exfiltrate XXE data
Prerequisites:
- XXE vulnerability exists
- Outbound requests can be made
Execution Outline:
1. 1. HTTP out-of-band
2. 2. FTP out-of-band
3. 3. DNS out-of-band
## XXE + SSRF Combined Attack
- ID: xxe-ssrf
- Difficulty: intermediate
- Subcategory: XXE+SSRF
- Tags: xxe, ssrf, combination, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-ssrf.md
Description:
Using XXE to achieve SSRF attacks
Prerequisites:
- XXE vulnerability exists
- Internal network is accessible
Execution Outline:
1. 1. Scan internal network ports
2. 2. Access internal services
## XXE to RCE
- ID: xxe-rce
- Difficulty: advanced
- Subcategory: XXE to RCE
- Tags: xxe, rce, php, expect
- Original Extracted Source: original extracted web-security-wiki source/xxe-rce.md
Description:
Using XXE to achieve remote code execution
Prerequisites:
- XXE vulnerability exists
- PHP expect extension is loaded
Execution Outline:
1. 1. Expect extension RCE
2. 2. Write WebShell
## XXE File Read
- ID: xxe-file-read
- Difficulty: beginner
- Subcategory: File Read
- Tags: xxe, file, read, lfi
- Original Extracted Source: original extracted web-security-wiki source/xxe-file-read.md
Description:
Using XXE to read server files
Prerequisites:
- XXE vulnerability exists
- File read permissions exist
Execution Outline:
1. 1. Read Linux files
2. 2. Read Windows files
3. 3. Read web configuration
4. 4. Read source code
## XXE External DTD Exploitation
- ID: xxe-dtd
- Difficulty: intermediate
- Subcategory: External DTD
- Tags: xxe, dtd, external, xml
- Original Extracted Source: original extracted web-security-wiki source/xxe-dtd.md
Description:
Using external DTD files for XXE attacks
Prerequisites:
- XXE vulnerability exists
- External DTD is accessible
Execution Outline:
1. 1. Host malicious DTD
2. 2. Reference external DTD
3. 3. Multi-step out-of-band exfiltration
4. 4. Error message leakage
## XLSX File XXE
- ID: xxe-xlsx
- Difficulty: intermediate
- Subcategory: XLSX File XXE
- Tags: xxe, xlsx, excel, office
- Original Extracted Source: original extracted web-security-wiki source/xxe-xlsx.md
Description:
Using XLSX files to perform XXE attacks
Prerequisites:
- Application parses XLSX files
- XXE vulnerability exists
Execution Outline:
1. 1. Unzip XLSX file
2. 2. Inject XXE payload
## DOCX File XXE
- ID: xxe-docx
- Difficulty: intermediate
- Subcategory: DOCX File XXE
- Tags: xxe, docx, word, office
- Original Extracted Source: original extracted web-security-wiki source/xxe-docx.md
Description:
Using DOCX files to perform XXE attacks
Prerequisites:
- Application parses DOCX files
- XXE vulnerability exists
Execution Outline:
1. 1. Unzip DOCX file
2. 2. Inject XXE payload
