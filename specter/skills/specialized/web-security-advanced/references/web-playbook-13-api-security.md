# API Security
English: API Security
- Entry Count: 12
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## JWT Security Vulnerabilities
- ID: jwt-security
- Difficulty: intermediate
- Subcategory: JWT
- Tags: jwt, token, authentication
- Original Extracted Source: original extracted web-security-wiki source/jwt-security.md
Description:
JSON Web Token security vulnerability exploitation
Prerequisites:
- JWT is used for authentication
- JWT configuration or validation has issues
Execution Outline:
1. 1. Decode JWT
2. 2. None algorithm attack
3. 3. Weak key cracking
4. 4. Key confusion attack
## GraphQL Injection Attack
- ID: graphql-injection
- Difficulty: intermediate
- Subcategory: GraphQL
- Tags: graphql, api, injection, introspection
- Original Extracted Source: original extracted web-security-wiki source/graphql-injection.md
Description:
GraphQL API injection and information disclosure attacks
Prerequisites:
- Target uses GraphQL API
- Unauthorized access or injection point exists
Execution Outline:
1. 1. Probe GraphQL endpoint
2. 2. Introspection query
3. 3. Batch query attack
4. 4. SQL injection
## GraphQL Introspection Attack
- ID: graphql-introspection
- Difficulty: beginner
- Subcategory: GraphQL Introspection
- Tags: graphql, introspection, enumeration, api
- Original Extracted Source: original extracted web-security-wiki source/graphql-introspection.md
Description:
Using GraphQL introspection to obtain API schema
Prerequisites:
- Target uses GraphQL
- Introspection is not disabled
Execution Outline:
1. 1. Basic introspection
2. 2. Full introspection
3. 3. Use tools to analyze
## GraphQL Batch Query Attack
- ID: graphql-batching
- Difficulty: intermediate
- Subcategory: GraphQL Batch Query
- Tags: graphql, batching, rate-limit, bypass
- Original Extracted Source: original extracted web-security-wiki source/graphql-batching.md
Description:
Using GraphQL batch queries to bypass rate limits
Prerequisites:
- Target uses GraphQL
- Rate limiting is in place
Execution Outline:
1. 1. Alias batch query
2. 2. Array batch query
3. 3. Brute force
## REST API Security Testing
- ID: rest-api-security
- Difficulty: intermediate
- Subcategory: REST API
- Tags: rest, api, security, testing
- Original Extracted Source: original extracted web-security-wiki source/rest-api-security.md
Description:
REST API security testing and vulnerability exploitation
Prerequisites:
- Target uses REST API
- API endpoints are known
Execution Outline:
1. 1. API endpoint discovery
2. 2. Authentication testing
3. 3. HTTP method testing
4. 4. Parameter pollution
## JWT None Algorithm Attack
- ID: jwt-none-alg
- Difficulty: beginner
- Subcategory: JWT Security
- Tags: jwt, none, algorithm, bypass
- Original Extracted Source: original extracted web-security-wiki source/jwt-none-alg.md
Description:
Bypassing signature verification using JWT None algorithm
Prerequisites:
- Target uses JWT authentication
- Server does not properly validate the algorithm
Execution Outline:
1. 1. Decode JWT
2. 2. Construct None algorithm token
3. 3. Modify user permissions
4. 4. Send malicious token
## JWT Key Confusion Attack
- ID: jwt-key-confusion
- Difficulty: intermediate
- Subcategory: JWT Security
- Tags: jwt, algorithm, confusion, rs256
- Original Extracted Source: original extracted web-security-wiki source/jwt-key-confusion.md
Description:
Bypassing signature using JWT algorithm confusion
Prerequisites:
- Target uses RS256 algorithm
- Public key can be obtained
Execution Outline:
1. 1. Obtain public key
2. 2. Algorithm confusion attack
3. 3. Send malicious token
## IDOR - Insecure Direct Object Reference
- ID: api-idor
- Difficulty: beginner
- Subcategory: IDOR
- Tags: idor, api, authorization, bypass
- Original Extracted Source: original extracted web-security-wiki source/api-idor.md
Description:
Using IDOR vulnerabilities to access unauthorized resources
Prerequisites:
- Target uses ID-based resource references
- Authorization check is flawed
Execution Outline:
1. 1. Identify ID parameters
2. 2. Enumerate IDs
3. 3. Batch detection
4. 4. Cross-user access
## API Rate Limit Bypass
- ID: api-rate-limit
- Difficulty: intermediate
- Subcategory: Rate Limiting
- Tags: api, rate-limit, bypass, brute-force
- Original Extracted Source: original extracted web-security-wiki source/api-rate-limit.md
Description:
Bypassing API rate limits for brute force attacks
Prerequisites:
- Target has rate limiting
- Rate limit implementation is flawed
Execution Outline:
1. 1. Detect rate limiting
2. 2. IP bypass
3. 3. Distributed bypass
4. 4. Other bypass techniques
## Mass Assignment Vulnerability
- ID: api-mass-assignment
- Difficulty: beginner
- Subcategory: Mass Assignment
- Tags: api, mass-assignment, privilege-escalation
- Original Extracted Source: original extracted web-security-wiki source/api-mass-assignment.md
Description:
Using mass assignment vulnerabilities to modify sensitive fields
Prerequisites:
- API accepts JSON input
- Unfiltered fields exist
Execution Outline:
1. 1. Identify input fields
2. 2. Add sensitive fields
3. 3. Update operation
4. 4. Nested objects
## BOLA - Broken Object Level Authorization
- ID: api-bola
- Difficulty: intermediate
- Subcategory: BOLA
- Tags: api, bola, authorization, idor
- Original Extracted Source: original extracted web-security-wiki source/api-bola.md
Description:
Using BOLA vulnerabilities to access unauthorized objects
Prerequisites:
- API uses object IDs
- Authorization check is flawed
Execution Outline:
1. 1. Identify object access
2. 2. Test authorization
3. 3. Lateral access
4. 4. Modify/delete operations
## API Injection Attacks
- ID: api-injection
- Difficulty: intermediate
- Subcategory: API Injection
- Tags: api, injection, sqli, nosqli
- Original Extracted Source: original extracted web-security-wiki source/api-injection.md
Description:
Various injection attacks against API endpoints
Prerequisites:
- API accepts user input
- Input is not properly filtered
Execution Outline:
1. 1. SQL injection
2. 2. NoSQL injection
3. 3. LDAP injection
4. 4. Command injection
