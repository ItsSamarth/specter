# Prototype Pollution
English: Prototype Pollution
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Server-Side Prototype Pollution to RCE
- ID: proto-server-rce
- Difficulty: advanced
- Subcategory: Server-Side Exploitation
- Tags: Prototype Chain, Prototype Pollution, RCE, Node.js, __proto__
- Original Extracted Source: original extracted web-security-wiki source/proto-server-rce.md
Description:
By polluting the JavaScript object prototype chain (__proto__/constructor.prototype) to inject malicious properties, achieve remote code execution on the Node.js server side by leveraging gadget chains in child_process or template engines such as EJS/Pug.
Prerequisites:
- Target uses Node.js
- A JSON merge/deep-copy operation exists
- Controllable JSON input
Execution Outline:
1. 1. Detect the prototype pollution sink
2. 2. EJS template engine RCE gadget
3. 3. Pug template engine RCE gadget
4. 4. Generic DoS/information disclosure gadget
## Client-Side Prototype Pollution to XSS
- ID: proto-client-xss
- Difficulty: advanced
- Subcategory: Client-Side Exploitation
- Tags: Prototype Chain, XSS, Client-Side, jQuery, DOM, Prototype Pollution
- Original Extracted Source: original extracted web-security-wiki source/proto-client-xss.md
Description:
Pollute the front-end JavaScript prototype chain via URL parameters, postMessage, or DOM manipulation, and use gadgets in jQuery/DOM manipulation libraries to achieve XSS on the client side. An attacker can lure a victim into triggering the vulnerability through a carefully crafted URL link.
Prerequisites:
- Target front-end uses a vulnerable JS library
- Logic that converts URL parameters into objects exists
Execution Outline:
1. 1. Identify the client-side pollution source
2. 2. jQuery html() gadget
3. 3. DOMPurify bypass gadget
4. 4. Automated detection script
## Prototype Pollution Combined with NoSQL Injection
- ID: proto-nosql-injection
- Difficulty: expert
- Subcategory: Combined Exploitation
- Tags: Prototype Chain, NoSQL, MongoDB, Authentication Bypass, Combined Attack
- Original Extracted Source: original extracted web-security-wiki source/proto-nosql-injection.md
Description:
Combine prototype pollution with MongoDB/NoSQL injection. By polluting the prototype chain properties of the query object, bypass authentication logic or construct malicious query conditions to achieve authentication bypass and data leakage.
Prerequisites:
- Target uses MongoDB
- A prototype pollution sink exists
- Query construction logic exists
Execution Outline:
1. 1. Identify the MongoDB query injection point
2. 2. Bypass query validation via prototype pollution
3. 3. Extract data with boolean blind injection
4. 4. Database enumeration and exfiltration
