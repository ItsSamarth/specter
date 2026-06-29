# Contributing to Specter

Thank you for contributing to Specter.

This document's goal is not to prescribe a bureaucratic process, but to help you quickly understand the current code structure so you make changes at the right layer — reducing the "it works, but the architecture gets messier" problem.

---

## Project Structure

```text
Specter/
|-- specter/
|   |-- __init__.py              # package version and basic metadata
|   |-- orchestrator.py          # CLI / Web shared task orchestration entry
|   |-- repl_runner.py           # REPL shared execution helper
|   |-- agent/                   # Agent core logic
|   |   |-- core.py              # AgentCore shell and coordination entry
|   |   |-- llm_client.py        # LLM calls, retries, tool summary passback
|   |   |-- tool_call_manager.py # tool-call dedup, execution, result wrapping
|   |   |-- builtin_tools.py     # python_execute / nmap_scan / MCP bridging
|   |   |-- context.py           # session state, findings, steps, lifecycle state
|   |   |-- runtime_state.py     # runtime loop state
|   |   |-- loop_controller.py   # auto / persistent main loop
|   |   |-- finding_parser.py    # finding extraction, evidence level and lifecycle classification
|   |   |-- prompt_context.py    # round context and attack summary
|   |   |-- prompts.py           # prompt construction helpers
|   |   |-- system_prompt.py     # dynamic system prompt assembly
|   |   |-- input_analysis.py    # target, phase, vuln-hint extraction
|   |   |-- anti_loop.py         # anti-deadloop, failed targets, attack path tracking
|   |   |-- recon_tracker.py     # recon dimension completion tracking
|   |   |-- ctf_mode.py          # CTF flag detection and verification
|   |   |-- skill_context.py     # Skill context selection
|   |   |-- kb_context.py        # knowledge base context injection
|   |   `-- think_filter.py      # think tag display and hiding
|   |-- cli/
|   |   |-- main.py              # CLI commands, doctor, web launch, target-state CLI
|   |   |-- tui.py               # TUI data classes, dashboard rendering, color constants
|   |   `-- tui_textual.py       # Textual-driven TUI workbench
|   |-- config/                  # config schema, loading, saving, env var overrides
|   |-- kb/                      # knowledge base storage, retrieval, updates
|   |-- mcp/
|   |   |-- lifecycle.py         # attach / probe / call / degrade behavior
|   |   |-- registry.py          # service state, health, attach state, tool registration
|   |   `-- router.py            # natural language intent to MCP tool suggestion
|   |-- report/                  # report generation, filtering, PoC generation
|   |-- skills/                  # built-in markdown skills, loader, dispatcher
|   |   |-- core/                  # 7 core flat-format Skills (single .md files)
|   |   |-- specialized/           # directory-format specialized Skills, each subdirectory contains SKILL.md
|   |   |   |-- <skill-name>/
|   |   |   |   |-- SKILL.md      # frontmatter + trigger conditions + behavior guidelines
|   |   |   |   `-- references/  # documents loadable on demand via load_skill_reference
|   |   |   `-- secknowledge-skill/ # CTF/SRC/Web+AI security testing knowledge base integration
|   |   |-- crypto_tools.py        # crypto_decode built-in tool implementation
|   |   |-- dispatcher.py          # natural language intent to Skill routing
|   |   `-- loader.py             # flat/directory Skill loading and reference reading
|   |-- target_state/            # target history, preview, diff, rollback, resume plan
|   |-- web/
|   |   |-- app.py               # FastAPI routes and static frontend serving
|   |   |-- schemas.py           # Web API request/response models
|   |   |-- task_manager.py      # Web task state and history persistence
|   |   |-- stream.py            # SSE event encoding
|   |   |-- services/            # config / report / target / task / MCP service layer
|   |   `-- static/              # fallback static page when frontend dist doesn't exist
|   `-- warstories/              # built-in case study markdown content
|-- frontend/
|   |-- src/
|   |   |-- pages/               # Dashboard / Tasks / Target / Snapshots / Reports / Settings
|   |   |-- api/                 # frontend API request wrappers
|   |   |-- hooks/               # React Query hooks
|   |   `-- types/               # shared frontend types
|   `-- package.json             # frontend build and development scripts
|-- scripts/                     # release preflight / dist verification scripts
|-- tests/                       # backend, CLI, MCP, release, web, report tests
|-- .github/workflows/           # CI / preflight / release workflows
|-- README.md                    # project documentation
|-- pyproject.toml               # packaging metadata and Hatch build rules
`-- CONTRIBUTING.md              # this file
```

---

## How to Find the Right Code

### 1. Modifying Agent behavior → `specter/agent/`

Applies to:
- Autonomous / persistent pentest loop behavior
- Tool call orchestration
- LLM request and response handling
- recon / CTF / anti-loop logic
- finding lifecycle, evidence level, result parsing

In the current architecture, `core.py` acts more as a coordination shell. Unless it's truly entry-level logic, prefer modifying the corresponding helper/module rather than piling more logic back into `core.py`.

### 2. Modifying shared task flow → `specter/orchestrator.py` and `specter/repl_runner.py`

Applies to:
- CLI / Web / REPL shared task lifecycle
- restore → run → save → summarize flow
- REPL single-execution helper

If the same behavior appears in both CLI and Web, it should typically be consolidated here rather than written separately in `cli/main.py` and `web/services/task_service.py`.

### 3. Modifying CLI or REPL behavior → `specter/cli/main.py`

Applies to:
- Typer commands
- REPL experience
- `doctor` output
- `web` launcher behavior
- `target-state` subcommands

This layer handles entry, parameter binding, and user output — it's not the right place for core pentest logic.

### 3.1 Modifying the TUI workbench → `specter/cli/tui.py` and `specter/cli/tui_textual.py`

Applies to:
- TUI dashboard layout and rendering
- Slash command system (`/target`, `/mode`, `/start`, etc.)
- Command Palette interaction
- Prompt/confirm state machine
- TUI color theme

**Architecture:**

```
main.py (Typer CLI)
  └─ tui.py (run_tui → delegates)
       └─ tui_textual.py (run_tui_textual → Textual App)
            ├─ DashboardScreen
            │   ├─ CommandPalette     (level 1: slash completion dropdown)
            │   ├─ SecondaryPopup     (level 2: parameter input popup)
            │   └─ RichLog + spinner  (execution mode: output area + trailing animation)
            └─ SpecterApp
```

| File | Responsibility |
|------|----------------|
| `tui.py` | Data classes (`TuiState`, `TuiMode`, `TuiTaskDraft`), Rich dashboard rendering (`build_dashboard`), color constants (`C_PRIMARY` etc.), slash command registry (`SLASH_COMMANDS`), entry `run_tui()` |
| `tui_textual.py` | Textual App implementation: `DashboardScreen` (layout + execution mode), `CommandPalette` (level-1 dropdown panel), `SecondaryPopup` (level-2 popup), `SpecterApp` (CSS), slash command handlers, prompt state machine, subprocess execution engine |

**Slash command system:**

Commands are registered via the function decorator `@_register_handler("...")`, and `_dispatch()` routes based on input. Command signature: `fn(session: dict, args: str) -> str | None`.
`SLASH_COMMANDS` dict (`tui.py`) determines which commands are visible in the command palette.

- Returns `"quit"` → exit TUI
- Returns `"launch"` → start pentest task (subprocess execution within TUI, not returning to CLI)
- Returns `None` → set prompt state (triggers level-2 popup)

Inline arguments supported: `/target example.com`, `/mode deep`, `/scope host=1.2.3.4`; without args, a level-2 popup opens for interactive input.

**Prompt state machine:**

`session["_prompt"]` tuple type (also set `_show_popup = True` to trigger level-2 popup):
- `("input", label, callback, default)` — popup shows description + input box, Enter confirms
- `("choice", label, choices, callback)` — popup shows description + option list, arrow keys + Enter
- `("confirm", label, callback)` — popup shows description + y/n, keypress confirms directly (y = True, n/esc = False)
- `("message", text)` — popup shows plain text, Enter/Escape closes (callback is None)
- `("chain", fields, idx, callback)` — popup shows chained multi-field input (e.g. scope step-by-step), each Enter moves to the next field, callback triggers on completion (can cascade popups)

**Command Palette:**

Inherits `ListView`, pops up above the input box when `/` is typed. `↑↓` moves the highlight pointer (doesn't fill the input box), `Tab`/`Enter` selects and completes. `show_commands()` uses `query_children(ListItem).remove()` to clear old entries + `mount()` to mount new ones (standard Textual API, replaces old private `_nodes` operations). CSS contains `.-highlight` style (`#fab283 30%` background + white text). Arrow key navigation intercepts `up`/`down` in `DashboardScreen.on_key` then calls `action_cursor_up/down`.

**Secondary Popup:**

Inherits `Vertical`, pops up automatically when a slash command is missing parameters. Five sub-modes:
| Mode | Example | Component |
|------|---------|-----------|
| `input` | `/target` | `Static` description + `Input` box |
| `choice` | `/mode` | `Static` description + `ListView` option list (arrow keys + Enter) |
| `confirm` | `/start` (deep validation) | `Static` description + y/n prompt (keypress confirms directly) |
| `message` | `/diag` | `Static` description (Enter/Escape closes) |
| `chain` | `/scope` | Field-by-field input `[1/7] → [2/7] → ...`, cascades to next popup on completion |

`_resolve(value)` confirms and calls callback to modify state; `_cancel()` closes popup without modifying state. Escape key calls `_cancel()` when popup is open (original value unchanged). `_on_done` callback ensures the dashboard auto-refreshes after the popup closes.

**Escape key behavior:**

Closes layer by layer: secondary popup `_cancel()` → command palette `hide_palette()` → prompt `_cancel_prompt()`. In idle state, no longer exits TUI (only `/quit` or `Ctrl+C` exits).

**Execution mode:**

When `/run` or `/start` returns `"launch"`, TUI doesn't exit; instead it runs a subprocess within TUI:
1. Hide dashboard (`#dashboard.-hidden`), show `RichLog` output area (`#output-log.-active`)
2. Left of input box shows **trailing animation**: 5 squares with no gaps, leading `[bold #fab283]■` with two-level trail (`[#fab283]■` + `[#808080]■`), updates 0.12s per frame, bounces left and right
3. Disable input box, launch subprocess via `subprocess.Popen` (`python -m specter.cli.main <cmd> <args>`), `encoding="utf-8"` to avoid GBK decode errors, real-time streaming of `stdout` pipe
4. Background thread reads subprocess output into `Queue`, main thread polls via `set_timer(0.3s)` and writes to `RichLog`
5. Execution complete: hide trailing animation, enable input box, reload config
6. `Ctrl+Shift+C` copies output log to system clipboard (Windows: `clip`, macOS: `pbcopy`, Linux: `xclip`)

**Color scheme (opencode style):**

| Variable | Value | Usage |
|----------|-------|-------|
| `C_PRIMARY` | `#fab283` | menu keys, highlight selection |
| `C_SECONDARY` | `#5c9cf5` | mode labels, info identifiers |
| `C_ACCENT` | `#9d7cd8` | titles, headers |
| `C_SUCCESS` | `#7fd88f` | configured/success state |
| `C_WARNING` | `#f5a742` | not set / needs attention |
| `C_ERROR` | `#e06c75` | error / invalid input |
| `C_MUTED` | `#808080` | secondary text, descriptions |
| `C_BORDER` | `#484848` | panel borders |

Textual CSS UI elements (Header, status bar, input box) use terminal-adaptive backgrounds (`$background`, `$surface`, `$boost`); accent colors are hard-coded to the values above.

### 4. Modifying configuration → `specter/config/`

- `schema.py`: configuration model definitions
- `settings.py`: loading, saving, env var overrides, directory paths

Don't scatter config parsing all over business logic.

### 5. Modifying report logic → `specter/report/`

Applies to:
- Markdown / HTML report rendering
- Report content filtering
- PoC generation
- Verification summaries and location info

The main entry point is `generator.py`, but note it now affects both target-state reports and persistent-cycle reports.

### 6. Modifying MCP behavior → `specter/mcp/`

- `registry.py`: service state, health, attach state, tool registration
- `lifecycle.py`: attach / probe / call / degrade logic
- `router.py`: natural language intent to MCP tool suggestion

Current status:
- `fetch` / `memory`: locally executable
- `chrome-devtools` / `burp`: have real stdio attach, dynamic tool discovery, persistent session skeleton
- Other services: mostly still degrade to structured placeholders

When modifying MCP, also consider:
- diagnostics display
- `error_type` classification
- degradation behavior after attach failure

### 7. Modifying resume/findings inheritance → `specter/target_state/`

Applies to:
- target-state persistence
- merge rules
- preview / diff / rollback
- resume strategy and summary generation

This module handles "sharing findings across commands for the same target." Don't push this logic back into `core.py` or duplicate it in the page layer.

### 8. Modifying the Web backend → `specter/web/`

- `app.py`: FastAPI routes and frontend static file serving
- `schemas.py`: request/response models
- `task_manager.py`: Web task state and history
- `services/`: config / report / target / task / MCP service layer

As a principle, put logic in `web/services/` to keep route functions from becoming catch-alls.

### 9. Modifying the Web UI → `frontend/`

Applies to:
- Dashboard / Task Console / Target State / Snapshots / Reports / Settings pages
- React Query hooks
- Frontend API bindings
- Console interaction and style improvements

Keep frontend/backend contracts in sync with `specter/web/schemas.py`.

### 10. Modifying packaging / release → `scripts/`, `.github/workflows/`, `pyproject.toml`

Applies to:
- Local preflight
- dist artifact verification
- CI / release workflows
- build include / exclude
- package metadata

Version source of truth is `pyproject.toml`; `specter/__init__.py` is the fallback.

### 11. Modifying or adding Skills → `specter/skills/`

Applies to:
- Adding core pentest workflow descriptions
- Adding specialized knowledge bases or reference documents
- Adjusting natural-language-to-Skill automatic routing rules
- Updating reference documents readable via `load_skill_reference`

There are two Skill formats:

| Format | Location | Purpose |
|--------|----------|---------|
| flat-format | `specter/skills/core/*.md` | Core workflow Skills, e.g. `pentest-flow`, `recon`, `reporting` |
| directory-format | `specter/skills/specialized/<skill-name>/` | Specialized Skills, must contain `SKILL.md`, optionally `references/` |

Directory-format conventions:
- `SKILL.md` uses YAML frontmatter with at least `name` and `description`
- `references/` contains `.md`, `.yaml`, `.yml` files; filenames are exposed to the Agent
- Reference content should be split by topic — avoid cramming large knowledge bases into `SKILL.md`
- To trigger the Skill, add strong-signal keywords to `SKILL_INTENT_MAP` in `dispatcher.py`
- After adding or modifying a Skill, update `tests/test_skills.py` and the Skill table in README

`secknowledge-skill` is the current external knowledge base integration example:
- Location: `specter/skills/specialized/secknowledge-skill/`
- Source: `Pa55w0rd/secknowledge-skill`
- Content: 38 upstream `references/` documents + Specter's `specter-ctf-src-routing.md`
- Triggers: `SRC`, vulnerability research, bug bounty, `GAARM`, `OWASP LLM/ASI/WSTG`, `Web+AI` and other CTF/SRC security testing signals

When syncing an external Skill, preserve the source, license, and integration notes, and use a file list comparison to confirm no reference documents are missing.

---

## Contribution Tips

- Make changes in the correct module — don't pile responsibilities that were already extracted back into `core.py`
- If modifying shared task flow, consider `orchestrator.py` / `repl_runner.py` first
- When changing behavior logic, add tests alongside
- When changing packaging/release logic, also check `pyproject.toml`, `scripts/`, `.github/workflows/`
- When updating documentation, ensure capability descriptions match the current actual implementation — especially MCP, sandbox, and security boundary details, which are easy to misrepresent

---

## Pre-PR Checklist

At minimum check:
1. Relevant tests pass
2. Documentation and implementation are consistent
3. New logic is in the correct module, not shoved back into a large file
4. If version, CLI output, README, or packaging flow is affected, those files are updated

---

## Web UI Notes

If you're modifying the Web UI, start with:
- `specter/web/`
- `frontend/`

The Web side is no longer just a placeholder skeleton; it now includes:
- Backend API
- Task state persistence
- target preview / diff
- MCP diagnostics
- Settings security mode configuration

Principles:
- Web layer reuses existing agent / target_state / report trunk
- Don't duplicate a new restore logic in the Web layer
- Don't let the frontend hold sensitive keys directly

---

## Suggested Preflight

Before submitting, run at least once:

```bash
python scripts/release_preflight.py
python scripts/release_preflight.py --build
```

It checks:
- Version consistency between `pyproject.toml` and `specter.__version__`
- Backend `pytest -q`
- Frontend `npx tsc -b`
- Optional build and dist artifact verification
