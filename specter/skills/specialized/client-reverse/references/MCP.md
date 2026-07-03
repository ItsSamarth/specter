# MCP Capabilities Reference

## 1. Purpose

This document catalogues the MCP capabilities that can be directly invoked in the current session. The goal is not merely a “tool list” but a reference draft suitable for authoring `skills` afterward.  
Key areas covered:

- The role of each MCP server / namespace
- How to call each method
- The meaning of main parameters
- What the return values typically contain
- Typical use cases
- Common workflows when combining multiple MCPs

This document is written for Codex / Agent-style tool orchestration, not as a general-purpose SDK reference. The emphasis is therefore on “when to use it” and “how to describe the calling strategy when writing a skill.”

---

## 2. General Calling Conventions

### 2.1 Tool Naming Format

Most MCP tool names in the current environment follow this pattern:

```text
mcp__<server_name>__<tool_name>
```

Examples:

- `mcp__adb_mcp__list_devices`
- `mcp__chrome_devtools__navigate_page`
- `mcp__ida_pro_mcp__decompile`

A small number of functions related to MCP resource access do not have the `mcp__` prefix, but they are still part of the MCP ecosystem:

- `list_mcp_resources`
- `list_mcp_resource_templates`
- `read_mcp_resource`

### 2.2 Call Parameter Format

All MCP tools use JSON-style parameter objects. Typical format:

```json
{
  "device_id": "emulator-5554",
  "lines": 200
}
```

Notes:

- Only pass the required fields; do not pad with meaningless empty arrays or `null`
- `optional` parameters can generally be omitted
- Some tools require absolute paths, especially for screenshots, saving source code, pulling files, and screen-recording output paths
- Some tools use pagination parameters such as `offset`, `count`, `pageIdx`, `pageSize`

### 2.3 Key Points to Describe When Writing a Skill

If you are turning these capabilities into a skill, it is recommended that each skill explicitly state:

1. Trigger condition  
2. Preferred MCP  
3. Order of tool invocations  
4. Which parameters must be filled in  
5. When to switch to another MCP  
6. What to do if output is empty or the call fails

### 2.4 MCP Selection Quick Reference

| Task Type | Preferred MCP |
| --- | --- |
| Android device management, installing APKs, tapping/swiping, pulling files | `adb_mcp` |
| Android visual control, UI tree location, wireless ADB, live screen | `scrcpy_vision` |
| Android HTTP/HTTPS traffic capture, Charles session analysis | `charles` |
| Burp history, Repeater, Collaborator, Intruder | `burp` |
| Web automation, screenshots, forms, network requests, console | `chrome_devtools` |
| JS breakpoints, source search, XHR initiator chain, function tracing | `js_reverse` |
| Official documentation lookup, code example queries | `context7` |
| General web scraping / fetching web content | `fetch` |
| Fast local file search | `everything_search` |
| Android dynamic injection, Frida attach/spawn | `frida_mcp` |
| Binary static analysis, IDA batch renaming / decompilation / type repair | `ida_pro_mcp` |
| APK decompilation, Manifest, class/method/xref queries | `jadx` |
| Knowledge graph memory, long-term structured memory | `memory` |
| Step-by-step reasoning for complex problems | `sequential_thinking` |

### 2.5 Common Combined Workflows

#### Android App Analysis

- Static: `jadx`
- Dynamic: `frida_mcp`
- Traffic capture: `charles`
- Device control: `adb_mcp`
- Visual / UI automation: `scrcpy_vision`

#### Web Front-End Reverse Engineering

- Page interaction: `chrome_devtools`
- JS breakpoints and source search: `js_reverse`
- HTTP replay and security testing: `burp`

#### Native / APK So Reverse Engineering

- IDA static analysis: `ida_pro_mcp`
- Runtime hooking: `frida_mcp`
- Device-side assistance: `adb_mcp` / `scrcpy_vision`

---

## 3. MCP Resource Generic Interfaces

These three functions are not specific business servers; they are generic capabilities for “accessing resources exposed by MCP servers.”

### 3.1 `list_mcp_resources`

- Purpose: List resources published by a specific MCP server or all servers
- Typical use: Find directly readable files, contexts, database schemas, or configuration fragments
- Parameters:
  - `server`: optional, specifies the server name
  - `cursor`: optional, pagination cursor
- Skill description advice: enumerate resources first, then decide whether to call `read_mcp_resource`

Example:

```json
{
  "server": "some_server"
}
```

### 3.2 `list_mcp_resource_templates`

- Purpose: List parameterized resource templates
- Typical use: Discover resources that are “read with parameters,” e.g., queried by table name, primary key, or path
- Parameters:
  - `server`
  - `cursor`
- Skill description advice: use this first when the resource URI is not fixed but a “template URI”

### 3.3 `read_mcp_resource`

- Purpose: Read the contents of a specific resource
- Parameters:
  - `server`: server name
  - `uri`: resource URI
- Suitable scenarios:
  - Reading configuration
  - Reading schemas
  - Reading service context
  - Reading shared state

Example:

```json
{
  “server”: “some_server”,
  “uri”: “resource://example/path”
}
```

---

## 4. `adb_mcp`: Android Device Control and File Interaction

### 4.1 Role

`adb_mcp` is the most fundamental Android device interaction layer. It is suited for:

- Listing devices and confirming status
- Installing / uninstalling APKs
- Taking screenshots and recording the screen
- Entering text, tapping, swiping, sending key events
- Pulling / pushing files
- Reading logcat, battery, memory, and storage information

If your skill needs to “control the device itself,” prioritize this.

### 4.2 Common Workflow

1. `list_devices` to confirm the device  
2. `get_device_info` / `get_battery_info` to assess the environment  
3. `install_app` or `list_packages`  
4. `send_tap` / `send_swipe` / `send_text` to drive interaction  
5. `take_screenshot` / `record_screen` for evidence  
6. `get_logcat` for troubleshooting  

### 4.3 Method List

| Tool | Main Parameters | Purpose | Typical Use |
| --- | --- | --- | --- |
| `mcp__adb_mcp__list_devices` | none | List connected Android devices | Task entry point — confirm device is online |
| `mcp__adb_mcp__get_device_info` | `device_id?` | Read detailed device information | Check model, OS version, serial number |
| `mcp__adb_mcp__get_battery_info` | `device_id?` | Read battery status | Verify charge before long tests |
| `mcp__adb_mcp__get_memory_info` | `device_id?` | Read memory information | Performance / stability troubleshooting |
| `mcp__adb_mcp__get_storage_info` | `device_id?` | Read storage information | Check space for installation / recording |
| `mcp__adb_mcp__clear_logcat` | `device_id?` | Clear logcat | Get a clean log capture |
| `mcp__adb_mcp__get_logcat` | `device_id?`, `filter_tag?`, `lines?` | Read logs | Crash, network, SSL, debug troubleshooting |
| `mcp__adb_mcp__install_app` | `apk_path`, `device_id?` | Install APK | Deploy a test build |
| `mcp__adb_mcp__uninstall_app` | `package_name`, `device_id?` | Uninstall app | Clean up environment |
| `mcp__adb_mcp__list_packages` | `device_id?`, `system_apps?` | List installed package names | Find target package name |
| `mcp__adb_mcp__list_files` | `remote_path`, `device_id?` | Browse device directory | Find cache, config, exported files |
| `mcp__adb_mcp__pull_file` | `remote_path`, `local_path`, `device_id?` | Pull file from device to local | Export database, logs, cache |
| `mcp__adb_mcp__push_file` | `local_path`, `remote_path`, `device_id?` | Push file to device | Push certificates, scripts, patches |
| `mcp__adb_mcp__send_keyevent` | `keycode`, `device_id?` | Send key event | Back, Home, Menu keys |
| `mcp__adb_mcp__send_tap` | `x`, `y`, `device_id?` | Tap coordinates | Automation operations |
| `mcp__adb_mcp__send_swipe` | `x1`,`y1`,`x2`,`y2`,`duration?`,`device_id?` | Swipe | Scroll list, unlock, change page |
| `mcp__adb_mcp__send_text` | `text`, `device_id?` | Enter text | Search, login, form input |
| `mcp__adb_mcp__take_screenshot` | `save_path`, `device_id?` | Screenshot to local | Evidence preservation, UI state confirmation |
| `mcp__adb_mcp__record_screen` | `duration?`, `save_path?`, `device_id?` | Record screen | Record workflow for evidence |

### 4.4 Typical Call Examples

List devices:

```json
{}
```

Screenshot:

```json
{
  "device_id": "emulator-5554",
  "save_path": "C:\\Users\\28484\\Desktop\\screen.png"
}
```

Read the last 200 log lines:

```json
{
  "device_id": "emulator-5554",
  "lines": 200
}
```

### 4.5 Notes for Writing Skills

- Almost every Android task should start with a `list_devices` call
- `take_screenshot` explicitly requires a local absolute path
- For `get_logcat` in complex scenarios, it is advisable to `clear_logcat` first
- `send_tap` / `send_swipe` rely entirely on coordinates — suitable for fixed layouts, not strongly dynamic ones
- `push_file` and `pull_file` are frequently used for certificate installation, log export, and data evidence

---

## 5. `charles`: Charles Traffic Capture and Session Analysis

### 5.1 Role

`charles` reads and analyzes traffic already captured by Charles Proxy. The focus is not on “directly controlling the Android proxy” but on:

- Checking whether Charles is online and whether an active capture session exists
- Starting or taking over a live capture and obtaining a `capture_id`
- Structured filtering of live traffic or saved recordings
- Drilling into individual requests to view headers, status codes, and request/response body previews
- Grouping traffic by host, path, status, or resource class for analysis
- Stopping a capture and persisting a snapshot for later review

### 5.2 Suitable Skill Types

- Android API reverse engineering
- HTTPS traffic capture
- App interface behavior analysis
- Before/after comparison of parameter signing
- Finding tokens, sessions, and encrypted fields
- Session recording, filtering, and evidence retention

### 5.3 Method List

| Tool | Main Parameters | Purpose | Typical Use |
| --- | --- | --- | --- |
| `mcp__charles__charles_status` | none | Check Charles connectivity and live capture status | Confirm environment is ready |
| `mcp__charles__reset_environment` | none | Reset Charles environment and restore saved configuration | Clean-slate experiment |
| `mcp__charles__start_live_capture` | `adopt_existing?`,`include_existing?`,`reset_session?` | Start or take over a live capture | Obtain the `capture_id` needed for subsequent analysis |
| `mcp__charles__query_live_capture_entries` | `capture_id`,`cursor?`,`preset?`,`host_contains?`,`path_contains?`,`method_in?`,`status_in?`,`request_body_contains?`,`response_body_contains?`,`max_items?` | Structured filtering of live traffic | Recommended real-time retrieval entry point |
| `mcp__charles__peek_live_capture` | `capture_id`,`cursor?`,`limit?` | Preview new entries in the current live capture | Lightweight view of recent requests |
| `mcp__charles__read_live_capture` | `capture_id`,`cursor?`,`limit?` | Incrementally read and advance the live cursor | Use when streaming new traffic |
| `mcp__charles__get_traffic_entry_detail` | `source`,`entry_id`,`capture_id?`,`recording_path?`,`include_full_body?`,`max_body_chars?` | Drill into a single traffic entry | View headers, body preview, request/response details |
| `mcp__charles__group_capture_analysis` | `source`,`capture_id?`,`recording_path?`,`group_by`,`preset?`,`host_contains?`,`path_contains?`,`status_in?` | Group by host/path/status/resource class | Quickly find hot endpoints |
| `mcp__charles__get_capture_analysis_stats` | `source`,`capture_id?`,`recording_path?`,`preset?` | Return coarse-grained statistics | View overall capture distribution |
| `mcp__charles__stop_live_capture` | `capture_id`,`persist?` | Stop live capture and optionally persist | End experiment and save snapshot |
| `mcp__charles__list_recordings` | none | List saved recording files | Select a historical traffic file |
| `mcp__charles__list_sessions` | none | List historical sessions (compatibility method) | Compatibility with older naming |
| `mcp__charles__get_recording_snapshot` | `path?` | Read snapshot metadata from a saved recording | Offline inspection of a recording |
| `mcp__charles__analyze_recorded_traffic` | `recording_path?`,`preset?`,`host_contains?`,`path_contains?`,`method_in?`,`status_in?`,`request_body_contains?`,`response_body_contains?`,`max_items?` | Analyze historical recordings | Offline review and retrospective |
| `mcp__charles__query_recorded_traffic` | `host_contains?`,`http_method?`,`keyword_regex?`,`keep_request?`,`keep_response?` | Query the most recently saved recording | Quickly filter historical traffic |
| `mcp__charles__proxy_by_time` | `record_seconds` | Capture or read the latest traffic for a fixed duration | Quick time-window analysis |
| `mcp__charles__filter_func` | `capture_seconds`,`host_contains?`,`http_method?`,`keyword_regex?`,`keep_request?`,`keep_response?` | Filter traffic by time window and conditions | Quickly narrow scope |
| `mcp__charles__throttling` | `preset` | Set Charles network throttling preset | Reproduce poor-network behavior and verify responses |

### 5.4 Recommended Workflow

1. `charles_status`  
2. Confirm Charles is listening, the Android proxy is pointing to the capture machine, and the Charles certificate is installed for HTTPS if needed  
3. `reset_environment` (optional, for a clean experiment)  
4. `start_live_capture`  
5. Operate the App  
6. `query_live_capture_entries`  
7. `get_traffic_entry_detail`  
8. `group_capture_analysis` / `get_capture_analysis_stats`  
9. `stop_live_capture`, set `persist: true` if needed  
10. `analyze_recorded_traffic` / `query_recorded_traffic`

### 5.5 Call Examples

Start a live capture:

```json
{
  "reset_session": true,
  "include_existing": false
}
```

Filter live API traffic:

```json
{
  "capture_id": "capture-id-from-start",
  "preset": "api_focus",
  "host_contains": "api.example.com",
  "max_items": 10
}
```

### 5.6 Notes

- The `charles` MCP will not configure the Android system proxy for you; you must first complete Charles listener setup, device proxy configuration, and certificate installation
- For real-time retrieval, prefer `query_live_capture_entries` over `read_live_capture`, which advances the cursor
- `get_traffic_entry_detail` shows only a preview by default to save context; only enable `include_full_body` when the full content is truly needed
- If you want to review capture results later, use `persist: true` when stopping the live capture
- If Charles is already running and you do not want to clear the current session, use `adopt_existing: true`

---

## 6. `burp`: Burp Suite Integration

### 6.1 Role

The `burp` MCP is the control and data-access layer for Burp Suite, suited for:

- Reading proxy history
- Sending requests to Repeater / Intruder
- Sending HTTP/1.1 and HTTP/2 requests
- Generating Collaborator payloads
- Viewing scanner issues
- Reading and writing the current editor content
- Toggling proxy interception and task execution state
- Reading and writing Burp configuration

### 6.2 Method List

| Tool | Main Parameters | Purpose | Typical Use |
| --- | --- | --- | --- |
| `mcp__burp__base64_encode` | `content` | Base64 encode | Construct payloads |
| `mcp__burp__base64_decode` | `content` | Base64 decode | View encoded data |
| `mcp__burp__url_encode` | `content` | URL encode | Construct parameters |
| `mcp__burp__url_decode` | `content` | URL decode | Restore parameters |
| `mcp__burp__generate_random_string` | `length`,`characterSet` | Generate random string | Tokens, boundary values, probe strings |
| `mcp__burp__get_active_editor_contents` | none | Get current editor content | Read a manually edited request |
| `mcp__burp__set_active_editor_contents` | `text` | Set current editor content | Auto-populate a request template |
| `mcp__burp__create_repeater_tab` | `content`,`targetHostname`,`targetPort`,`usesHttps`,`tabName?` | Create a new Repeater tab | Send request to Repeater |
| `mcp__burp__send_to_intruder` | `content`,`targetHostname`,`targetPort`,`usesHttps`,`tabName?` | Send to Intruder | Brute-force / batch testing |
| `mcp__burp__send_http1_request` | `content`,`targetHostname`,`targetPort`,`usesHttps` | Send HTTP/1.1 request | Precise replay |
| `mcp__burp__send_http2_request` | `pseudoHeaders`,`headers`,`requestBody`,`targetHostname`,`targetPort`,`usesHttps` | Send HTTP/2 request | H2-specific scenarios |
| `mcp__burp__generate_collaborator_payload` | `customData?` | Generate OOB domain | SSRF / RCE / Blind XXE testing |
| `mcp__burp__get_collaborator_interactions` | `payloadId?` | Poll for OOB interactions | Check for outbound connections |
| `mcp__burp__get_proxy_http_history` | `count`,`offset` | Read proxy HTTP history | Review past requests |
| `mcp__burp__get_proxy_http_history_regex` | `count`,`offset`,`regex` | Filter HTTP history by regex | Precise filtering |
| `mcp__burp__get_proxy_websocket_history` | `count`,`offset` | Read WebSocket history | Analyze WebSocket traffic |
| `mcp__burp__get_proxy_websocket_history_regex` | `count`,`offset`,`regex` | Filter WebSocket history by regex | Find tokens, command fields |
| `mcp__burp__get_scanner_issues` | `count`,`offset` | List scanner findings | Vulnerability audit |
| `mcp__burp__output_project_options` | none | Export project-level configuration | View config schema |
| `mcp__burp__output_user_options` | none | Export user-level configuration | View config schema |
| `mcp__burp__set_project_options` | `json` | Set project-level configuration | Automated tuning |
| `mcp__burp__set_user_options` | `json` | Set user-level configuration | Global user settings |
| `mcp__burp__set_proxy_intercept_state` | `intercepting` | Toggle proxy interception | Enable/disable Intercept |
| `mcp__burp__set_task_execution_engine_state` | `running` | Toggle task execution engine | Pause/resume scan tasks |

### 6.3 Typical Call Examples

Create a Repeater tab:

```json
{
  "content": "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
  "targetHostname": "example.com",
  "targetPort": 443,
  "usesHttps": true,
  "tabName": "home"
}
```

Generate a Collaborator payload:

```json
{
  "customData": "ssrf-test"
}
```

### 6.4 Notes

- `send_http2_request` separates headers and body; do not include headers in the body
- Before changing configuration, run `output_project_options` / `output_user_options` first
- The OOB detection flow is typically: `generate_collaborator_payload` -> inject into the target -> `get_collaborator_interactions`
- `get_proxy_http_history_regex` is well suited for “auto-filtering relevant historical requests” in a skill

---

## 7. `chrome_devtools`: Browser Automation, Page Diagnostics, and Performance Analysis

### 7.1 Role

`chrome_devtools` handles automated control of browser pages and DevTools-level observation. Core capabilities include:

- Opening / closing / selecting pages
- Navigating, refreshing, emulating devices
- DOM snapshots, screenshots
- Clicking, typing, uploading files
- Listing network requests and console messages
- Executing page scripts
- Lighthouse audits
- Performance tracing
- Heap snapshots

If you need to “operate a page like a human in the browser,” this is the first choice.

### 7.2 Page and Context Control

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__list_pages` | none | List currently open pages |
| `mcp__chrome_devtools__new_page` | `url`,`background?`,`isolatedContext?`,`timeout?` | Open a new tab at the given URL |
| `mcp__chrome_devtools__select_page` | `pageId`,`bringToFront?` | Switch the active page |
| `mcp__chrome_devtools__close_page` | `pageId` | Close a page |
| `mcp__chrome_devtools__navigate_page` | `type`,`url?`,`timeout?`,`ignoreCache?`,`handleBeforeUnload?`,`initScript?` | URL navigation, forward, back, refresh |
| `mcp__chrome_devtools__resize_page` | `width`,`height` | Resize the browser window |
| `mcp__chrome_devtools__emulate` | `viewport?`,`colorScheme?`,`geolocation?`,`networkConditions?`,`userAgent?`,`cpuThrottlingRate?` | Device / network / UA emulation |

### 7.3 Page Structure and Screenshots

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__take_snapshot` | `filePath?`,`verbose?` | Get page a11y tree snapshot; returns element `uid` |
| `mcp__chrome_devtools__take_screenshot` | `filePath?`,`format?`,`fullPage?`,`quality?`,`uid?` | Screenshot of page or element |
| `mcp__chrome_devtools__wait_for` | `text`,`timeout?` | Wait for specific text to appear |

Notes:

- The most reliable approach is to call `take_snapshot` first, then use the returned `uid` for click/fill/hover
- `uid` is an element identifier in the current snapshot context; it may change after the snapshot is refreshed

### 7.4 Page Interaction

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__click` | `uid`,`dblClick?`,`includeSnapshot?` | Click an element |
| `mcp__chrome_devtools__hover` | `uid`,`includeSnapshot?` | Hover over an element |
| `mcp__chrome_devtools__drag` | `from_uid`,`to_uid`,`includeSnapshot?` | Drag and drop |
| `mcp__chrome_devtools__fill` | `uid`,`value`,`includeSnapshot?` | Fill a single input field |
| `mcp__chrome_devtools__fill_form` | `elements`,`includeSnapshot?` | Fill multiple form fields at once |
| `mcp__chrome_devtools__type_text` | `text`,`submitKey?` | Type text into the current focus |
| `mcp__chrome_devtools__press_key` | `key`,`includeSnapshot?` | Keyboard shortcuts, special keys |
| `mcp__chrome_devtools__upload_file` | `uid`,`filePath`,`includeSnapshot?` | Upload a file |
| `mcp__chrome_devtools__handle_dialog` | `action`,`promptText?` | Handle alert/confirm/prompt dialogs |

### 7.5 Page Scripts and Debug Information

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__evaluate_script` | `function`,`args?` | Execute JS inside the page |
| `mcp__chrome_devtools__list_console_messages` | `includePreservedMessages?`,`pageIdx?`,`pageSize?`,`types?` | View console logs |
| `mcp__chrome_devtools__get_console_message` | `msgid` | Get details for a single console message |
| `mcp__chrome_devtools__list_network_requests` | `includePreservedRequests?`,`pageIdx?`,`pageSize?`,`resourceTypes?` | View list of network requests |
| `mcp__chrome_devtools__get_network_request` | `reqid?`,`requestFilePath?`,`responseFilePath?` | View or export request details / body |

### 7.6 Auditing and Performance

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__chrome_devtools__lighthouse_audit` | `device?`,`mode?`,`outputDirPath?` | Run Lighthouse (excluding performance score) |
| `mcp__chrome_devtools__performance_start_trace` | `autoStop?`,`filePath?`,`reload?` | Start a performance trace |
| `mcp__chrome_devtools__performance_stop_trace` | `filePath?` | Stop a performance trace |
| `mcp__chrome_devtools__performance_analyze_insight` | `insightName`,`insightSetId` | Analyze a specific performance insight |
| `mcp__chrome_devtools__take_memory_snapshot` | `filePath` | Export a JS heap snapshot |

### 7.7 Recommended Workflows

#### Page Automation

1. `new_page`
2. `take_snapshot`
3. `click` / `fill` / `press_key`
4. `wait_for`
5. `take_screenshot`

#### Capturing Page Requests

1. `new_page`
2. Page interaction
3. `list_network_requests`
4. `get_network_request`

#### Performance Troubleshooting

1. `navigate_page`
2. `performance_start_trace`
3. Page actions or reload
4. `performance_stop_trace`
5. `performance_analyze_insight`

### 7.8 Notes

- Call `take_snapshot` before DOM interactions
- Old `uid` values may no longer be valid after a page refresh
- When retrieving request/response bodies, use `requestFilePath` / `responseFilePath` to save to file when needed
- If you care about “JS call chains and breakpoints,” `js_reverse` is usually more appropriate

---

## 8. `context7`: Real-Time Documentation and Example Retrieval

### 8.1 Role

`context7` is suited for querying third-party libraries, frameworks, official documentation, and code examples, especially in skill writing scenarios that require referencing the latest official usage.

### 8.2 Methods

#### `mcp__context7__resolve_library_id`

- Purpose: Resolve a “library name” into a document ID recognized by Context7
- Parameters:
  - `libraryName`
  - `query`
- Key return values:
  - `libraryId`
  - Library name
  - Description
  - Number of snippets
  - Source reputation
  - Benchmark score

#### `mcp__context7__query_docs`

- Purpose: Retrieve documentation and examples based on a previously resolved `libraryId`
- Parameters:
  - `libraryId`
  - `query`

### 8.3 Recommended Workflow

1. `resolve_library_id`
2. Select the most appropriate `libraryId`
3. `query_docs`

### 8.4 Examples

Resolve first:

```json
{
  "libraryName": "Next.js",
  "query": "App Router middleware authentication examples"
}
```

Then query:

```json
{
  "libraryId": "/vercel/next.js",
  "query": "How to protect routes in App Router middleware?"
}
```

### 8.5 Notes for Writing Skills

- If the user provides a vague library name, run `resolve_library_id` first
- This is a “documentation Q&A MCP,” not a general web search engine
- For technical questions, treat it primarily as an “official documentation retriever”

---

## 9. `everything_search`: Fast Local File Search

### 9.1 Role

This is a Windows local file search MCP, suited for quickly finding files under large directories, across the whole disk, or with fuzzy conditions.

### 9.2 Methods

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__everything_search__search` | `query`,`maxResults?`,`parentPath?`,`filesOnly?`,`foldersOnly?`,`matchPath?`,`regex?`,`caseSensitive?`,`wholeWord?`,`sortBy?`,`sortDescending?`,`showSize?`,`showDateModified?` | Search for files or directories |
| `mcp__everything_search__get_file_info` | `filename` | Get detailed information about a specific file |

### 9.3 Examples

Search for all `.apk` files under a specific directory:

```json
{
  "query": "*.apk",
  "parentPath": "C:\\Users\\28484",
  "filesOnly": true,
  "maxResults": 50
}
```

### 9.4 Use Cases

- Finding APKs / SOs / logs / exported files
- Locating target files for reverse-engineering skills
- Finding configuration, scripts, databases, and certificates in large directories

---

## 10. `fetch`: General-Purpose Web Scraping

### 10.1 Role

`fetch` is the general-purpose tool for “fetching web page / URL content,” suited for:

- Pulling web page content
- Fetching documentation pages
- Reading HTML
- Simple web content extraction

### 10.2 Methods

#### `mcp__fetch__fetch`

- Parameters:
  - `url`
  - `max_length?`
  - `raw?`
  - `start_index?`
- Purpose:
  - Retrieve web page content
  - Can return simplified markdown-style content
  - Supports offset-based reading for long pages

### 10.3 Examples

```json
{
  "url": "https://example.com",
  "max_length": 6000
}
```

### 10.4 Notes

- Better suited for “fetching content from a known URL,” not a search engine
- For very long pages, use `start_index` to read in segments
- In technical documentation scenarios, prefer `context7` when available

---

## 11. `frida_mcp`: Android Dynamic Injection and Runtime Hooking

### 11.1 Role

`frida_mcp` is the Android dynamic analysis layer. Core uses:

- Checking / starting / stopping `frida-server`
- Enumerating applications
- Getting the current foreground application
- `spawn` or `attach` to a target process
- Injecting Frida JS scripts
- Retrieving script output logs

Suitable scenarios:

- SSL Pinning bypass
- Printing method arguments / return values
- Dynamically capturing signatures, tokens, and headers
- Runtime observation at the native / Java layer

### 11.2 Method List

| Tool | Main Parameters | Purpose | Typical Use |
| --- | --- | --- | --- |
| `mcp__frida_mcp__check_frida_status` | none | Check if frida-server is running | Pre-flight check |
| `mcp__frida_mcp__start_frida_server` | none | Start frida-server | Prepare for dynamic analysis |
| `mcp__frida_mcp__stop_frida_server` | none | Stop frida-server | Clean up environment |
| `mcp__frida_mcp__list_applications` | none | List device applications | Find package name, check if running |
| `mcp__frida_mcp__get_frontmost_application` | none | Get the current foreground application | Confirm the package name of the current screen |
| `mcp__frida_mcp__spawn` | `package_name`,`initial_script?`,`script_file_path?`,`output_file?` | Suspend-start and attach to the target application | Early-stage hooking |
| `mcp__frida_mcp__attach` | `target`,`initial_script?`,`script_file_path?`,`output_file?` | Attach to a PID or package name | Inject into an already-running application |
| `mcp__frida_mcp__get_messages` | `max_messages?` | Retrieve hook/log output buffer | View script output |

### 11.3 Difference Between `attach` and `spawn`

- `attach`
  - Used when the target is already running
  - Can attach by PID or package name
  - Suitable for temporary observation and late-stage hooking

- `spawn`
  - Used to inject a script before the application resumes
  - Suitable for early class loading, startup flows, signature initialization, and early SSL pinning bypass

### 11.4 Examples

Check status:

```json
{}
```

Spawn by package name and inject a script file:

```json
{
  "package_name": "com.example.app",
  "script_file_path": "C:\\Users\\28484\\Desktop\\hook.js",
  "output_file": "C:\\Users\\28484\\Desktop\\frida.log"
}
```

Attach to a running application with an inline script:

```json
{
  "target": "com.example.app",
  "initial_script": "Java.perform(function(){ console.log('hook loaded'); });"
}
```

### 11.5 Recommended Workflow

1. `check_frida_status`
2. If not running, call `start_frida_server`
3. `list_applications` or `get_frontmost_application`
4. `spawn` or `attach`
5. `get_messages`

### 11.6 Notes

- The device environment must have `frida-server` properly deployed
- `script_file_path` takes precedence over `initial_script`
- Most signature / encryption locating tasks follow the pattern: `jadx` static location -> `frida_mcp` dynamic verification

---

## 12. `ida_pro_mcp`: IDA Pro Static Analysis and Batch Restructuring

### 12.1 Role

`ida_pro_mcp` is the heaviest static analysis MCP in the current toolkit. It covers far more than “just viewing decompilation”:

- Opening / switching IDA instances
- Quick binary survey
- Listing functions, globals, imports, and types
- Looking up xrefs / call graphs / basic blocks
- Decompiling, disassembling, and exporting function information
- Editing comments, renaming, declaring types, creating stack variables
- Reading memory, patching bytes, patching assembly
- Running Python scripts within the IDA context

If a skill targets native reverse engineering, malware analysis, patching, or batch renaming, this MCP is essentially the core.

### 12.2 Strongly Recommended Entry Tool

#### `mcp__ida_pro_mcp__survey_binary`

This is the best tool to use as a first-step triage. It provides in one call:

- File metadata
- Segment layout
- Entry points
- Statistics
- High-frequency strings
- High-value functions
- Classified imports
- Call-graph overview

When writing a skill, you can explicitly require:  
“After opening the IDB, call `survey_binary` first — do not blindly jump to `list_funcs`.”

### 12.3 Instance and Session Management

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__list_instances` | none | List currently connectable IDA instances |
| `mcp__ida_pro_mcp__select_instance` | `port`,`host?` | Switch the IDA instance the MCP points to |
| `mcp__ida_pro_mcp__open_file` | `file_path`,`autonomous?`,`new_database?`,`switch?`,`timeout?` | Open a file in a new IDA instance |
| `mcp__ida_pro_mcp__server_health` | none | Check current IDB / server health |
| `mcp__ida_pro_mcp__server_warmup` | `build_caches?`,`init_hexrays?`,`wait_auto_analysis?` | Warm up the analysis environment |
| `mcp__ida_pro_mcp__idb_save` | `path?` | Save the current IDB |

### 12.4 Binary Overview and Discovery

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__survey_binary` | `detail_level?` | Binary overview |
| `mcp__ida_pro_mcp__entity_query` | complex query object | Query functions/globals/imports/strings/names |
| `mcp__ida_pro_mcp__find_regex` | `pattern`,`limit?`,`offset?` | Regex search in strings |
| `mcp__ida_pro_mcp__find` | `targets`,`type`,`limit?`,`offset?` | Search strings, immediates, data/code references |
| `mcp__ida_pro_mcp__find_bytes` | `patterns`,`limit?`,`offset?` | Byte-pattern search |

### 12.5 Function and Graph Analysis

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__list_funcs` | `queries` | List functions |
| `mcp__ida_pro_mcp__func_query` | filter condition set | Filter functions by size/name/type presence |
| `mcp__ida_pro_mcp__func_profile` | query set | Generate an overview profile for functions |
| `mcp__ida_pro_mcp__lookup_funcs` | `queries` | Look up functions by address or name |
| `mcp__ida_pro_mcp__callees` | `addrs`,`limit?` | Query callees of a function |
| `mcp__ida_pro_mcp__callgraph` | `roots`,`max_depth?`,`max_nodes?`,`max_edges?`,`max_edges_per_func?` | Build a call graph |
| `mcp__ida_pro_mcp__basic_blocks` | `addrs`,`offset?`,`max_blocks?` | Get CFG basic blocks |
| `mcp__ida_pro_mcp__analyze_function` | `addr`,`include_asm?` | Compact single-function analysis |
| `mcp__ida_pro_mcp__analyze_batch` | `queries` | Batch comprehensive analysis of multiple functions |
| `mcp__ida_pro_mcp__analyze_component` | `addrs` | Component analysis for a set of related functions |

### 12.6 Decompilation, Disassembly, and Export

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__decompile` | `addr` | Decompile a function |
| `mcp__ida_pro_mcp__disasm` | `addr`,`offset?`,`max_instructions?`,`include_total?` | Disassemble a function |
| `mcp__ida_pro_mcp__export_funcs` | `addrs`,`format?` | Export functions as JSON / C headers / prototypes |

### 12.7 Cross-References and Data Flow

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__xrefs_to` | `addrs`,`limit?` | Get xrefs to an address |
| `mcp__ida_pro_mcp__xref_query` | query set | Batch query xrefs by direction/type |
| `mcp__ida_pro_mcp__trace_data_flow` | `addr`,`direction?`,`max_depth?` | Trace multi-hop data flow |
| `mcp__ida_pro_mcp__xrefs_to_field` | `queries` | Query references to struct fields |

### 12.8 Type System and Structure Recovery

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__type_query` | query set | Query local types |
| `mcp__ida_pro_mcp__type_inspect` | `queries` | View type declarations and members |
| `mcp__ida_pro_mcp__declare_type` | `decls` | Inject C type declarations |
| `mcp__ida_pro_mcp__set_type` | `edits` | Set function/variable/local variable types |
| `mcp__ida_pro_mcp__type_apply_batch` | `batch` | Batch apply types |
| `mcp__ida_pro_mcp__infer_types` | `addrs` | Infer types |
| `mcp__ida_pro_mcp__enum_upsert` | `queries` | Create or extend enumerations |
| `mcp__ida_pro_mcp__search_structs` | `filter` | Search structs / unions |
| `mcp__ida_pro_mcp__read_struct` | `queries` | Read struct field values at an address |

### 12.9 Stack Frames and Local Variables

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__stack_frame` | `addrs` | Get the stack frame of a function |
| `mcp__ida_pro_mcp__declare_stack` | `items` | Declare stack variables |
| `mcp__ida_pro_mcp__delete_stack` | `items` | Delete stack variables |

### 12.10 Renaming, Comments, and Diff Verification

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__rename` | `batch` | Batch rename functions/data/locals/stack variables |
| `mcp__ida_pro_mcp__set_comments` | `items` | Set comments |
| `mcp__ida_pro_mcp__append_comments` | `items` | Append comments |
| `mcp__ida_pro_mcp__diff_before_after` | `addr`,`action`,`action_args` | Compare decompilation before/after applying a rename/type/comment |

### 12.11 Raw Memory Reading and Patching

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__get_bytes` | `regions` | Read bytes |
| `mcp__ida_pro_mcp__get_int` | `queries` | Read integers |
| `mcp__ida_pro_mcp__get_string` | `addrs` | Read strings |
| `mcp__ida_pro_mcp__get_global_value` | `queries` | Read global variable values |
| `mcp__ida_pro_mcp__put_int` | `items` | Write integers |
| `mcp__ida_pro_mcp__patch` | `patches` | Patch bytes |
| `mcp__ida_pro_mcp__patch_asm` | `items` | Patch assembly |
| `mcp__ida_pro_mcp__undefine` | `items` | Undefine back to raw bytes |
| `mcp__ida_pro_mcp__define_code` | `items` | Define bytes as code |
| `mcp__ida_pro_mcp__define_func` | `items` | Define a function |

### 12.12 Imports, Globals, Instructions, and Entity Queries

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__imports` | `count`,`offset` | List imports |
| `mcp__ida_pro_mcp__imports_query` | `queries` | Filter imports by module/name |
| `mcp__ida_pro_mcp__list_globals` | `queries` | List global variables |
| `mcp__ida_pro_mcp__insn_query` | `queries` | Query instruction patterns |
| `mcp__ida_pro_mcp__int_convert` | `inputs` | Number format conversion |

### 12.13 Python Extension

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__ida_pro_mcp__py_eval` | `code` | Execute a Python snippet in the IDA environment |
| `mcp__ida_pro_mcp__py_exec_file` | `file_path` | Execute an entire Python script file |

### 12.14 Recommended Workflows

#### Initial Triage

1. `server_health`
2. `server_warmup`
3. `survey_binary`
4. `find_regex` / `imports_query`
5. `analyze_function` / `decompile`

#### Recovering Semantics

1. `decompile`
2. `stack_frame`
3. `type_query` / `type_inspect`
4. `set_type` / `declare_type`
5. `rename`
6. `diff_before_after`

#### Tracing Sensitive Strings

1. `find_regex`
2. `xrefs_to`
3. `trace_data_flow`
4. `analyze_component`

### 12.15 Skill Writing Suggestions

- Hard-coding “run `survey_binary` first” at the start is usually a good strategy
- For batch renaming, treating `diff_before_after` as a verification step is recommended
- For analyzing JNI / crypto / dispatch tables, `trace_data_flow` is very valuable
- `type_apply_batch` is suited for “auto-fix types” skills
- `py_eval` / `py_exec_file` are suitable for advanced automation, but script boundaries should be carefully defined

---

## 13. `jadx`: APK Static Decompilation and Android Code Navigation

### 13.1 Role

The `jadx` MCP is the Android static analysis entry point, suited for:

- Reading `AndroidManifest.xml`
- Finding the main Activity, components, and exported components
- Searching classes / methods / fields
- Getting class source code, method source code, and smali
- Querying references
- Renaming classes / methods / fields / variables / packages

Its difference from `ida_pro_mcp`:

- `jadx` leans more toward Java/Kotlin-layer APKs
- `ida_pro_mcp` leans more toward native binaries / sos / ELFs / PEs

### 13.2 Entry Information and Manifest

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__get_android_manifest` | none | Get the full Manifest |
| `mcp__jadx__get_main_activity_class` | none | Get the main Activity |
| `mcp__jadx__get_main_application_classes_names` | none | Get primary class names in the main application package |
| `mcp__jadx__get_main_application_classes_code` | `count?`,`offset?` | Get primary class source code |
| `mcp__jadx__get_manifest_component` | `component_type`,`only_exported?` | Get activity/service/provider/receiver component information |

### 13.3 Class and Source Reading

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__get_all_classes` | `count?`,`offset?` | Get all class names |
| `mcp__jadx__fetch_current_class` | none | Get the source of the currently selected class in the GUI |
| `mcp__jadx__get_class_source` | `class_name` | Get the Java source of a class |
| `mcp__jadx__get_smali_of_class` | `class_name` | Get the smali of a class |
| `mcp__jadx__get_methods_of_class` | `class_name` | List methods |
| `mcp__jadx__get_fields_of_class` | `class_name` | List fields |
| `mcp__jadx__get_method_by_name` | `class_name`,`method_name` | Get the source of a specific method |
| `mcp__jadx__get_selected_text` | none | Get the currently selected text |

### 13.4 Resources and Strings

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__get_all_resource_file_names` | `count?`,`offset?` | List resource files |
| `mcp__jadx__get_resource_file` | `resource_name` | Read a resource file's content |
| `mcp__jadx__get_strings` | `count?`,`offset?` | Get strings.xml content |

### 13.5 Search and References

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__search_classes_by_keyword` | `search_term`,`package?`,`search_in?`,`offset?`,`count?` | Cross-code search of classes/methods/fields/code content |
| `mcp__jadx__search_method_by_name` | `method_name` | Search by method name |
| `mcp__jadx__get_xrefs_to_class` | `class_name`,`count?`,`offset?` | Query class references |
| `mcp__jadx__get_xrefs_to_field` | `class_name`,`field_name`,`count?`,`offset?` | Query field references |
| `mcp__jadx__get_xrefs_to_method` | `class_name`,`method_name`,`count?`,`offset?` | Query method references |

### 13.6 Renaming

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__rename_class` | `class_name`,`new_name` | Rename a class |
| `mcp__jadx__rename_field` | `class_name`,`field_name`,`new_name` | Rename a field |
| `mcp__jadx__rename_method` | `method_name`,`new_name` | Rename a method |
| `mcp__jadx__rename_variable` | `class_name`,`method_name`,`variable_name`,`new_name`,`reg?`,`ssa?` | Rename a variable |
| `mcp__jadx__rename_package` | `old_package_name`,`new_package_name` | Rename a package |

### 13.7 Debugging

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__jadx__debug_get_threads` | none | View debug threads |
| `mcp__jadx__debug_get_stack_frames` | none | View the current call stack |
| `mcp__jadx__debug_get_variables` | none | View current variables |

### 13.8 Recommended Workflows

#### Initial APK Analysis

1. `get_android_manifest`
2. `get_main_activity_class`
3. `get_manifest_component`
4. `search_classes_by_keyword`
5. `get_class_source`

#### Signature / Interface Location

1. `search_classes_by_keyword` for `okhttp`, `retrofit`, `sign`, `token`, `encrypt`
2. `get_xrefs_to_method`
3. `get_method_by_name`
4. Switch to `frida_mcp` for dynamic verification when needed

### 13.9 Notes

- `search_classes_by_keyword` is a very high-value entry tool in `jadx`
- `search_in` can be set to `class,method,field,code,comment`
- For JNI scenarios, typically `jadx` finds the native registration point and `ida_pro_mcp` digs into the so

---

## 14. `js_reverse`: Web Front-End JavaScript Reverse Engineering and Breakpoint Debugging

### 14.1 Role

`js_reverse` is a professional MCP for web front-end reverse engineering. Its difference from `chrome_devtools`:

- `chrome_devtools` leans more toward page operations, network, snapshots, and performance
- `js_reverse` leans more toward JS source code, breakpoints, call chains, XHR initiators, function tracing, and source saving

Applicable scenarios:

- Analyzing signature functions
- Tracing XHR/Fetch initiator chains
- Locating obfuscated functions
- Searching for keywords in JS source
- Getting variables in execution context
- Analyzing WebSocket message patterns

### 14.2 Page and Context

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__new_page` | `url`,`timeout?` | Open a new page |
| `mcp__js_reverse__select_page` | `pageIdx?` | List or switch pages |
| `mcp__js_reverse__navigate_page` | `type`,`url?`,`timeout?`,`ignoreCache?` | Navigate / refresh |
| `mcp__js_reverse__select_frame` | `frameIdx?` | List or switch frames/iframes |

### 14.3 Script Enumeration and Source Reading

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__list_scripts` | `filter?` | List current page scripts |
| `mcp__js_reverse__search_in_sources` | `query`,`isRegex?`,`caseSensitive?`,`excludeMinified?`,`urlFilter?`,`maxResults?`,`maxLineLength?` | Search across all scripts |
| `mcp__js_reverse__get_script_source` | `url?`,`scriptId?`,`startLine?`,`endLine?`,`offset?`,`length?` | Read a small source snippet |
| `mcp__js_reverse__save_script_source` | `filePath`,`url?`,`scriptId?` | Save a complete script to local file |

Notes:

- `get_script_source` is designed for “viewing a local excerpt,” not pulling the entire file
- Use `save_script_source` for large scripts

### 14.4 Breakpoints, Tracing, and Execution Control

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__set_breakpoint_on_text` | `text`,`urlFilter?`,`occurrence?`,`condition?` | Auto-set breakpoints by code text |
| `mcp__js_reverse__list_breakpoints` | none | List breakpoints |
| `mcp__js_reverse__remove_breakpoint` | `breakpointId?`,`url?` | Remove a breakpoint or XHR breakpoint |
| `mcp__js_reverse__pause_or_resume` | none | Pause or resume execution |
| `mcp__js_reverse__step` | `direction` | Step over/into/out |
| `mcp__js_reverse__trace_function` | `functionName`,`logArgs?`,`logThis?`,`pause?`,`traceId?`,`urlFilter?` | Trace function calls |
| `mcp__js_reverse__inject_before_load` | `script?`,`identifier?` | Inject a script before page load |

### 14.5 Context Analysis After Breakpoint Hit

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__get_paused_info` | `frameIndex?`,`includeScopes?`,`maxScopeDepth?` | Get call stack and scope variables at breakpoint hit |
| `mcp__js_reverse__evaluate_script` | `function`,`frameIndex?`,`mainWorld?` | Execute JS in the current page or breakpoint frame |

### 14.6 Network and Call Chain

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__break_on_xhr` | `url` | Set breakpoint on XHR/Fetch containing the target URL |
| `mcp__js_reverse__list_network_requests` | `reqid?`,`pageIdx?`,`pageSize?`,`resourceTypes?`,`urlFilter?`,`includePreservedRequests?` | View request list or single request details |
| `mcp__js_reverse__get_request_initiator` | `requestId` | View which JS code initiated a request |
| `mcp__js_reverse__list_console_messages` | `msgid?`,`pageIdx?`,`pageSize?`,`types?`,`includePreservedMessages?` | View console messages |

### 14.7 WebSocket Analysis

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__get_websocket_messages` | `wsid?`,`analyze?`,`groupId?`,`frameIndex?`,`direction?`,`show_content?`,`pageIdx?`,`pageSize?`,`urlFilter?`,`includePreservedConnections?` | List WS connections, analyze message groups, view specific frames |

### 14.8 Screenshot

| Tool | Main Parameters | Purpose |
| --- | --- | --- |
| `mcp__js_reverse__take_screenshot` | `filePath?`,`format?`,`fullPage?`,`quality?` | Take a screenshot |

### 14.9 Recommended Workflows

#### Locating a Signature Function

1. `new_page`
2. `list_scripts`
3. `search_in_sources` for `sign` / `token` / path keywords
4. `set_breakpoint_on_text`
5. Trigger the request
6. `get_paused_info`
7. `step`
8. `evaluate_script`

#### Tracing Who Initiated a Request

1. Interact with the page
2. `list_network_requests`
3. `get_request_initiator`
4. `break_on_xhr` if needed

#### Analyzing an Obfuscated Script

1. `search_in_sources`
2. `save_script_source`
3. `set_breakpoint_on_text`
4. `trace_function`

### 14.10 Skill Writing Suggestions

- When a source keyword is available, prefer `search_in_sources`
- When a request URL is known, prefer `break_on_xhr` or `get_request_initiator`
- When you need to get global variables in the page script scope, consider `mainWorld: true`
- If the page reloads frequently, query scripts by URL rather than relying heavily on temporary `scriptId` values

---

## 15. `memory`：结构化知识图谱记忆

### 15.1 定位

`memory` 是长期结构化记忆层，不是普通笔记。它维护的是“实体-观察-关系”的知识图谱。

适合用来：

- 记录用户偏好
- 记录项目事实
- 记录设备、目标、包名、接口名、漏洞点等结构化知识
- 在多轮任务之间保存稳定事实

### 15.2 核心对象

- 实体 `entity`
  - 有名字 `name`
  - 有类型 `entityType`
  - 有多条观察 `observations`

- 关系 `relation`
  - `from`
  - `relationType`
  - `to`

### 15.3 方法清单

| 工具 | 主要参数 | 作用 |
| --- | --- | --- |
| `mcp__memory__read_graph` | 无 | 读取整个图谱 |
| `mcp__memory__search_nodes` | `query` | 搜实体/类型/观察 |
| `mcp__memory__open_nodes` | `names` | 打开指定实体详情 |
| `mcp__memory__create_entities` | `entities` | 批量创建实体 |
| `mcp__memory__delete_entities` | `entityNames` | 删除实体 |
| `mcp__memory__add_observations` | `observations` | 给实体追加观察 |
| `mcp__memory__delete_observations` | `deletions` | 删除观察 |
| `mcp__memory__create_relations` | `relations` | 创建关系 |
| `mcp__memory__delete_relations` | `relations` | 删除关系 |

### 15.4 示例

创建实体：

```json
{
  "entities": [
    {
      "name": "com.example.app",
      "entityType": "android_app",
      "observations": [
        "主包名",
        "使用 OkHttp"
      ]
    }
  ]
}
```

创建关系：

```json
{
  "relations": [
    {
      "from": "com.example.app",
      "relationType": "uses",
      "to": "OkHttp"
    }
  ]
}
```

### 15.5 适合 skill 的用途

- 在逆向 skill 中记住目标包名、加密类、so 名、关键接口
- 在渗透测试 skill 中记住域名、漏洞点、扫描结果
- 在自动化 skill 中记住账号环境、部署方式、约定路径

### 15.6 注意点

- 关系建议用主动语态，例如 `App uses OkHttp`
- 不适合存超长原文，更适合存“可检索事实”

---

## 16. `sequential_thinking`：分步思考辅助

### 16.1 定位

这是一个“显式多步思考”工具，用于复杂问题分析、修正、分支、验证假设。  
它适合做：

- 多步骤逆向分析规划
- 不确定任务的方案探索
- 需要修正前面判断的复杂决策
- 大任务分解

### 16.2 方法

#### `mcp__sequential_thinking__sequentialthinking`

主要参数：

- `thought`
- `thoughtNumber`
- `totalThoughts`
- `nextThoughtNeeded`
- `isRevision?`
- `revisesThought?`
- `branchFromThought?`
- `branchId?`
- `needsMoreThoughts?`

### 16.3 使用方式理解

这个工具不是用来“查数据”的，而是用来把推理状态结构化地提交给系统。  
你可以：

- 从第 1 步开始分析
- 发现前面错了就 revision
- 从某一步分叉 branch
- 最后形成一个经过验证的解法

### 16.4 适合 skill 的场景

- 自动 triage skill
- 多阶段漏洞利用路线判断
- 逆向中“先 Java 还是先 native”的决策
- 多候选签名函数筛选

### 16.5 示例

```json
{
  "thought": "先确认问题是前端签名还是服务端校验导致 403。",
  "thoughtNumber": 1,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}
```

### 16.6 注意点

- 这是分析增强器，不是执行器
- 对简单任务没必要使用
- 对复杂、模糊、容易走错路的问题尤其有价值

---

## 17. `scrcpy_vision`：Android 可视化控制、UI 定位与无线调试

### 17.1 定位

`scrcpy_vision` 把 ADB、scrcpy 低延迟控制、屏幕截图/串流、`uiautomator` UI 树读取整合到一组工具里，适合做：

- 以 `serial` 为核心的 Android 设备连接与识别
- 基于当前页面元素文本、`resource-id`、`content-desc` 的 UI 定位
- 坐标点击、拖拽、长按、滑动、键盘输入
- 屏幕唤醒/解锁、前台 Activity、通知、剪贴板等状态确认
- USB 转 WiFi ADB 调试
- 单帧截图或持续画面流，用于观察界面变化和自动化联动

和 `adb_mcp` 相比，它更偏“可视化控制”和“UI 层定位”；`adb_mcp` 更偏基础设备管理、安装 APK、logcat、录屏、文件传输。写 skill 时两者通常是互补关系，而不是二选一。

### 17.2 适合的 skill 类型

- Android UI 自动化与页面回归
- App 动态测试中的元素定位与界面驱动
- 无线调试切换与真机远程控制
- 抓包/Hook 前后的页面状态验证
- 需要通过 UI 树确认按钮、输入框、弹窗位置的任务
- 需要连续查看设备画面而不是只截单张图的任务

### 17.3 方法清单

#### 设备连接与识别

| 工具 | 主要参数 | 作用 | 典型用途 |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_devices_list` | 无 | 列出已连接设备 | 获取 `serial`，确认 USB/WiFi 连接是否正常 |
| `mcp__scrcpy_vision__android_devices_info` | `serial` | 读取设备基础 `getprop` 信息 | 看型号、系统版本、ABI、设备标识 |
| `mcp__scrcpy_vision__android_adb_enableTcpip` | `serial`,`port?` | 在 USB 已连接时开启 WiFi 调试 | 为无线 ADB 做前置准备 |
| `mcp__scrcpy_vision__android_adb_getDeviceIp` | `serial` | 获取设备 WiFi IP | 准备 `connectWifi` |
| `mcp__scrcpy_vision__android_adb_connectWifi` | `ipAddress`,`port?` | 通过 WiFi 连接设备 | 无线调试 |
| `mcp__scrcpy_vision__android_adb_disconnectWifi` | `ipAddress?` | 断开指定或全部 WiFi ADB 连接 | 清理无线调试会话 |

#### 应用与运行态

| 工具 | 主要参数 | 作用 | 典型用途 |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_app_start` | `serial`,`packageName`,`activity?` | 启动应用或指定 Activity | 打开目标 App、直达指定页面 |
| `mcp__scrcpy_vision__android_app_stop` | `serial`,`packageName` | 强制停止应用 | 重置应用状态 |
| `mcp__scrcpy_vision__android_apps_list` | `serial`,`system?` | 列出已安装包 | 找包名、确认应用是否安装 |
| `mcp__scrcpy_vision__android_activity_current` | `serial` | 获取当前前台包名与 Activity | 判断当前页面是否切换成功 |
| `mcp__scrcpy_vision__android_notifications_get` | `serial` | 导出当前通知详情 | 查验证码通知、推送文案、包名来源 |

#### 屏幕、剪贴板与设备状态

| 工具 | 主要参数 | 作用 | 典型用途 |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_screen_isOn` | `serial` | 判断屏幕是否点亮 | 自动化前检查设备状态 |
| `mcp__scrcpy_vision__android_screen_wake` | `serial` | 点亮屏幕 | 准备操作设备 |
| `mcp__scrcpy_vision__android_screen_sleep` | `serial` | 熄灭屏幕 | 收尾或验证锁屏行为 |
| `mcp__scrcpy_vision__android_screen_unlock` | `serial` | 尝试唤醒并解锁设备 | 无安全锁时快速进入桌面 |
| `mcp__scrcpy_vision__android_clipboard_get` | `serial` | 读取剪贴板内容 | 取验证码、分享链接、复制结果 |
| `mcp__scrcpy_vision__android_clipboard_set` | `serial`,`text` | 尝试设置剪贴板 | 向输入框粘贴准备好的文本 |

#### 文件与 Shell

| 工具 | 主要参数 | 作用 | 典型用途 |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_file_list` | `serial`,`path` | 列出设备目录内容 | 查看导出目录、缓存目录、下载目录 |
| `mcp__scrcpy_vision__android_file_pull` | `serial`,`remotePath`,`localPath` | 从设备拉文件到本地 | 导出日志、图片、下载文件 |
| `mcp__scrcpy_vision__android_file_push` | `serial`,`localPath`,`remotePath` | 推送本地文件到设备 | 推配置、测试文件、证书 |
| `mcp__scrcpy_vision__android_shell_exec` | `serial`,`command` | 执行任意 `adb shell` 命令 | 在必须时做高级诊断、分辨率查询或设备操作 |

#### UI 树读取与输入控制

| 工具 | 主要参数 | 作用 | 典型用途 |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_ui_dump` | `serial` | 导出当前页面的 `uiautomator` XML | 获取元素文本、类名、边界、`resource-id` |
| `mcp__scrcpy_vision__android_ui_findElement` | `serial`,`text?`,`resourceId?`,`className?`,`contentDesc?` | 按 UI 属性查元素并返回中心坐标 | 定位按钮、输入框、弹窗控件 |
| `mcp__scrcpy_vision__android_input_tap` | `serial`,`x`,`y` | 点击坐标 | 点按钮、列表项、菜单 |
| `mcp__scrcpy_vision__android_input_longPress` | `serial`,`x`,`y`,`durationMs?` | 长按坐标 | 呼出上下文菜单、拖动态准备 |
| `mcp__scrcpy_vision__android_input_swipe` | `serial`,`x1`,`y1`,`x2`,`y2`,`durationMs?` | 滑动屏幕 | 滚动列表、切页、下拉刷新 |
| `mcp__scrcpy_vision__android_input_dragDrop` | `serial`,`startX`,`startY`,`endX`,`endY`,`durationMs?` | 拖拽到目标位置 | 拖动卡片、图标、排序项 |
| `mcp__scrcpy_vision__android_input_pinch` | `serial`,`centerX`,`centerY`,`startDistance`,`endDistance`,`durationMs?` | 近似模拟缩放手势 | 地图、图片缩放验证 |
| `mcp__scrcpy_vision__android_input_keyevent` | `serial`,`keycode` | 发送 Android 按键 | Home、Back、Enter、Delete、音量键 |
| `mcp__scrcpy_vision__android_input_text` | `serial`,`text` | 输入文本 | 登录、搜索、表单填写 |

#### 视觉能力

| 工具 | 主要参数 | 作用 | 典型用途 |
| --- | --- | --- | --- |
| `mcp__scrcpy_vision__android_vision_snapshot` | `serial` | 通过 `adb exec-out screencap -p` 获取当前屏幕 PNG | 单次截图确认界面 |
| `mcp__scrcpy_vision__android_vision_startStream` | `serial`,`frameFps?`,`maxFps?`,`maxSize?` | 启动 scrcpy+ffmpeg 持续画面流 | 持续观察页面变化，配合快速输入控制 |
| `mcp__scrcpy_vision__android_vision_stopStream` | `serial` | 停止画面流并移除资源 | 收尾，释放流资源 |

### 17.4 推荐工作流

#### 页面自动化与定位

1. `android_devices_list`
2. `android_screen_isOn` / `android_screen_wake` / `android_screen_unlock`
3. 如果后续要用坐标点击或滑动，先用 `android_shell_exec` 执行 `wm size` 获取当前分辨率
4. `android_vision_snapshot` 或 `android_vision_startStream`
5. `android_ui_dump` 或 `android_ui_findElement`
6. `android_input_tap` / `android_input_text` / `android_input_swipe`
7. `android_activity_current` 确认是否进入目标页面
8. 需要持续观察时保留 stream，结束后 `android_vision_stopStream`

#### WiFi ADB 切换

1. USB 连接设备后执行 `android_adb_enableTcpip`
2. `android_adb_getDeviceIp`
3. `android_adb_connectWifi`
4. `android_devices_list` 确认无线连接已出现
5. 测试完成后用 `android_adb_disconnectWifi` 清理

### 17.5 调用示例

开启 WiFi 调试：

```json
{
  "serial": "R58N123456A",
  "port": 5555
}
```

按文本找元素：

```json
{
  "serial": "R58N123456A",
  "text": "登录"
}
```

启动持续画面流：

```json
{
  "serial": "R58N123456A",
  "frameFps": 5,
  "maxSize": 1080
}
```

查询当前分辨率：

```json
{
  "serial": "R58N123456A",
  "command": "wm size"
}
```

### 17.6 注意点

- 除 `android_devices_list`、`android_adb_connectWifi`、`android_adb_disconnectWifi` 之外，大多数方法都要求先拿到设备 `serial`
- 如果 scrcpy 画面流已启动，点击、滑动、输入等操作会优先走更快的 scrcpy 控制通道；否则回退到 ADB 输入
- 如果要发坐标点击、长按、滑动、拖拽或 pinch，先查询当前分辨率；不同设备、横竖屏、缩放或截图尺寸假设都可能导致坐标偏移
- `android_ui_findElement` 适合当前页面的静态定位，页面变化后建议重新 `ui_dump` 或重新查元素
- 能用 `android_ui_findElement` / `android_ui_dump` 就尽量别直接写死坐标；只有在元素定位不可靠时才退回坐标点击
- `android_screen_unlock` 只适用于没有 PIN/密码/图案等安全锁的设备
- `android_clipboard_set` 在 Android 10+ 上可能受到系统限制，不保证所有设备都能直接生效
- `android_input_pinch` 是近似手势，不是真正的多点触控
- `android_shell_exec`、`android_file_push` 会直接改动设备环境，写 skill 时应明确这是高风险操作
- `android_vision_startStream` 产出的是实时资源而不是落地文件；如果只是单次截图，优先用 `android_vision_snapshot`

---

## 18. 结合 skill 编写的推荐分组

为了后续写 skill，更推荐你按“任务域”来组织，而不是按“工具服务器名”机械拆分。

### 18.1 Android 静态分析 skill

优先 MCP：

- `jadx`
- `everything_search`

常见流程：

1. 找 APK / 资源
2. 读 Manifest
3. 搜关键类
4. 拉方法源码
5. 追 xref

### 18.2 Android 动态分析 skill

优先 MCP：

- `adb_mcp`
- `scrcpy_vision`
- `frida_mcp`
- `charles`

常见流程：

1. 确认设备
2. 安装应用
3. 视情况启动 scrcpy 画面流或读取 UI 树
4. 启动 Charles live capture
5. 注入 hook
6. 查看请求、界面和日志

### 18.3 Native 逆向 skill

优先 MCP：

- `ida_pro_mcp`
- `everything_search`

常见流程：

1. 找 so / exe
2. `survey_binary`
3. 查字符串/导入
4. 反编译关键函数
5. 重命名、修类型、追数据流

### 18.4 Web 页面自动化 skill

优先 MCP：

- `chrome_devtools`

常见流程：

1. 打开页面
2. 获取快照
3. 交互表单
4. 抓请求
5. 截图留证

### 18.5 Web JS 逆向 skill

优先 MCP：

- `js_reverse`
- `chrome_devtools`
- `burp`

常见流程：

1. 搜源码
2. 对请求 URL 断点
3. 追调用链
4. 导出脚本
5. Burp 重放

### 18.6 文档检索 skill

优先 MCP：

- `context7`
- `fetch`

常见流程：

1. `resolve_library_id`
2. `query_docs`
3. 如需补充页面内容，再用 `fetch`

---

## 19. 写 skill 时可直接复用的提示词模板

下面给你几个适合直接改写进 skill 的模板。

### 19.1 Android 逆向 skill 模板片段

```text
当用户要求分析 Android APK 时：
1. 若任务是对已授权 Android App 做渗透测试，不要先静态分析 APK；先确认连接设备上是否已安装目标 App。
2. 先准备 burp 或 charles 的抓包可见性，再使用 scrcpy_vision 打开 App、驱动真实业务点击、输入和导航。
3. 每个关键动作后，先检查 burp 或 charles 是否已经出现 HTTP/HTTPS 或 WebSocket 数据包，并结合 adb_mcp 查看日志、界面异常和运行时状态。
4. 如果数据包已经可见且可重放，直接转入 Web/API/WebSocket 安全测试，按“界面动作 -> 数据包 -> Web 安全分析”的循环继续推进不同业务功能。
5. 只有在抓不到包、包被加密、明文不可得、协议仍不透明、无法稳定重放，或异常明显指向客户端逻辑阻塞时，才使用 jadx 读取 AndroidManifest.xml、主 Activity、导出组件，并搜索 okhttp/retrofit/sign/token/encrypt 等关键字。
6. 若 Java 层仍不够，使用 frida_mcp hook Java 或 native 边界恢复明文；若发现 native 线索（System.loadLibrary、JNI、so 文件）且 Java 与 hook 仍无法解决，再切换到 ida_pro_mcp 分析 dump 出来的 so。
7. 若需要控制设备、按 UI 元素定位、观察实时画面或切到 WiFi 调试，使用 scrcpy_vision；若需要安装应用、录屏、logcat、基础文件传输，使用 adb_mcp。
```

### 19.2 Web JS 逆向 skill 模板片段

```text
当用户要求定位前端签名、混淆函数或接口调用链时：
1. 优先使用 js_reverse 列举脚本并用 search_in_sources 搜索 sign/token/hash/encode/api path 等关键词。
2. 如果已知请求 URL，优先使用 break_on_xhr 或 get_request_initiator 确定发起位置。
3. 对关键函数使用 set_breakpoint_on_text、trace_function、get_paused_info、step 和 evaluate_script 获取运行时上下文。
4. 若需要保存完整脚本用于离线分析，使用 save_script_source。
5. 若需要复现或重放请求，配合 burp 的 create_repeater_tab、send_http1_request、send_http2_request。
6. 若需要页面级交互或截图，配合 chrome_devtools。
```

### 19.3 Native 二进制分析 skill 模板片段

```text
当用户要求分析二进制、so、恶意样本或 patch 点时：
1. 打开 IDA 后先调用 ida_pro_mcp.survey_binary 做总览，不要直接盲目 list_funcs。
2. 优先从 strings、imports、callgraph、关键常量、敏感 API 入手缩小范围。
3. 对可疑函数使用 analyze_function / decompile / xref_query / trace_data_flow。
4. 如果函数可读性差，使用 rename、set_type、declare_type、stack_frame、diff_before_after 逐步恢复语义。
5. 如需修改样本，使用 patch / patch_asm / put_int，并在必要时保存 IDB。
```

---

## 20. 常见注意事项汇总

### 20.1 绝对路径要求

以下类型工具经常要求绝对路径：

- `adb_mcp.take_screenshot`
- `adb_mcp.record_screen`
- `adb_mcp.pull_file` / `push_file`
- `scrcpy_vision.android_file_pull` / `android_file_push`
- `frida_mcp` 的 `script_file_path`、`output_file`
- `js_reverse.save_script_source`
- `chrome_devtools.take_screenshot`
- `chrome_devtools.take_memory_snapshot`
- `ida_pro_mcp.open_file`

### 20.2 分页类参数

常见分页/分片参数：

- `offset`
- `count`
- `limit`
- `pageIdx`
- `pageSize`
- `start_index`
- `length`

写 skill 时建议显式说明：

- 默认先取小批量样本
- 若结果过多，再增大 limit / count

### 20.3 先发现，再深入

很多 MCP 都有明显的“发现阶段工具”，不要一上来就深挖：

- `ida_pro_mcp`: `survey_binary`
- `jadx`: `get_android_manifest` / `search_classes_by_keyword`
- `js_reverse`: `list_scripts` / `search_in_sources`
- `chrome_devtools`: `take_snapshot`
- `charles`: `query_live_capture_entries`

### 20.4 证据留存

适合做证据保留的 MCP：

- `adb_mcp.take_screenshot`
- `adb_mcp.record_screen`
- `scrcpy_vision.android_vision_snapshot`
- `chrome_devtools.take_screenshot`
- `js_reverse.take_screenshot`
- `charles.get_traffic_entry_detail`
- `burp` 历史与 Repeater

### 20.5 最常见的组合

- Android 静态 + 动态：`jadx` + `frida_mcp`
- Android 动态 + 流量：`adb_mcp` + `charles`
- Android 动态 + UI 自动化：`scrcpy_vision` + `frida_mcp`
- Android 抓包 + 页面驱动：`scrcpy_vision` + `charles`
- Web 自动化 + JS 逆向：`chrome_devtools` + `js_reverse`
- Web 安全重放：`js_reverse` + `burp`
- Native 静态 + 动态：`ida_pro_mcp` + `frida_mcp`

---

## 21. 总结

如果你的目标是“方便后续写成 skills”，最实用的做法不是为每个 MCP 单独写一个 skill，而是按任务域拆：

- Android 静态分析
- Android 动态分析与抓包
- Web 自动化
- Web JS 逆向
- Native 二进制分析
- 文档检索
- 记忆与任务状态管理

其中最值得优先围绕其设计 skill 的 MCP 是：

1. `jadx`
2. `ida_pro_mcp`
3. `js_reverse`
4. `chrome_devtools`
5. `frida_mcp`
6. `charles`
7. `adb_mcp`

如果后面你要，我还可以在这份文档基础上继续帮你做两件事：

1. 再生成一份“适合 skills 的精简版 MCP 速查表”
2. 直接把这份文档拆成多个 `SKILL.md` 模板骨架
