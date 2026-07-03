<div align="center">

# Specter 👻

> *AI-Powered Penetration Testing CLI — Speak plainly, find real bugs.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![OpenAI Compatible](https://img.shields.io/badge/API-OpenAI_Compatible-green)](https://platform.openai.com/)
[![MCP](https://img.shields.io/badge/Toolchain-MCP-orange)](https://modelcontextprotocol.io/)
[![PyPI](https://img.shields.io/badge/PyPI-v0.3.2-blueviolet)](https://pypi.org/project/specter/)
[![Security](https://img.shields.io/badge/Scope-Authorized_Only-red)](#-security-notice)
<br>

**This project is a standalone AI penetration testing Agent.**

<br>

Built on LLM Agent + MCP Toolchain + Pentest Skill orchestration,
compatible with OpenAI / MiniMax / DeepSeek and similar models.
Natural language input → automated "Recon → Vulnerability Discovery → Exploitation → Reporting".

[Quick Start](#quick-start) · [Architecture](#-architecture) · [Skills](#-built-in-skills)

</div>

---

## What It Does

Give it a natural language command and watch it run a full pentest:

```
User:   "Run a penetration test on http://target.example.com"

Specter executes:
  Round 1:  Recon → Fingerprinting, port scan, directory enumeration
  Round 2:  Vulnerability Discovery → Injection points, known CVEs, misconfigs
  Round 3:  Exploitation → PoC verification, access obtained
  Round 4:  Reporting → Structured report + Python PoC script
```

> 📸 **Screenshots coming soon** — Specter CLI and Web UI demos will be added to showcase the workflow in action.

Suitable for authorized pentests, CTF competitions, security training, and red team operations.

---

## Features

- **Natural Language Driven** — Describe your intent in plain English, it auto-identifies phases and tools
- **13 LLM Providers** — OpenAI / MiniMax / DeepSeek / Zhipu / Moonshot / Qwen / SiliconFlow / Doubao / Baichuan / StepFun / SenseTime / Yi, one-command switch
- **MCP Toolchain** — Ships with 11 MCP service configs and 23 tool definitions; `fetch` / `memory` currently run in stable `local` mode, while most other MCP integrations remain preview or placeholder until full session lifecycle management is completed
- **AI Agent Core** — OpenAI-compatible protocol + Tool Calling + autonomous pentest loop
- **21 Pentest Skills** — 7 core + 14 specialized skills (incl. CTF Web/Crypto/Misc, osint-recon, secknowledge-skill), 180 reference documents
- **Encode/Decode & Crypto Tools** — 29 operations (Base64/Hex/URL/AES/JWT/Morse etc.), LLM calls them directly, no guessing
- **Python Code Execution** — Built-in `python_execute` tool for payload crafting and response parsing; currently still a high-risk experimental capability, not a strong isolation sandbox
- **Persistent Pentesting** — Cyclic runs (100 rounds/cycle × 10 cycles = 1000 rounds), auto-reports every cycle, runs until you stop it
- **Thinking Process Control** — `think on/off` toggles LLM reasoning visibility, off by default for clean output
- **Sandbox Mode Prompting** — Unlocks AI security testing capabilities, designed for CTF and authorized pentest scenarios
- **Auto Report & PoC** — Generates structured Markdown reports and runnable Python PoC scripts
- **Web UI Mode** — `specter web` launches a local web interface for browser-based pentest operations, default `127.0.0.1:7788`
- **Security Knowledge Base** — Includes the KB module and baseline seed data today; retrieval augmentation is being integrated into the main workflow incrementally

---

## Quick Start

### Installation

```bash
# Install from PyPI (recommended)
pip install specter

# Install from source
git clone https://github.com/Unclecheng-li/Specter.git
cd Specter
pip install -e .
```

### Four-Step Launch

```bash
# 1. Select provider (auto-fills Base URL and model name)
specter config provider minimax   # or openai / deepseek / zhipu / moonshot / qwen / siliconflow

# 1.2 (optional) custom Base URL or model name
specter config set llm.base_url https://your-own-api.example.com/v1
specter config set llm.model your-model-name

# 2. Set API Key
specter config set llm.api_key sk-your-key-here

# 3. Default: open the original CLI / REPL
specter

# 4. Optional: open the TUI workbench
specter tui
```

### Environment Check

```bash
specter doctor
```

Sample output:

```
👻 Specter Environment Check

  Python: 3.14.4
  Node.js: v24.14.1
  npx: installed
  nmap: installed

LLM Config:
  Provider: openai
  API Key: set
  Base URL: https://api.openai.com/v1
  Model: gpt-4o

MCP Services:
  fetch: enabled [P0]
  memory: enabled [P0]
  ...

✅ Ready. Run specter to start.
```

---

## CLI Command Reference

Run `specter --help` to see all available commands:

```bash
$ specter --help

👻 Specter — AI-powered penetration testing CLI

 Usage: specter [OPTIONS] COMMAND [ARGS]...

 Options:
   --version  Show version and exit.
   --help     Show this message and exit.

 Commands:
   run           🚀 Full pentest in one shot
   persistent    🔄 Persistent pentesting (100 rounds/cycle)
   recon         🔍 Reconnaissance only (no exploitation)
   scan          🔎 Vulnerability scanning
   exploit       💥 Exploitation phase
   report        📝 Generate report from session JSON
   repl          💬 Start the classic REPL
   config        ⚙️  Manage config (set/get/list/provider)
   init          🔧 Initialize configuration
   doctor        🏥  Check runtime environment
   tui           🖥️  Open the terminal UI workbench
   web           🌐 Launch local Web UI
```

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `specter` | Open the original CLI / REPL by default | `specter` |
| `specter tui` | Explicitly open the terminal UI workbench | `specter tui` / `specter tui --target target.com` |
| `specter repl` | Start the classic REPL interactive shell | `specter repl` |
| `specter run <target>` | Full pentest in one shot | `specter run 192.168.1.1` |
| `specter persistent <target>` | Persistent pentesting | `specter persistent 192.168.1.1` |
| `specter recon <target>` | Reconnaissance only | `specter recon target.com` |
| `specter scan <target>` | Vulnerability scanning | `specter scan target.com --ports 80,443` |
| `specter exploit <target>` | Exploitation phase | `specter exploit target.com --cve CVE-2024-1234` |
| `specter report <session>` | Generate report from session | `specter report session_xxx.json` |
| `specter config set <key> <value>` | Set a config value | `specter config set llm.api_key sk-xxx` |
| `specter config get <key>` | View a config value | `specter config get llm.model` |
| `specter config list` | List all config | `specter config list` |
| `specter config provider <name>` | Switch LLM provider | `specter config provider deepseek` |
| `specter init` | Initialize config files | `specter init` |
| `specter doctor` | Check runtime environment | `specter doctor` |
| `specter web` | Launch local Web UI | `specter web` / `specter web --port 8080` |

### TUI Workbench

`specter tui` is the optional terminal UI workbench entry. It shows the authorized target, check mode, runtime overview, safety boundary, command preview, target history, report entry, and inline environment diagnostics before a task starts.

```bash
specter tui
specter tui --target https://target.example --mode quick --only-port 443
specter tui --dry-run --target https://target.example --mode deep --only-path /admin
```

The default `specter` command still opens the original CLI / REPL. The TUI opens only when users explicitly run `specter tui`.

### Provider Configuration

```bash
# List all providers and switch
specter config provider --list    # list all available providers
specter config provider minimax   # switch to MiniMax

# Manual setup (custom mode)
specter config set llm.base_url https://your-api.com/v1
specter config set llm.model your-model-name
specter config set llm.api_key sk-your-key
```

---

## Usage

### Mode 1: Original CLI / REPL Interactive Mode (Default)

```bash
$ specter
```

No-args startup opens the original 👻 interactive shell for natural-language use:

```text
👻 specter> pentest 192.168.1.100 — this is my authorized lab

[*] Entering autonomous pentest mode. Press Ctrl+C to interrupt at any time.
── Round 1 ──
  [+] Target: 192.168.1.100
  [+] Open ports: 22, 80, 443, 8080
```

### Mode 2: TUI Workbench

```bash
$ specter tui
```

The TUI shows target, mode, runtime overview, and safety boundary before launching a task.

```bash
specter tui
specter tui --target https://target.example --mode quick --only-port 443
specter tui --dry-run --target https://target.example --mode deep --only-path /admin
```

### Mode 3: Classic REPL

```bash
$ specter repl
```

Enter the classic 👻 interactive shell and chat in natural language:

```
👻 specter> pentest 192.168.1.100 — this is my authorized lab

[*] Entering autonomous pentest mode. Press Ctrl+C to interrupt at any time.
── Round 1 ──
  [+] Target: 192.168.1.100
  [+] Open ports: 22, 80, 443, 8080
  [+] Web fingerprint: Apache/2.4.62
── Round 2 ──
  [+] Discovered /manager/html (Tomcat Manager)
  [+] Matched CVE-202X-XXXX: Apache Tomcat Auth Bypass
── Round 3 ──
  [+] Vulnerability verified

👻 192.168.1.100 | report> generate pentest report
[+] Report saved: ./reports/192.168.1.100_20260418.md
[+] PoC saved: ./pocs/CVE-202X-XXXX.py
```

#### Classic REPL Built-in Commands

| Command             | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `target <host>`     | Set pentest target                                      |
| `status`            | View current state (target, phase, tools, thinking)    |
| `tools`             | List available MCP tools                               |
| `think`             | Toggle thinking process display                         |
| `think on` / `off`  | Explicitly control thinking visibility                  |
| `persistent`        | Start persistent pentesting (100 rounds/cycle)         |
| `persistent <host>` | Start persistent pentest on a target                   |
| `clear`             | Clear current session                                  |
| `help`              | Show help                                              |
| `exit` / `quit` / `q` | Exit Specter                                       |

### Mode 4: Persistent Pentest

```bash
specter persistent 192.168.1.100              # default: 100 rounds/cycle × 10 cycles
specter persistent 192.168.1.100 -r 200 -c 5  # 200 rounds/cycle × 5 cycles
specter persistent 192.168.1.100 --no-report   # disable auto-report
```

### Mode 5: Web UI

```bash
# Install Web dependencies
pip install specter[web]

# Launch Web UI (default: 127.0.0.1:7788)
specter web

# Custom port
specter web --port 8080
```

Once launched, open `http://127.0.0.1:7788` in your browser.

> ⚠️ By default the server binds to localhost only. To allow remote access you must explicitly pass `--host 0.0.0.0 --allow-remote` — make sure your network is secure.

---

## LLM Provider Configuration

Specter supports all OpenAI-compatible APIs with 13 built-in provider presets:

```bash
specter config provider --list    # list all providers
specter config provider minimax   # one-command switch
```

| Provider     | Command                  | Default Model          |
| ------------ | ------------------------ | ---------------------- |
| OpenAI      | `provider openai`        | gpt-4o                 |
| MiniMax     | `provider minimax`       | MiniMax-M3             |
| DeepSeek    | `provider deepseek`      | deepseek-v4-pro        |
| Zhipu GLM   | `provider zhipu`         | glm-4.7                |
| Kimi        | `provider moonshot`      | kimi-k2.6              |
| Qwen        | `provider qwen`          | qwen3-max              |
| SiliconFlow | `provider siliconflow`   | DeepSeek-V4-Flash      |
| Doubao      | `provider doubao`        | Doubao-Seed-2.0-Pro    |
| Baichuan    | `provider baichuan`      | Baichuan4-Turbo        |
| StepFun     | `provider stepfun`       | step-3.5-flash         |
| SenseTime   | `provider sensetime`     | SenseNova-6.7-Flash-Lite |
| Yi          | `provider yi`            | yi-lightning           |
| Custom      | `provider custom`        | manual                 |

---

## Architecture

### Core Modules

| Module              | File                                                  | Description                                        |
| ------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| **CLI/TUI Entry**   | `cli/main.py` + `cli/tui.py`                         | Typer commands + default original CLI/REPL + explicit TUI |
| **Agent Core**      | `agent/core.py`                                      | AgentCore coordination entrypoint |
| **Dynamic Prompts** | `agent/prompts.py`                                   | Base identity + core contract + skills + MCP tools  |
| **Prompt Assembly** | `agent/system_prompt.py` + `prompt_context.py`       | System prompt / round context / attack summary assembly |
| **Input Analysis**  | `agent/input_analysis.py`                            | Target detection, phase detection, explicit vuln-hint extraction |
| **Anti-loop / CTF** | `agent/anti_loop.py` + `ctf_mode.py`                | Completion signals, attack-path heuristics, failed-target tracking, flag state machine |
| **Session State**   | `agent/context.py`                                   | Phase tracking + findings + step records            |
| **Skill / KB Context** | `agent/skill_context.py` + `kb_context.py`       | Skill selection and knowledge-base prompt injection |
| **Target State**    | `target_state/store.py`                              | Per-target persistence, resume, snapshots, rollback, target-level reports |
| **MCP Orchestration**| `mcp/registry.py` + `lifecycle.py` + `router.py`    | Service registry + lifecycle + NL→tool routing     |
| **Skill Dispatcher** | `skills/loader.py` + `dispatcher.py`               | Directory-format Skills + CTF/SRC/AI/Web intent routing |
| **Crypto Tools**    | `skills/crypto_tools.py`                             | 29 encode/decode/crypto ops, registered as built-in tools |
| **Config**          | `config/schema.py` + `settings.py`                   | Pydantic models + YAML persistence + 13 provider presets |
| **Report Generator** | `report/generator.py` + `poc_builder.py`          | Markdown reports + Python PoC templates             |
| **Security KB**     | `kb/store.py` + `retriever.py`                     | JSON storage + CVE/technique/tool retrieval        |

---

## MCP Toolchain

| MCP Service         | Tools | Use Case                    | Priority |
| ------------------- | ----- | ---------------------------- | ------- |
| fetch              | 1     | HTTP requests, API testing    | P0      |
| memory             | 2     | Context memory, state persist | P0      |
| chrome-devtools    | 4     | Browser automation            | P0      |
| js-reverse         | 2     | JavaScript reversing          | P0      |
| burp               | 2     | HTTP interception & replay    | P0      |
| frida-mcp          | 2     | Mobile Hook                   | P1      |
| adb-mcp            | 3     | Android device control        | P1      |
| jadx               | 2     | APK decompilation             | P1      |
| ida-pro-mcp        | 2     | Binary reversing              | P1      |
| sequential-thinking| 1     | Complex reasoning chains       | P1      |
| context7           | 1     | Code context retrieval        | P1      |
| everything-search   | 1     | Local file search             | P2      |

> 11 MCP services, 23 tool definitions total. Plus 3 built-in Agent tools (`load_skill_reference` + `crypto_decode` + `python_execute`) callable without MCP.

---

## Built-in Skills

### Core Skills (7)

| Skill              | Description                         |
| ------------------ | ----------------------------------- |
| pentest-flow       | Full pentest workflow orchestration  |
| recon              | Information gathering               |
| vuln-discovery     | Vulnerability discovery              |
| exploitation       | Exploitation                       |
| post-exploitation  | Post-exploitation                  |
| reporting          | Report generation                  |
| waf-bypass        | WAF bypass techniques              |

### Specialized Skills (14)

| Skill                      | Ref Docs | Description                                          |
| -------------------------- | -------- | ---------------------------------------------------- |
| web-pentest                | 4        | Web application pentesting                            |
| android-pentest            | 9        | Android application pentesting                        |
| client-reverse            | 20       | Client-side reverse engineering                      |
| web-security-advanced      | 34       | Advanced web security (injection, bypass, chains)     |
| ai-mcp-security            | 7        | AI/MCP security testing                              |
| intranet-pentest-advanced  | 15       | Advanced internal network pentesting                  |
| pentest-tools              | 18       | Pentest tool quick reference                         |
| rapid-checklist            | 3        | Rapid validation checklists                          |
| crypto-toolkit             | 3        | Encode/decode/crypto (29 ops, registered as built-in)|
| ctf-web                   | 9        | CTF Web attacks (PHP bypass/RCE/SSTI/deserialization)|
| ctf-crypto                | 6        | CTF cryptography (RSA/AES/ECC/PRNG/lattice attacks)  |
| ctf-misc                  | 6        | CTF Misc (PyJail/BashJail/encoding chains/VM RE)    |
| osint-recon               | 7        | OSINT four-dimension model (server/web/domain/person)|
| secknowledge-skill        | 39       | Web+AI security testing knowledge base               |

---

## Configuration

```bash
specter config list                          # view all settings
specter config get llm.model                 # view single setting
specter config set llm.api_key sk-xx         # set API key
specter config set session.max_rounds 30     # set max autonomous rounds (default 15)
specter config set session.show_thinking false  # hide thinking process
```

Config file location: `~/.specter/config.yaml`.

---

## Security Notice

Specter is intended **solely for authorized security testing**. Before using this tool, ensure:

1. You have **explicit authorization** for the target system
2. Scope has been **confirmed in writing** with the target owner
3. You comply with all applicable **local laws and regulations**

Unauthorized penetration testing is illegal. The author assumes no liability for misuse.

---

## License

[MIT License](LICENSE)

Original project: [VulnClaw](https://github.com/Unclecheng-li/VulnClaw) by Unclecheng-li (MIT License). Specter is a fork with English translation, rebranding, and security improvements.

---

<div align="center">

> 👻 **Specter** — Every pentest should follow a process.

</div>
