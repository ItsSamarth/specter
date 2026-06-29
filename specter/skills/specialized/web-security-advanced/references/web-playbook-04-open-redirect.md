# Open Redirect
English: Open Redirect
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Basic Open Redirect
- ID: redirect-basic
- Difficulty: beginner
- Subcategory: Basic
- Tags: redirect, url, phishing
- Original Extracted Source: original extracted web-security-wiki source/redirect-basic.md
Description:
URL redirection vulnerability exploitation
Prerequisites:
- Target parameter controls the redirect address
Execution Outline:
1. Direct redirect
2. Bypass validation
3. Slash bypass
## Redirect Bypass
- ID: redirect-bypass
- Difficulty: intermediate
- Subcategory: Bypass
- Tags: redirect, bypass
- Original Extracted Source: original extracted web-security-wiki source/redirect-bypass.md
Description:
Open redirect bypass techniques
Prerequisites:
- A redirect parameter exists
Execution Outline:
1. URL encoding
2. @ symbol
3. Backslash
## Redirect to SSRF
- ID: redirect-ssrf
- Difficulty: intermediate
- Subcategory: SSRF
- Tags: redirect, ssrf
- Original Extracted Source: original extracted web-security-wiki source/redirect-ssrf.md
Description:
Leverage an open redirect vulnerability as a pivot to steer SSRF probing into the internal network, bypassing the SSRF URL allowlist/blocklist restrictions
Prerequisites:
- Target has an Open Redirect vulnerability
- Target has an SSRF entry point (URL parameter/Webhook, etc.)
- SSRF filtering only checks the initial URL and does not follow redirects
Execution Outline:
1. Identify the open redirect point
2. Bypass SSRF filtering via the redirect
3. Short links and DNS rebinding assistance
4. Full exploitation chain: redirect → SSRF → internal network probing
