# Business Logic Vulnerabilities
English: Business Logic Vulnerabilities
- Entry Count: 5
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## IDOR - Unauthorized Access
- ID: biz-idor
- Difficulty: beginner
- Subcategory: Unauthorized Access Vulnerability
- Tags: IDOR, unauthorized-access, business-logic, OWASP, A01
- Original Extracted Source: original extracted web-security-wiki source/biz-idor.md
Description:
Insecure Direct Object Reference (IDOR): gaining unauthorized access to other users' data by tampering with object IDs in request parameters. Attackers can enumerate user IDs, order numbers, and other parameters to access unauthorized resources.
Prerequisites:
- Target has resource access interfaces based on IDs
- A regular user account is already logged in
Execution Outline:
1. 1. Identify enumerable parameters
2. 2. Horizontal privilege escalation testing
3. 3. Vertical privilege escalation testing
4. 4. Parameter pollution for unauthorized access
## Race Condition Attack
- ID: biz-race-condition
- Difficulty: intermediate
- Subcategory: Race Condition
- Tags: race-condition, Race-Condition, TOCTOU, concurrency, business-logic
- Original Extracted Source: original extracted web-security-wiki source/biz-race-condition.md
Description:
Exploiting server-side TOCTOU (Time-of-Check to Time-of-Use) vulnerabilities via concurrent requests to trigger the same operation multiple times within the time window between check and execution, achieving business logic bypasses such as duplicate coupon redemption, repeated withdrawals, and over-purchasing.
Prerequisites:
- Target has quantifiable resource operations such as balance/points/coupons
- Python/Turbo Intruder environment
Execution Outline:
1. 1. Identify race condition targets
2. 2. Python concurrent test script
3. 3. Burp Turbo Intruder testing
4. 4. Verify race condition success
## Payment Logic Tampering
- ID: biz-payment-tamper
- Difficulty: intermediate
- Subcategory: Payment Security
- Tags: payment, amount-tampering, business-logic, zero-purchase, e-commerce-security
- Original Extracted Source: original extracted web-security-wiki source/biz-payment-tamper.md
Description:
Manipulating transaction logic by modifying payment parameters such as amount, quantity, and discount in payment requests. Common in e-commerce platforms and online payment systems, can lead to serious business risks such as zero-cost purchases, negative prices, and stacked discounts.
Prerequisites:
- Target has payment/order functionality
- HTTP requests can be intercepted and modified
Execution Outline:
1. 1. Amount tampering test
2. 2. Quantity and shipping fee tampering
3. 3. Coupon stacking and substitution
4. 4. Payment callback tampering
## Password Reset Logic Flaws
- ID: biz-password-reset
- Difficulty: intermediate
- Subcategory: Authentication Flaw
- Tags: password-reset, authentication-bypass, business-logic, captcha, Host-injection
- Original Extracted Source: original extracted web-security-wiki source/biz-password-reset.md
Description:
Logic vulnerabilities in password reset flows, including reset token leakage, captcha brute force, response manipulation, and Host header injection attacks, allowing arbitrary user password resets.
Prerequisites:
- Target has password reset/recovery functionality
- HTTP requests can be intercepted
Execution Outline:
1. 1. Host header injection to steal reset link
2. 2. Captcha brute force
3. 3. Response manipulation bypass
4. 4. Weak randomness in reset tokens
## Captcha Bypass Techniques
- ID: biz-captcha-bypass
- Difficulty: beginner
- Subcategory: Captcha Security
- Tags: captcha, CAPTCHA, bypass, SMS-captcha, human-verification
- Original Extracted Source: original extracted web-security-wiki source/biz-captcha-bypass.md
Description:
Various techniques for bypassing human verification mechanisms such as graphic captchas, SMS captchas, and slider verification, including response leakage, replay attacks, OCR recognition, and logic flaw exploitation.
Prerequisites:
- Target has captcha-protected functionality
- Python environment
Execution Outline:
1. 1. Captcha response leakage
2. 2. Captcha replay attack
3. 3. Delete captcha parameter
4. 4. Universal captcha
