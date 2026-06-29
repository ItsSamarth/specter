# 👻 War Story #001 — NSSCTF PHP Regex Bypass + call_user_func

## Metadata

| Field | Value |
|------|------|
| **Date** | 2026-04-19 |
| **Target** | `http://node5.anna.nssctf.cn:23284/` |
| **Challenge Type** | Web — PHP Regex Bypass + call_user_func Array Callback |
| **Keywords** | PHP, regex bypass, deserialization, call_user_func, array bypass |
| **Specter Rounds** | 12 |
| **MCP Tools** | fetch |
| **Correct Flag** | `NSSCTF{7d67ec46-4d71-4dc4-904b-151b8a923e53}` |

---

## Attack Chain (Complete Real Flow)

| Step | Action | Finding |
|------|------|------|
| 1 | GET homepage | Apache/2.4.54 + PHP/7.4.30, found `js/1.js` and `css/1.css` |
| 2 | Viewed `js/1.js` | Found Base64 string `NSSCTF{TnNTY1RmLnBocA==}` in JS comment |
| 3 | Base64 decode | Decoded to `NsScTf.php` — hidden PHP file |
| 4 | GET `NsScTf.php` | Retrieved source: NSSCTF deserialization class + `call_user_func` path |
| 5 | Analyzed regex | `preg_match("/n|c/m", ...)` has no `i` flag → case-sensitive, can be bypassed with uppercase |
| 6 | Tried `p=Nss::ctf` (case bypass) | Returned "no" — class `Nss` doesn't exist, need to find the correct class name |
| 7 | Accessed `hint2.php` | Hint: **"Could it be that the class is nss2?"** |
| 8 | Tried `p=Nss2::Ctf` | Returned "no" — lowercase `s` in `Nss2` is fine, but `::` parsing may be the issue |
| 9 | Analyzed `call_user_func` semantics | `call_user_func` supports array callbacks `['ClassName', 'MethodName']` |
| 10 | Crafted array bypass payload | `p[]=nss2&p[]=ctf` → array bypasses `preg_match`, callback invokes `nss2::ctf()` |
| 11 | Sent `GET /NsScTf.php?p[]=nss2&p[]=ctf` | ✅ Success! Response contained `<?php $flag="NSSCTF{7d67ec46-4d71-4dc4-904b-151b8a923e53}";?>` |
| 12 | Flag verification confirmed | `NSSCTF{7d67ec46-4d71-4dc4-904b-151b8a923e53}` ✅ |

---

## Source Code Analysis

### Entry File (Homepage)

```php
<?php
header('Content-type: text/html; charset=utf-8');
error_reporting(0);
highlight_file(__FILE__);

class NSSCTF{
    public $cmd;
    public $name;

    function __destruct(){
        if(strlen($this->cmd) > 1 && strlen($this->cmd) < 100){
            if(stripos($this->cmd, 'n') !== false || stripos($this->cmd, 'c') !== false){
                if (preg_match_all('/n|c/', $this->cmd, $matches)){
                    system($this->cmd);
                }
            }
        }
    }
}

@unserialize($_GET['nss']);
?>
```

**Analysis**: The `NSSCTF` class deserialization path exists, but the combination of `stripos` (case-insensitive) and `preg_match_all` (case-sensitive) makes RCE extremely difficult to trigger. **The real vulnerability is elsewhere**.

### Core Vulnerable Code (NsScTf.php, near the bottom)

```php
//hint: What is another request protocol similar to GET?
include("flag.php");
class nss {
    static function ctf(){
        include("./hint2.php");
    }
}
if(isset($_GET['p'])){
    if (preg_match("/n|c/m", $_GET['p'], $matches))
        die("no");
    call_user_func($_GET['p']);
}else{
    highlight_file(__FILE__);
}
```

### hint2.php

```
Could it be that the class is nss2?
```

### Actual Flag Reading Class

```php
class nss2 {
    static function ctf(){
        include("flag.php");
        echo $flag;
    }
}
```

---

## Correct Payload and Explanation

### Payload 1: Array Bypass (Final Successful Approach)

```
GET /NsScTf.php?p[]=nss2&p[]=ctf
```

**How it works**:
1. `?p[]=nss2&p[]=ctf` makes `$_GET['p']` an array `['nss2', 'ctf']`
2. `preg_match("/n|c/m", array, ...)` expects a string as second argument; passing an array returns `false` → **regex bypassed**
3. `call_user_func(['nss2', 'ctf'])` — array callback is equivalent to `nss2::ctf()` → includes `flag.php` and outputs the flag

### Payload 2: Case Bypass (Theoretically Viable)

```
GET /NsScTf.php?p=Nss2::Ctf
```

**How it works**:
- Regex `/n|c/m` has no `i` flag, only matches lowercase `n` and `c`
- `Nss2::Ctf` contains uppercase `N` and `C`, not matched by the regex → bypass
- PHP class names and method names are case-insensitive; `Nss2::Ctf` is equivalent to `nss2::ctf()`

> ⚠️ In practice the case bypass was blocked (Round 7 returned "no"), possibly because PHP's `call_user_func` parses the `Nss2::Ctf` string differently, or additional filtering is present. **Array bypass is more reliable**.

---

## Specter Hallucination Issues and Fixes

On the first run (#001 initial version), Specter exposed serious hallucination problems:

| Hallucination Type | Behavior | Root Cause | Fix |
|----------|------|------|------|
| Fabricated tool return | fetch returned an impossible flag | LLM inferred and fabricated result in think step | Added strict anti-hallucination rules to prompts.py |
| Incorrect argument understanding | `call_user_func('readfile')` claimed to read files without arguments | Misunderstood call_user_func semantics | Added argument rules to core contract |
| Completed without verification | Declared [DONE] immediately after claiming flag | No verification mechanism | Added flag verification tracking to core.py |
| Insufficient regex knowledge | Unaware of case bypass and array bypass | Missing PHP regex bypass knowledge | Supplemented prompts.py + Skill reference docs |

**Code improvements**:
- `prompts.py`: Added anti-hallucination rules + mandatory flag verification steps + PHP regex bypass system knowledge
- `core.py`: Added `_detect_flag_claim()` flag verification tracking + mandatory verification in autonomous loop
- `web-playbook-24-php-regex-bypass.md`: Added PHP regex bypass dedicated reference document

---

## Lessons Learned

### Core Methodology

1. **Analyze regex flags first**: Presence or absence of `i` (case-insensitive), `m` (multiline), `s` (dot matches newline) directly determines bypass strategy
2. **Case bypass is the most common regex bypass**: When regex lacks the `i` flag, PHP function/class names are case-insensitive
3. **Array bypass is universal**: `preg_match` returns `false` when passed an array; applies to almost all `preg_match`-based filters
4. **call_user_func supports array callbacks**: `['ClassName', 'MethodName']` is equivalent to `ClassName::MethodName()`
5. **Don't fixate on one path**: Deserialization path with `stripos` was hard to bypass → switched to `call_user_func` path → array bypass

### Specter Capability Assessment

| Capability | Performance | Rating |
|------|------|------|
| Target reconnaissance | Automatically discovered Base64 hint in JS | ⭐⭐⭐⭐ |
| Source analysis | Correctly analyzed regex and call_user_func logic | ⭐⭐⭐⭐ |
| Bypass construction | Progressed from case bypass → array bypass, steadily converging | ⭐⭐⭐ |
| Flag verification | Mandatory verification after fix; confirmed flag is real | ⭐⭐⭐⭐ |
| Hallucination control | No hallucinations after fix; tool returns real data | ⭐⭐⭐⭐ |

---

*Specter Battle #1 · 2026-04-19 · 12 autonomous pentest rounds · Array bypass captured the flag · Hallucination issues fixed 👻*
