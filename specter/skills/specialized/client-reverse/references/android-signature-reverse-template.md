# Android Signature Reverse Template

Use this template for Android sign, token, encrypt, decrypt, JNI, interceptor, and replay tasks.

## Template

```markdown
# Android Signature Reverse-Engineering Record

## Basic Information

- APK / package name:
- Target feature:
- Target request:
- Target field:
- Current phase: static / dynamic / native / replay
- Current status: 🟡 In progress / ✅ Closed out / ⛔ Blocked
- Goal:
- Constraints:

## Static Overview

| Item | Content |
| --- | --- |
| Manifest entry |  |
| Application |  |
| Main Activity / target component |  |
| Main package structure |  |
| Network framework |  |
| DI framework |  |
| Current conclusion |  |

## Request Call Chain

```text
Activity / Fragment / Service
-> ViewModel / Presenter / UseCase
-> Repository / DataSource
-> ApiService / RequestBuilder / Interceptor
-> Signer / Encryptor / Serializer
```

- Actual call chain:
- Request Method / Path:
- Header write points:
- Body write points:
- Sign input convergence point:
- Sequence / preconditions:

## Sign / Crypto Location

| Item | Content |
| --- | --- |
| Sign class / method |  |
| Encrypt class / method |  |
| Key constants |  |
| Key Header |  |
| Key Token / Device value |  |
| Java-only / Java+JNI / Native-first |  |

## Dynamic Verification

| Hook point | Reason | Captured content | Result |
| --- | --- | --- | --- |
| Hook1 |  |  |  |

- URL:
- Headers:
- Body:
- Sign input:
- Sign output:
- Proxy verification:

## JNI / SO Analysis

| Item | Content |
| --- | --- |
| Java native entry |  |
| SO name |  |
| JNI type | static / dynamic |
| Input parameters |  |
| Output role | final sign / intermediate token / other |
| Deeper RE needed |  |

## Burp Replay Baseline

- Method:
- Path:
- Query:
- Headers:
- Body:
- Fields that must be preserved:
- Mutable fields:
- Precondition state:
- Whether device / Hook / App assistance is needed:

## Conclusion

- Current closure level:
- Remaining blockers:
- Next-step recommendations:
```

## Minimum Required Fields

Even in a compact record, keep:

- APK or package
- target request
- real call-flow summary
- network stack
- sign or crypto location
- Java versus JNI conclusion
- one runtime hook or explicit reason why runtime is not needed
- Burp replay baseline or explicit blocker
