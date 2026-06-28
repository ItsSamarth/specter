# Cache & CDN Security
English: Cache & CDN Security
- Entry Count: 3
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## Cache Poisoning
- ID: cache-poisoning
- Difficulty: advanced
- Subcategory: Cache Poisoning
- Tags: cache, poisoning, web-cache
- Original Extracted Source: original extracted web-security-wiki source/cache-poisoning.md
Description:
Web cache poisoning attacks
Prerequisites:
- Target uses caching
- Cache key is misconfigured
Execution Outline:
1. Probe the cache
2. Unkeyed headers
3. Cache poisoning
4. Fat GET
## Cache Deception
- ID: cache-deception
- Difficulty: intermediate
- Subcategory: Deception
- Tags: cache, deception, auth
- Original Extracted Source: original extracted web-security-wiki source/cache-deception.md
Description:
Exploit discrepancies between web caches and server-side path parsing to trick the CDN/cache layer into caching dynamic pages containing sensitive information
Prerequisites:
- Target uses a CDN or reverse-proxy cache
- A path-parsing discrepancy exists (backend ignores the path suffix)
- Cache policy is based on the URL extension
Execution Outline:
1. Probe caching behavior
2. Path-confusion cache deception
3. Advanced cache deception variants
4. End-to-end attack flow validation
## CDN Bypass
- ID: cdn-bypass
- Difficulty: intermediate
- Subcategory: CDN
- Tags: cdn, bypass, recon
- Original Extracted Source: original extracted web-security-wiki source/cdn-bypass.md
Description:
Bypass the CDN to find the real IP
Prerequisites:
- Target uses a CDN
Execution Outline:
1. Historical DNS
2. Email headers
3. DNS history and certificate transparency queries
4. Probe the real IP via subdomains and related services

