# Authentication Vulnerabilities
English: Authentication Vulnerabilities
- Entry Count: 10
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Authentication Bypass
- ID: auth-bypass
- Difficulty: intermediate
- Subcategory: Authentication Bypass
- Tags: auth, bypass, authentication
- Original Extracted Source: original extracted web-security-wiki source/auth-bypass.md
Description:
Web application authentication bypass techniques
Prerequisites:
- Target has an authentication mechanism
- The authentication implementation has flaws
Execution Outline:
1. SQL injection bypass
2. Array bypass
3. Type juggling
4. JSON bypass
## Brute Force
- ID: auth-brute
- Difficulty: beginner
- Subcategory: Brute Force
- Tags: auth, brute-force, password
- Original Extracted Source: original extracted web-security-wiki source/auth-brute.md
Description:
Automated password guessing attack
Prerequisites:
- No CAPTCHA
- No lockout policy
Execution Outline:
1. Pitchfork
2. Cluster bomb
3. Username enumeration based on response differences
4. CAPTCHA/OTP brute force and bypass
## Session Hijacking
- ID: auth-session
- Difficulty: intermediate
- Subcategory: Session Management
- Tags: auth, session, hijack
- Original Extracted Source: original extracted web-security-wiki source/auth-session.md
Description:
Exploit session management flaws to hijack or forge user sessions and gain unauthorized access
Prerequisites:
- Target uses Cookie- or Token-based session management
- Session identifiers can be intercepted or predicted
- Network communication is not fully encrypted (HTTP) or XSS exists
Execution Outline:
1. Session Cookie attribute analysis
2. Session Fixation attack
3. Session hijacking (HTTP sniffing)
4. Session prediction (weak randomness)
## Password Reset Vulnerabilities
- ID: auth-password-reset
- Difficulty: intermediate
- Subcategory: Logic Vulnerability
- Tags: auth, password-reset, logic
- Original Extracted Source: original extracted web-security-wiki source/auth-password-reset.md
Description:
Bypass the password reset flow
Prerequisites:
- The password reset feature has logic flaws
Execution Outline:
1. Host header poisoning
2. Token brute force
3. Password reset Token predictability analysis
4. Password reset flow logic flaws
## OAuth Vulnerabilities
- ID: auth-oauth
- Difficulty: advanced
- Subcategory: OAuth
- Tags: auth, oauth, redirect
- Original Extracted Source: original extracted web-security-wiki source/auth-oauth.md
Description:
OAuth authentication flow vulnerabilities
Prerequisites:
- Uses OAuth login
Execution Outline:
1. CSRF attack
2. Redirect URI
3. OAuth State parameter missing/predictable CSRF
4. Token theft and Scope privilege escalation
## SAML Vulnerabilities
- ID: auth-saml
- Difficulty: advanced
- Subcategory: SAML
- Tags: auth, saml, xml
- Original Extracted Source: original extracted web-security-wiki source/auth-saml.md
Description:
SAML assertion attacks
Prerequisites:
- Uses SAML SSO
Execution Outline:
1. XML signature bypass
2. XXE attack
3. SAML Response tampering and replay
4. Advanced SAML signature bypass techniques
## 2FA Bypass
- ID: auth-2fa
- Difficulty: intermediate
- Subcategory: 2FA
- Tags: auth, 2fa, mfa
- Original Extracted Source: original extracted web-security-wiki source/auth-2fa.md
Description:
Bypass two-factor authentication
Prerequisites:
- 2FA enabled
Execution Outline:
1. Direct access
2. Verification code brute force
3. Logic bypass
## CAPTCHA Bypass
- ID: auth-captcha
- Difficulty: beginner
- Subcategory: CAPTCHA
- Tags: auth, captcha, bypass
- Original Extracted Source: original extracted web-security-wiki source/auth-captcha.md
Description:
Bypass graphical CAPTCHA
Prerequisites:
- A CAPTCHA exists
Execution Outline:
1. Reuse
2. Null value bypass
3. Remove parameter
## Remember Me Vulnerabilities
- ID: auth-remember-me
- Difficulty: intermediate
- Subcategory: Session Management
- Tags: auth, remember-me, cookie
- Original Extracted Source: original extracted web-security-wiki source/auth-remember-me.md
Description:
Remember Me feature vulnerabilities
Prerequisites:
- Remember Me enabled
Execution Outline:
1. Cookie forgery
2. Base64 decoding
3. Remember Me Token reverse analysis
4. Shiro RememberMe deserialization RCE
## JWT Authentication Vulnerabilities
- ID: auth-jwt
- Difficulty: intermediate
- Subcategory: JWT
- Tags: auth, jwt, token
- Original Extracted Source: original extracted web-security-wiki source/auth-jwt.md
Description:
Exploit JWT (JSON Web Token) implementation flaws to forge or tamper with authentication tokens, achieving unauthorized access or privilege escalation
Prerequisites:
- Target uses JWT for authentication
- JWT tokens can be obtained or intercepted
- The JWT library has known vulnerabilities or the server is misconfigured
Execution Outline:
1. JWT decoding and analysis
2. Algorithm None attack
3. HS256 key brute force
4. RS256→HS256 algorithm confusion attack
