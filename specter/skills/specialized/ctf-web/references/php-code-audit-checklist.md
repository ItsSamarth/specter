# PHP Code Audit Checklist

## Step 1: Identify Input Entry Points

### Superglobal Variables
```php
$_GET['param']        // URL query parameters
$_POST['param']       // POST form data
$_REQUEST['param']    // GET + POST + COOKIE
$_COOKIE['param']     // Cookie values
$_SERVER['HTTP_X']    // HTTP request headers
$_FILES['file']       // Uploaded files
$_SESSION['key']      // Session data (if controllable)
```

### Covert Inputs
```php
php://input           // Raw POST data
getallheaders()       // All HTTP headers
getenv()              // Environment variables
file_get_contents()   // Read from file/URL
```

## Step 2: Identify Dangerous Functions

### Code Execution
```php
eval()                // Execute arbitrary PHP code
assert()              // Can execute code on PHP < 7
preg_replace(/e)      // The /e modifier executes the replacement result
create_function()     // Create an anonymous function
call_user_func()      // Call a callback function
call_user_func_array()// Call a callback function (array arguments)
array_map()           // Apply a callback to array elements
usort()               // Custom sort (callback can be injected)
array_filter()        // Filter an array (callback can be injected)
```

### Command Execution
```php
system()              // Execute an external program, output the result
exec()                // Execute an external program, return the last line
shell_exec()          // Execute a command, return the full output
passthru()            // Execute an external program, output raw data
popen()               // Open a process pipe
proc_open()           // Open a process (more flexible)
pcntl_exec()          // Execute a program (requires the pcntl extension)
backticks `cmd`       // Equivalent to shell_exec()
```

### File Operations
```php
include() / require()          // File inclusion
include_once() / require_once()
file_get_contents()            // Read a file
file_put_contents()            // Write a file
fopen() + fread()              // Open and read
readfile()                     // Output file contents
highlight_file() / show_source()// Highlight source code
unlink()                       // Delete a file
rename()                       // Rename a file
copy()                         // Copy a file
move_uploaded_file()           // Move an uploaded file
```

### Deserialization
```php
unserialize()        // Deserialize an object
__wakeup()           // Called during deserialization
__destruct()         // Called when the object is destroyed
__toString()         // Called when the object is used as a string
__call()             // Triggered when calling a non-existent method
__get()              // Triggered when accessing a non-existent property
```

## Step 3: Analyze Filtering/Validation Logic

### Regex Filtering Analysis Checklist
```php
preg_match("/pattern/flags", $input)

□ Is there an i modifier?  → No → case bypass possible
□ Is there an m modifier?  → Yes → consider newline bypass of ^$
□ Is there an s modifier?  → Yes → . matches newlines
□ Is it checking a string or an array? → array bypass
□ Can backtracking be exceeded?  → PCRE backtracking limit bypass
```

### Common Filtering Functions
```php
str_replace()        // String replacement (double-write bypass possible)
str_ireplace()       // Case-insensitive replacement
strstr() / strpos()  // String search (case bypass / array bypass possible)
strlen()             // Length check (can be bypassed via quirks)
in_array()           // Array check (loose-type comparison)
is_numeric()         // Numeric check (hex / scientific notation)
intval()             // Integer conversion (quirk bypass)
trim()               // Trim whitespace (%0a%0d bypass)
htmlspecialchars()   // HTML escaping (does not escape single quotes by default)
addslashes()         // Add slashes (wide-byte/GBK bypass)
mysql_real_escape_string() // Escaping (wide-byte/GBK bypass)
```

## Step 4: Draw the Data Flow Diagram

```
User input → [Filter A] → [Filter B] → dangerous function
          ↓
          Filtered?
          ↓ No
          [Bypass check] → dangerous function executes
```

### Path Selection Principles
1. **Prefer the path with the least filtering**
2. **Prefer the path with the fewest parameters** (a 3-parameter path < a 5-parameter path)
3. **Prefer the path with visible results** (system() over exec())
4. **Prefer simpler bypasses** (case bypass < encoding bypass < chained bypass)

## Step 5: Output Visibility Analysis

### Confirm Whether Command Output Is Visible
```
1. system() output → directly in the HTTP response
2. exec() output → requires an extra echo
3. eval() + system() → output in the eval context
4. highlight_file() + system() → output after the source highlight
```

### Test First When Unsure
```php
// First test output visibility with a simple command
system('id');
system('echo TESTFLAG123');
// Search for TESTFLAG123 in the HTTP response
```

### Response Analysis Techniques
```python
# Use python_execute to analyze the response
import requests
r = requests.get(url, params=payload)
print(f"Status: {r.status_code}")
print(f"Length: {len(r.text)}")
print(f"Headers: {dict(r.headers)}")
# Look only at the last N characters (the flag is often at the end)
print(f"Tail: {r.text[-500:]}")
# Search for flag patterns
import re
flags = re.findall(r'(NSSCTF\{[^}]+\}|flag\{[^}]+\}|CTF\{[^}]+\})', r.text)
if flags:
    print(f"FLAG FOUND: {flags}")
```
