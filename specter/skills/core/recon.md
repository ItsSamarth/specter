---
name: recon
description: Information gathering workflow — passive + active reconnaissance
---

# Information Gathering Skill

Perform passive and active information gathering to build a target profile and attack surface map.

## Execution Steps

### 1. Passive Reconnaissance
- Access the target via the fetch tool and collect HTTP response headers
- Identify server type, version, and WAF
- Analyze technology stack indicators in the HTML source

### 2. Active Reconnaissance
- Probe common Web ports
- Enumerate directories and paths
- Check sensitive files (robots.txt, .env, .git)
- Discover API endpoints

### 3. Technology Stack Identification
- Frontend frameworks (React/Vue/Angular/jQuery)
- Backend frameworks (Express/Django/Flask/Spring)
- CMS systems (WordPress/Joomla/custom)
- Database types

### 4. Output
- Target profile (IP/domain/ports/services/technology stack)
- Attack surface map (accessible paths, APIs, admin entry points)
