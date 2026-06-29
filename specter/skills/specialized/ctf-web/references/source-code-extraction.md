# CTF Web Source Code Extraction Methods

## Core Understanding

- CTF Web challenges commonly use `highlight_file(__FILE__)` to display source code, which outputs HTML with syntax highlighting
- Some challenges only expose partial source in HTML comments or hidden elements — this is intentional
- **Source code is an important clue, but not the only one** — some challenges hide key entry points in robots.txt, response headers, or hidden files

---

## Method 1: strip_tags Extraction (Preferred for highlight_file scenarios)

**When to use**: Pages displaying source via `highlight_file()` / `show_source()`

```python
import requests, re
r = requests.get(url)
# Strip all HTML tags to get plain text
clean = re.sub(r'<[^>]+>', '', r.text)
# Optional: remove excess blank lines
clean = re.sub(r'\n{3,}', '\n\n', clean)
print(clean)
```

**Notes**:
- Removes all HTML tags; any HTML strings in the source itself will also be stripped
- The HTML-highlighted output from the fetch tool **is not suitable for direct visual reconstruction** — use python_execute to verify

---

## Method 2: php://filter Source Extraction

**When to use**: Scenarios with file inclusion vulnerabilities (`include`/`require`)

```
?page=php://filter/convert.base64-encode/resource=index.php
?page=php://filter/read=convert.base64-encode/resource=flag.php
```

After obtaining the base64-encoded source:
```python
import base64
source = base64.b64decode(base64_string).decode('utf-8')
print(source)
```

---

## Method 3: .phps Extension

**When to use**: Server is configured to serve PHP source

```
/learning.phps
/index.phps
```

---

## Method 4: Backup Files / Version Control Leaks

| Path | Notes |
|------|-------|
| `.git/HEAD` | Git repository leak |
| `.svn/entries` | SVN repository leak |
| `index.php.bak` | Backup file |
| `index.php~` | Editor temp file |
| `www.zip` / `web.tar.gz` | Full-site archive |
| `.index.php.swp` | Vim swap file |

---

## Method 5: HTML Comments and Hidden Elements

Some challenges put source code or hints inside HTML comments:

```python
import requests, re
r = requests.get(url)
# Extract HTML comment content
comments = re.findall(r'<!--(.*?)-->', r.text, re.DOTALL)
for c in comments:
    print(c)
```

---

## Method 6: Response Headers and Cookies

Some challenges hide hints in response headers:

```python
import requests
r = requests.get(url)
print("Headers:", dict(r.headers))
print("Cookies:", dict(r.cookies))
```

---

## Source Code Integrity Check

After extracting source, verify it's complete:

| Check | Notes |
|-------|-------|
| Brace matching | Unclosed `}` after `if` may indicate truncation, or may be intentional |
| Output statements | If no `echo`/`print`/`die`, there may be unseen code |
| Dangerous functions | If no `eval`/`system` etc., the RCE entry point may be on another page |

**Note**: Incomplete source has two possible causes —
1. Extraction method has an issue → try a different method
2. The challenge intentionally exposes only this much → explore other clues (other pages, parameters, files)
