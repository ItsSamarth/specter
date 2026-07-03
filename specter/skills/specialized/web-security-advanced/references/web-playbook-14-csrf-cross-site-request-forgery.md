# CSRF Cross-Site Request Forgery
English: CSRF Cross-Site Request Forgery
- Entry Count: 8
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## CSRF Basic Attack
- ID: csrf-basic
- Difficulty: beginner
- Subcategory: Basic Attack
- Tags: csrf, cross-site, request, forgery
- Original Extracted Source: original extracted web-security-wiki source/csrf-basic.md
Description:
Basic cross-site request forgery attack techniques
Prerequisites:
- Target has sensitive operations
- CSRF protection is missing
Execution Outline:
1. 1. Construct CSRF form
2. 2. GET request CSRF
3. 3. JSON CSRF
4. 4. Link luring
## JSON CSRF Attack
- ID: csrf-json
- Difficulty: intermediate
- Subcategory: JSON CSRF
- Tags: csrf, json, api, post
- Original Extracted Source: original extracted web-security-wiki source/csrf-json.md
Description:
CSRF attack techniques targeting JSON requests
Prerequisites:
- Target uses JSON format requests
- CSRF protection is missing
- CORS is misconfigured
Execution Outline:
1. 1. Simple JSON CSRF
2. 2. Flash JSON CSRF
3. 3. XSSI attack
4. 4. SWF file attack
## CSRF Bypass Techniques
- ID: csrf-bypass
- Difficulty: intermediate
- Subcategory: Bypass Techniques
- Tags: csrf, bypass, token, referer
- Original Extracted Source: original extracted web-security-wiki source/csrf-bypass.md
Description:
Various techniques for bypassing CSRF protections
Prerequisites:
- Target has CSRF protection
- Protection mechanism has flaws
Execution Outline:
1. 1. Token validation bypass
2. 2. Referer validation bypass
3. 3. Origin validation bypass
4. 4. SameSite bypass
## SameSite Bypass Techniques
- ID: csrf-samesite
- Difficulty: intermediate
- Subcategory: SameSite Bypass
- Tags: csrf, samesite, cookie, bypass
- Original Extracted Source: original extracted web-security-wiki source/csrf-samesite.md
Description:
CSRF attacks bypassing SameSite cookie attribute
Prerequisites:
- Cookie has SameSite attribute set
- SameSite configuration has flaws
Execution Outline:
1. 1. SameSite=Lax bypass
2. 2. SameSite=Strict bypass
3. 3. SameSite not set
4. 4. Exploit OAuth flow
## Token Bypass Techniques
- ID: csrf-token-bypass
- Difficulty: intermediate
- Subcategory: Token Bypass
- Tags: csrf, token, bypass, predictable
- Original Extracted Source: original extracted web-security-wiki source/csrf-token-bypass.md
Description:
Techniques for bypassing CSRF token validation
Prerequisites:
- Target uses CSRF tokens
- Token mechanism has flaws
Execution Outline:
1. 1. Predictable token
2. 2. Token not bound to session
3. 3. Token leakage
4. 4. Token replay
## Referer Bypass Techniques
- ID: csrf-referer-bypass
- Difficulty: intermediate
- Subcategory: Referer Bypass
- Tags: csrf, referer, bypass, header
- Original Extracted Source: original extracted web-security-wiki source/csrf-referer-bypass.md
Description:
CSRF attacks bypassing Referer validation
Prerequisites:
- Target validates Referer header
- Validation logic has flaws
Execution Outline:
1. 1. Regex match bypass
2. 2. Empty Referer bypass
3. 3. Subdomain bypass
4. 4. Referrer-Policy exploitation
## Flash CSRF Attack
- ID: csrf-flash
- Difficulty: advanced
- Subcategory: Flash CSRF
- Tags: csrf, flash, swf, crossdomain
- Original Extracted Source: original extracted web-security-wiki source/csrf-flash.md
Description:
Using Flash to perform CSRF attacks
Prerequisites:
- Target allows Flash requests
- crossdomain.xml is misconfigured
Execution Outline:
1. 1. crossdomain.xml exploitation
2. 2. Create malicious SWF
3. 3. Send JSON request
4. 4. Custom header
## CORS Misconfiguration Exploitation
- ID: csrf-cors
- Difficulty: intermediate
- Subcategory: CORS Misconfiguration
- Tags: csrf, cors, misconfiguration, api
- Original Extracted Source: original extracted web-security-wiki source/csrf-cors.md
Description:
Using CORS misconfiguration for CSRF attacks
Prerequisites:
- CORS is misconfigured
- Cross-origin requests with credentials are allowed
Execution Outline:
1. 1. Detect CORS configuration
2. 2. Reflected Origin attack
3. 3. null origin attack
4. 4. Regex bypass
