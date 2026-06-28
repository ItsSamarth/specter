# WebSocket Security
English: WebSocket Security
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Cross-Site WebSocket Hijacking (CSWSH)
- ID: ws-hijack
- Difficulty: intermediate
- Subcategory: WebSocket Hijacking
- Tags: WebSocket, CSWSH, Origin, cross-site, session hijacking
- Original Extracted Source: original extracted web-security-wiki source/ws-hijack.md
Description:
Exploit the vulnerability of missing Origin validation during the WebSocket handshake phase, establishing a cross-site WebSocket connection via a malicious web page. The attacker can hijack the victim's WebSocket session, steal real-time data, or send messages as the victim. Similar to CSRF but targeting the WebSocket protocol.
Prerequisites:
- The target uses WebSocket communication
- The WebSocket handshake does not validate Origin
Execution Outline:
1. 1. Identify WebSocket endpoints
2. 2. Construct a cross-site hijacking POC page
3. 3. WebSocket message injection
4. 4. WebSocket traffic analysis script
## WebSocket Smuggling Attack
- ID: ws-smuggling
- Difficulty: expert
- Subcategory: WebSocket Smuggling
- Tags: WebSocket, smuggling, reverse proxy, H2C, intranet pivoting
- Original Extracted Source: original extracted web-security-wiki source/ws-smuggling.md
Description:
Exploit differences in how reverse proxies / load balancers handle the WebSocket protocol to smuggle HTTP requests to internal network services via a WebSocket upgrade request. The attacker can bypass front-end security controls and communicate directly with the backend, accessing protected internal APIs or management interfaces.
Prerequisites:
- The target uses a reverse proxy (Nginx/Varnish, etc.)
- The proxy allows WebSocket upgrades
- Internal services exist behind the backend
Execution Outline:
1. 1. Detect WebSocket smuggling feasibility
2. 2. WebSocket tunnel construction
3. 3. H2C smuggling to bypass access control
4. 4. Reverse proxy discrepancy exploitation
## WebSocket Authentication and Authorization Bypass
- ID: ws-auth-bypass
- Difficulty: intermediate
- Subcategory: Authentication Bypass
- Tags: WebSocket, authentication, authorization, privilege bypass, token replay
- Original Extracted Source: original extracted web-security-wiki source/ws-auth-bypass.md
Description:
Exploit the vulnerability of missing continuous authentication checks after a WebSocket connection is established, bypassing authentication and authorization mechanisms via session fixation, token replay, unauthorized channel subscription, and similar techniques. The long-lived nature of WebSocket connections means the original connection can retain access even after permissions change.
Prerequisites:
- The target uses WebSocket real-time communication
- A valid session/Token has already been obtained
Execution Outline:
1. 1. WebSocket authentication mechanism analysis
2. 2. Token replay and session fixation
3. 3. Unauthorized channel/room subscription
4. 4. WebSocket rate limiting and DoS testing

