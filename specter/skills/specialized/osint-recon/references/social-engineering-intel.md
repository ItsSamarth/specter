# Social Engineering Intelligence Summary

## Persona Profiling Framework

### Information Dimensions

| Dimension | Data Source | Extraction Method |
|------|--------|---------|
| Identity markers | Page meta, GitHub | Regex extract author/copyright |
| Social networks | Page external links | `<a href>` matching social media domains |
| Technology preferences | GitHub repository language distribution | GitHub API |
| Geographic location | GitHub location, blog | Profile page |
| Professional information | GitHub company, LinkedIn | Profile page |
| Contact information | GitHub email, blog contact page | API + page extraction |
| Areas of interest | GitHub repository topics, blog articles | Repository topics + article categories |

## Information Cross-Verification

### Principles
1. **Do not trust a single source** — key information requires confirmation from at least 2 independent sources
2. **Timeliness annotation** — annotate the time information was obtained; flag outdated information separately
3. **Confidence rating**:
   - 🟢 **High**: confirmed by multiple independent sources
   - 🟡 **Medium**: single reliable source
   - 🔴 **Low**: inferred/unverified

### Common Correlation Patterns

```
Blog GitHub link → GitHub username → GitHub API to obtain email
                                  → GitHub API to obtain repositories → infer tech stack
                                  → GitHub commit email → correlate other identities

Blog Bilibili link → Bilibili UID → Bilibili homepage → following/followers → interest tags
                                    → uploaded videos → technical domain

Username → cross-platform search → discover more social accounts
Email → haveibeenpwned → data breach records
```

## Social Media Information Extraction

### Bilibili
```python
import re

def extract_bilibili_uid(url):
    """Extract UID from a Bilibili URL"""
    # space.bilibili.com/12345
    m = re.search(r'bilibili\.com/(\d+)', url)
    if m:
        return m.group(1)
    return None
```

### Weibo
```python
def extract_weibo_uid(url):
    """Extract UID from a Weibo URL"""
    # weibo.com/u/12345 or weibo.com/username
    m = re.search(r'weibo\.com/(?:u/)?(\w+)', url)
    if m:
        return m.group(1)
    return None
```

### Zhihu
```python
def extract_zhihu_username(url):
    """Extract username from a Zhihu URL"""
    # zhihu.com/people/username
    m = re.search(r'zhihu\.com/people/([^/?]+)', url)
    if m:
        return m.group(1)
    return None
```

## Information Summary Report Format

```markdown
# Target Reconnaissance Report

## 📋 Basic Information
| Item | Content | Confidence | Source |
|------|------|--------|------|
| Target | https://xxx | - | User input |
| Framework | Hexo | 🟢 | HTTP headers + HTML features |
| Server | GitHub Pages | 🟢 | Server header |
| Author | XXX | 🟢 | meta author |
| ... | ... | ... | ... |

## 👤 Persona Profile
- **Nickname**: XXX
- **GitHub**: https://github.com/xxx
- **Bilibili**: https://space.bilibili.com/xxx
- **Tech stack**: Python / JavaScript
- **Location**: Shenzhen
- ...

## 🔗 Correlation Findings
- [Finding 1]
- [Finding 2]

## 📌 Key Findings
1. ...
2. ...

---
*Report generated at: YYYY-MM-DD HH:MM*
*Data sources: target website, GitHub API, public social media information*
```

## Privacy and Ethics

- ✅ Only collect **public information** (content accessible without login)
- ✅ Do not attempt to log into others' accounts
- ✅ Do not use collected information for harassment or social engineering attacks
- ✅ Annotate information sources to ensure traceability
- ❌ Do not collect private communication content
- ❌ Do not use information for phishing or other deceptive behavior
