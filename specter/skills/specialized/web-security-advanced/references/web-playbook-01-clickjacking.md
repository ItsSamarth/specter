# Clickjacking
English: Clickjacking
- Entry Count: 2
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Basic Clickjacking
- ID: clickjacking-basic
- Difficulty: beginner
- Subcategory: Basics
- Tags: clickjacking, ui-redressing, iframe
- Original Extracted Source: original extracted web-security-wiki source/clickjacking-basic.md
Description:
Use a transparent iframe overlay to trick users into unknowingly clicking hidden malicious buttons or links
Prerequisites:
- The target site allows being embedded in an iframe
- The target does not set the X-Frame-Options response header
- The target does not configure a CSP frame-ancestors policy
- Basic knowledge of HTML/CSS
Execution Outline:
1. Detect X-Frame-Options and CSP
2. Basic transparent iframe overlay POC
3. Multi-step drag-and-drop hijacking (Drag-and-Drop)
4. Bypass using CSS pointer-events
## Clickjacking + XSS
- ID: clickjacking-xss
- Difficulty: intermediate
- Subcategory: XSS
- Tags: clickjacking, xss
- Original Extracted Source: original extracted web-security-wiki source/clickjacking-xss.md
Description:
Combine clickjacking with XSS attacks, first using clickjacking to trigger the XSS attack vector to gain deeper control
Prerequisites:
- The target has an XSS vulnerability
- The target allows being embedded in an iframe
- The XSS payload can be triggered by a click
Execution Outline:
1. Identify exploitable XSS and Clickjacking combinations
2. Self-XSS + Clickjacking combined exploitation
3. Reflected XSS + iframe nesting exploitation

