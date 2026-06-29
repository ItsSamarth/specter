# JWT Security
English: JWT Security
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## JWT None Algorithm Attack
- ID: jwt-none-attack
- Difficulty: beginner
- Subcategory: Algorithm Attacks
- Tags: JWT, none algorithm, authentication bypass, token forgery, CVE-2015-2951
- Original Extracted Source: original extracted web-security-wiki source/jwt-none-attack.md
Description:
Exploit the flaw in JWT libraries that support the "none" algorithm: change the signature algorithm in the JWT header to none and remove the signature portion, constructing a forged token that passes verification without requiring any key. This is one of the most classic JWT vulnerabilities.
Prerequisites:
- Target uses JWT for authentication
- jwt_tool or the Python PyJWT library
Execution Outline:
1. 1. Decode the existing JWT
2. 2. Construct a None-algorithm JWT
3. 3. Automated attack with jwt_tool
4. 4. Verify the forged token
## JWT Key Confusion Attack (RS→HS)
- ID: jwt-key-confusion
- Difficulty: advanced
- Subcategory: Algorithm Attacks
- Tags: JWT, key confusion, RS256, HS256, algorithm tampering
- Original Extracted Source: original extracted web-security-wiki source/jwt-key-confusion.md
Description:
When the server uses an RSA public key to verify a JWT, the attacker changes the algorithm from RS256 to HS256. The server then mistakenly uses the RSA public key as the HMAC key for verification. Because the RSA public key is public, the attacker can use it to sign arbitrary JWTs.
Prerequisites:
- Target JWT uses the RS256/RS384/RS512 algorithm
- RSA public key already obtained
- jwt_tool or Python
Execution Outline:
1. 1. Obtain the RSA public key
2. 2. Key confusion attack
3. 3. Automated attack with jwt_tool
4. 4. JWKS endpoint injection
## JWT Secret Brute Force
- ID: jwt-secret-bruteforce
- Difficulty: intermediate
- Subcategory: Key Cracking
- Tags: JWT, secret brute force, HS256, weak key, hashcat
- Original Extracted Source: original extracted web-security-wiki source/jwt-secret-bruteforce.md
Description:
When a JWT uses an HMAC symmetric algorithm (HS256/HS384/HS512) and the secret is a weak password, the signing key can be recovered through dictionary or brute-force cracking, allowing arbitrary JWT tokens to be forged.
Prerequisites:
- Target JWT uses an HMAC algorithm (HS256, etc.)
- A valid JWT sample already obtained
- hashcat or jwt_tool
Execution Outline:
1. 1. Confirm the algorithm and structure
2. 2. GPU-accelerated brute force with hashcat
3. 3. Dictionary brute force with jwt_tool
4. 4. Forge a JWT using the cracked secret
## JWT JKU/X5U Header Injection
- ID: jwt-jku-x5u-injection
- Difficulty: advanced
- Subcategory: Header Injection
- Tags: JWT, JKU, X5U, Header injection, JWKS, key hijacking
- Original Extracted Source: original extracted web-security-wiki source/jwt-jku-x5u-injection.md
Description:
Exploit the jku (JWK Set URL) or x5u (X.509 URL) parameter in the JWT header to point the key source to an attacker-controlled server, causing the server to use the attacker's public key to verify the JWT and thereby achieving token forgery.
Prerequisites:
- Target JWT supports the jku/x5u header parameter
- Attacker owns a public-facing server
- Python environment
Execution Outline:
1. 1. Probe for JKU/X5U support
2. 2. Generate the attacker key pair
3. 3. Host the JWKS and sign the JWT
4. 4. Verify the attack
