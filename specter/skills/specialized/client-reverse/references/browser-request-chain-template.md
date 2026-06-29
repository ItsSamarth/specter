# Browser Request Chain Template

Use this template for browser-side sign, token, anti-bot, worker, wasm, cookie-hop, and replay tasks.

## Template

```markdown
# Browser Request Chain Record

## Basic Information

- Target page:
- Target request:
- Target field:
- Trigger action:
- Current stage: locate / recover / runtime / validation
- Current status: 🟡 In progress / ✅ Closed loop / ⛔ Blocked
- Goal:
- Constraints:

## Samples and Observations

- Normal-state sample:
- Risk-control-state sample:
- Browser observation:
- Local observation:
- Current difference:

## Request Chain Master Table

| Item | Content |
| --- | --- |
| writer |  |
| builder |  |
| entry |  |
| source |  |
| Upstream dependency |  |
| State carrier |  |
| Risk-control branch point |  |
| Current conclusion |  |

## Key Evidence

| Evidence type | Location/point | Content | Conclusion |
| --- | --- | --- | --- |
| Request sample |  |  |  |
| Call stack |  |  |  |
| Breakpoint/Hook |  |  |  |
| Intermediate value |  |  |  |
| Cookie/Storage |  |  |  |

## Stage Supplements

### Locate Supplement

- Sink:
- Real write point:
- Upstream request:
- Normal-state / risk-control-state distinction:

### Recover Supplement

- Obfuscation layer type:
- Current recovery level: A / B / C
- Recovered contracts:
- Still-unrecovered gaps:

### Runtime Supplement

- Missing objects:
- Missing state:
- Fixed source:
- First divergence point:
- Risk control / anti-debugging:

### Validation Supplement

| Checkpoint | Browser side | Local/recovery side | Result | Evidence | Gap |
| --- | --- | --- | --- | --- | --- |
| Checkpoint 1 |  |  |  |  |  |

## Burp Replay Baseline

- Method:
- Path:
- Query:
- Headers:
- Body:
- Fields that must be preserved:
- Mutable fields:
- Prerequisite state:

## Stage Handoff

--- Stage Handoff ---
From:
To:
Proven:
Open:
Invalidated:

## Next Steps

- Next action:
- Expected output:
- Blockers:
```

## Minimum Required Fields

Even in a compact record, keep:

- target page and target request
- current stage
- `writer / builder / entry / source`
- one real request sample
- one concrete evidence row
- Burp replay baseline or explicit blocker
