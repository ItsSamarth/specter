---
name: client-reverse
description: Client-side reverse engineering and Burp replay — recovering complex client signatures, restoring encryption, tracing request chains, and achieving stable replay; applies to authorized Android app pentesting, browser JS signing, and desktop client reverse engineering
---

# Client-Side Reverse Engineering and Burp Replay Skill

Use this Skill when requests are constructed by a client (Android app, browser JS, desktop client) and signing, encryption, token state, device binding, or anti-automation logic prevents Burp from replaying them directly.

## Core Principle

**Packet-First**: First capture and analyze the real HTTP/HTTPS request or WebSocket traffic, confirm its usability, and then reverse engineer blocking points as needed. Reverse engineering is a step for resolving blockers, not the default entry point.

## Scenario Routing

### Authorized Android App Pentesting

**Do not start by analyzing the APK with jadx or ida_pro_mcp.** Follow this order:

1. Confirm the target app is installed on the connected device
2. Have Burp or Charles ready to capture traffic
3. Use scrcpy_vision to open the app and drive the real business flow
4. After each key action, check whether HTTP/HTTPS or WebSocket packets appear in Burp/Charles
5. If packets are visible and replayable → immediately move to `web-security-advanced` for Web/API security testing
6. Repeat the "UI action → capture → Web security analysis" loop
7. Only when packets cannot be captured / are encrypted / cannot be replayed → escalate to jadx → frida_mcp → ida_pro_mcp

**MCP toolchain**: scrcpy_vision → burp/charles → adb_mcp → jadx → frida_mcp → ida_pro_mcp

### Browser JS Signing, Anti-Scraping, WebSocket Handshake

1. Use chrome_devtools to inspect page state and request chains
2. Use js_reverse to locate token/sign generation logic
3. Use burp to validate replay and determine mutable fields

**Phase model**: locate → recover → runtime → validation → replay

**MCP toolchain**: chrome_devtools → js_reverse → burp

### Desktop Client / Local Signer

1. Use everything_search to locate relevant files
2. Use ida_pro_mcp for static analysis of the signing function
3. Use frida_mcp to obtain runtime parameters
4. Use burp to validate stable replay

**MCP toolchain**: everything_search → ida_pro_mcp → frida_mcp → burp

## Replay-Readiness Checklist

Before moving to payload testing, you must be able to answer:

- How is the request body constructed?
- Where do the signing/encryption inputs come from?
- Which cookies, headers, tokens, device values, timestamps, and nonces are required?
- Does the request depend on ordering or session state?
- Which fields can be changed without breaking replay?

## Evidence Preservation

- Location of the builder/signer/crypto code
- Key hook points and observed runtime values
- A usable replay request sample
- Documentation of preconditions, failure modes, and anti-automation behavior

## Reference Documents

- `references/02-client-api-reverse-and-burp.md` — End-to-end workflow from client reverse engineering to Burp replay
- `references/android-authorized-app-pentest-sop.md` — Android app pentest SOP
- `references/browser-js-signing-workflow.md` — Browser JS signing workflow
- `references/android-signing-and-crypto-workflow.md` — Android signing and crypto workflow
- `references/android-ui-driven-observation-and-packet-loop.md` — Android UI-driven observation loop
- `references/android-external-url-runtime-first-workflow.md` — Android external URL testing
- `references/android-network-layer-testing-quick-reference.md` — Android network-layer testing quick reference
- `references/MCP.md` — MCP capabilities master document
- `references/tool-selection-map.md` — Tool selection map
