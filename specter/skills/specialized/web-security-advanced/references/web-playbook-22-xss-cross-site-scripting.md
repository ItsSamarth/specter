# XSS Cross-Site Scripting
English: XSS Cross-Site Scripting
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Reflected XSS
- ID: xss-reflected
- Difficulty: beginner
- Subcategory: Reflected
- Tags: xss, reflected, javascript
- Original Extracted Source: original extracted web-security-wiki source/xss-reflected.md
Description:
Reflected cross-site scripting attack techniques
Prerequisites:
- User input is reflected back to the page
- Input is not filtered or encoded
Execution Outline:
1. 1. Probe XSS injection points
2. 2. Event handler bypass
3. 3. Tag bypass
4. 4. Steal cookies
## Stored XSS
- ID: xss-stored
- Difficulty: intermediate
- Subcategory: Stored
- Tags: xss, stored, persistent
- Original Extracted Source: original extracted web-security-wiki source/xss-stored.md
Description:
Stored cross-site scripting attack techniques
Prerequisites:
- Data storage functionality exists
- Stored data is displayed without filtering
Execution Outline:
1. 1. Probe storage points
2. 2. Stealthy payload
3. 3. Persistent control
4. 4. BeEF Hook
## DOM-Based XSS
- ID: xss-dom
- Difficulty: intermediate
- Subcategory: DOM-Based
- Tags: xss, dom, javascript
- Original Extracted Source: original extracted web-security-wiki source/xss-dom.md
Description:
DOM-based cross-site scripting attacks
Prerequisites:
- JavaScript dynamically manipulates the DOM
- User input is written directly to the DOM
Execution Outline:
1. 1. Probe DOM XSS
2. 2. Common sink points
3. 3. location.hash exploitation
4. 4. postMessage exploitation
## CSP Bypass
- ID: xss-csp-bypass
- Difficulty: advanced
- Subcategory: CSP Bypass
- Tags: xss, csp, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-csp-bypass.md
Description:
XSS techniques for bypassing Content Security Policy (CSP)
Prerequisites:
- XSS vulnerability exists
- CSP policy is present but misconfigured
Execution Outline:
1. 1. Analyze CSP policy
2. 2. Exploit unsafe-inline
3. 3. Exploit unsafe-eval
4. 4. JSONP bypass
## Mutation XSS (mXSS)
- ID: xss-mxss
- Difficulty: advanced
- Subcategory: Mutation-Based
- Tags: xss, mxss, mutation, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-mxss.md
Description:
XSS attacks exploiting browser parsing discrepancies
Prerequisites:
- HTML output point exists
- Browser parsing discrepancies exist
Execution Outline:
1. 1. Basic mXSS probing
2. 2. SVG mXSS
3. 3. Math mXSS
4. 4. DOM clobbering combination
## Unicode XSS
- ID: xss-unicode
- Difficulty: intermediate
- Subcategory: Unicode Encoding
- Tags: xss, unicode, encoding, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-unicode.md
Description:
Using Unicode encoding characteristics to bypass filters
Prerequisites:
- XSS injection point exists
- Filter checks for keywords
Execution Outline:
1. 1. Unicode escaping
2. 2. HTML entity encoding
3. 3. Unicode normalization attack
4. 4. UTF-7 encoding
## XSS Filter Bypass
- ID: xss-filter-bypass
- Difficulty: intermediate
- Subcategory: Filter Bypass
- Tags: xss, filter, bypass, waf
- Original Extracted Source: original extracted web-security-wiki source/xss-filter-bypass.md
Description:
Various techniques for bypassing XSS filters
Prerequisites:
- XSS injection point exists
- Filtering mechanism is in place
Execution Outline:
1. 1. Case obfuscation
2. 2. Double-write bypass
3. 3. Comment obfuscation
4. 4. Null byte truncation
## XSS Encoding Bypass
- ID: xss-encoding
- Difficulty: intermediate
- Subcategory: Encoding Bypass
- Tags: xss, encoding, bypass
- Original Extracted Source: original extracted web-security-wiki source/xss-encoding.md
Description:
Using various encoding techniques to bypass XSS filters
Prerequisites:
- XSS injection point exists
- Encoding processing is in place
Execution Outline:
1. 1. URL encoding
2. 2. HTML entity encoding
3. 3. JavaScript encoding
4. 4. CSS encoding
## Polyglot XSS
- ID: xss-polyglot
- Difficulty: intermediate
- Subcategory: Polyglot
- Tags: xss, polyglot, universal
- Original Extracted Source: original extracted web-security-wiki source/xss-polyglot.md
Description:
Universal XSS payloads for multiple environments
Prerequisites:
- XSS injection point exists
- Specific environment is unknown
Execution Outline:
1. 1. Classic polyglot
2. 2. Short polyglot
3. 3. Attribute injection polyglot
4. 4. URL parameter polyglot
## XSS Cookie Theft
- ID: xss-cookie-theft
- Difficulty: beginner
- Subcategory: Cookie Theft
- Tags: xss, cookie, theft, session
- Original Extracted Source: original extracted web-security-wiki source/xss-cookie-theft.md
Description:
Stealing user cookies using XSS
Prerequisites:
- XSS vulnerability exists
- Cookie does not have HttpOnly flag set
Execution Outline:
1. 1. Basic cookie theft
2. 2. Fetch API theft
3. 3. XMLHttpRequest theft
4. 4. Encoded transmission
## XSS Keylogger
- ID: xss-keylogger
- Difficulty: intermediate
- Subcategory: Keylogger
- Tags: xss, keylogger, credential
- Original Extracted Source: original extracted web-security-wiki source/xss-keylogger.md
Description:
Recording user keyboard input using XSS
Prerequisites:
- Stored XSS exists
- Target page has sensitive input fields
Execution Outline:
1. 1. Basic keylogging
2. 2. Full keylogger
3. 3. Form theft
4. 4. Form submission hijacking
## BeEF Framework Exploitation
- ID: xss-beef
- Difficulty: advanced
- Subcategory: BeEF Exploitation
- Tags: xss, beef, framework, exploitation
- Original Extracted Source: original extracted web-security-wiki source/xss-beef.md
Description:
Using BeEF framework for XSS exploitation
Prerequisites:
- XSS vulnerability exists
- BeEF server deployed
Execution Outline:
1. 1. Deploy BeEF
2. 2. Inject hook script
3. 3. Common commands
4. 4. Module exploitation
