# Request Smuggling
English: Request Smuggling
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## CL-TE Request Smuggling
- ID: smuggling-cl-te
- Difficulty: advanced
- Subcategory: CL-TE
- Tags: smuggling, request, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-cl-te.md
Description:
Content-Length vs. Transfer-Encoding smuggling
Prerequisites:
- Target uses multiple proxy layers
- Front-end/back-end processing discrepancy
Execution Outline:
1. CL-TE basics
2. TE-CL basics
3. TE-TE
## CL-CL Smuggling
- ID: smuggling-cl-cl
- Difficulty: advanced
- Subcategory: CL-CL
- Tags: smuggling, cl-cl, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-cl-cl.md
Description:
Achieve HTTP request smuggling by exploiting the discrepancy in how a front-end proxy and back-end server both process the Content-Length header but handle multiple CL headers differently
Prerequisites:
- A front-end proxy (e.g. HAProxy/Nginx) + back-end server architecture exists
- The two ends parse the Content-Length header differently
- Understanding of HTTP request smuggling principles
Execution Outline:
1. Detect CL-CL smuggling conditions
2. CL-CL request smuggling PoC
3. Use CL-CL smuggling to bypass front-end access control
## TE-CL Smuggling
- ID: smuggling-te-cl
- Difficulty: expert
- Subcategory: TE-CL
- Tags: smuggling, te-cl, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-te-cl.md
Description:
Achieve HTTP request smuggling by exploiting the discrepancy where the front-end uses Transfer-Encoding while the back-end uses Content-Length
Prerequisites:
- The front-end proxy prioritizes Transfer-Encoding
- The back-end server prioritizes Content-Length
- Understanding of the chunked encoding format
Execution Outline:
1. Detect the TE-CL discrepancy
2. TE-CL smuggling PoC
3. TE-CL smuggling for request hijacking
## TE-TE Smuggling
- ID: smuggling-te-te
- Difficulty: expert
- Subcategory: TE-TE
- Tags: smuggling, te-te, http
- Original Extracted Source: original extracted web-security-wiki source/smuggling-te-te.md
Description:
Achieve request smuggling by exploiting how the front-end and back-end handle different obfuscated variants of the Transfer-Encoding header differently
Prerequisites:
- Both front-end and back-end support Transfer-Encoding
- The TE header can be obfuscated so that one end ignores it
- Understanding of chunked encoding and HTTP smuggling principles
Execution Outline:
1. Probe for TE obfuscation variants
2. TE-TE smuggling exploitation (front-end ignores the obfuscated TE)
3. TE-TE cache poisoning attack

