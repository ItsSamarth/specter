# 👻 War Stories — Specter Field Experience Library

This is where Specter's real-world penetration test / CTF write-ups are kept.

Each write-up records the complete attack chain: from reconnaissance to the final flag, including which dead ends were taken and where the key breakthrough was.

## File Naming Convention

```
YYYY-MM-DD_challenge-type_keyword.md
```

For example: `2026-04-19_php-deserialization_regex-bypass.md`

## Write-up Template

Each write-up should include:

| Section | Content |
|------|------|
| **Metadata** | Date, target, type, keywords, number of rounds, toolchain |
| **Attack chain** | What was done at each step, what was discovered |
| **Key breakthrough** | Which step was decisive, and why |
| **Dead ends** | Which attempts failed, and the reasons |
| **Payload** | The final reproducible exploit code |
| **Lessons learned** | Methodology that transfers to similar challenges |

## Write-up Index

| Date | Challenge | Type | Rounds | Link |
|------|------|------|------|------|
| 2026-04-19 | NSSCTF PHP regex bypass | Web / PHP / regex bypass | 14 | [→](./2026-04-19_php-deserialization_regex-bypass.md) |
