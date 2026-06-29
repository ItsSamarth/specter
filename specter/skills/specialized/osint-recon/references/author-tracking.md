# Author Tracking Methods

## Core Flow

```
Extract author identifier from page → Determine unique identifier (username/email) → Cross-platform search → Consolidate info
```

## Step 1: Extract Author Identifier from Page

### HTML Meta Tags
```python
import re

def extract_author_from_meta(html):
    """Extract author information from HTML meta tags"""
    authors = []
    
    # <meta name="author" content="XXX">
    m = re.findall(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', html)
    authors.extend(m)
    
    # <meta name="copyright" content="XXX">
    m = re.findall(r'<meta\s+name=["\']copyright["\']\s+content=["\']([^"\']+)["\']', html)
    authors.extend(m)
    
    # OG tags
    m = re.findall(r'<meta\s+property=["\']article:author["\']\s+content=["\']([^"\']+)["\']', html)
    authors.extend(m)
    
    return list(set(authors))
```

### Page Link Extraction
```python
def extract_social_links(html):
    """Extract social media links from a page"""
    links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
    
    social = {}
    for link in links:
        if 'github.com' in link:
            social['github'] = link
        elif 'bilibili.com' in link:
            social['bilibili'] = link
        elif 'weibo.com' in link or 'weibo.cn' in link:
            social['weibo'] = link
        elif 'zhihu.com' in link:
            social['zhihu'] = link
        elif 'twitter.com' in link or 'x.com' in link:
            social['twitter'] = link
        elif 'linkedin.com' in link:
            social['linkedin'] = link
        elif 'youtube.com' in link:
            social['youtube'] = link
        elif 'facebook.com' in link:
            social['facebook'] = link
    
    return social
```

## Step 2: GitHub Tracking

### User Info API
```python
import requests

def get_github_profile(username):
    """Retrieve public GitHub user information"""
    r = requests.get(f"https://api.github.com/users/{username}")
    if r.status_code != 200:
        return None
    
    data = r.json()
    return {
        'name': data.get('name'),
        'bio': data.get('bio'),
        'email': data.get('email'),
        'blog': data.get('blog'),
        'location': data.get('location'),
        'company': data.get('company'),
        'public_repos': data.get('public_repos'),
        'followers': data.get('followers'),
        'following': data.get('following'),
        'created_at': data.get('created_at'),
        'avatar_url': data.get('avatar_url'),
    }

def get_github_repos(username):
    """Get user's public repos (infer tech stack)"""
    r = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100")
    if r.status_code != 200:
        return []
    
    repos = r.json()
    languages = {}
    for repo in repos:
        lang = repo.get('language')
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    return {
        'top_languages': sorted(languages.items(), key=lambda x: -x[1])[:5],
        'repo_count': len(repos),
        'starred_total': sum(r.get('stargazers_count', 0) for r in repos),
    }
```

### Extract Email from GitHub Commit History
```python
def get_github_commit_email(username, repo):
    """Extract author email from GitHub commit history"""
    r = requests.get(f"https://api.github.com/repos/{username}/{repo}/commits?per_page=10")
    if r.status_code != 200:
        return []
    
    emails = set()
    for commit in r.json():
        author = commit.get('commit', {}).get('author', {})
        if author.get('email'):
            emails.add(author['email'])
    
    return list(emails)
```

## Step 3: Cross-Platform Correlation

### Search Other Platforms by Username
```python
# Common platform checks
PLATFORMS = {
    'GitHub': 'https://github.com/{username}',
    'Bilibili': 'https://space.bilibili.com/search?keyword={username}',
    'Zhihu': 'https://www.zhihu.com/search?type=content&q={username}',
    'CSDN': 'https://blog.csdn.net/{username}',
    'Juejin': 'https://juejin.cn/user/{username}',
    'Twitter': 'https://twitter.com/{username}',
    'LinkedIn': 'https://www.linkedin.com/in/{username}',
}

async def cross_platform_search(username, fetch_tool):
    """Search multiple platforms by username"""
    results = {}
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)
        try:
            resp = await fetch_tool(url=url)
            if resp.get('status') == 200:
                results[platform] = f"✅ Found ({url})"
            else:
                results[platform] = f"❌ Not found"
        except:
            results[platform] = f"⚠️ Detection failed"
    return results
```

## Step 4: Information Summary Template

```markdown
## Personal Profile: {Nickname}

### Basic Information
- **Nickname**: xxx
- **Real Name**: xxx (if available)
- **Email**: xxx
- **Location**: xxx
- **Occupation/Company**: xxx

### Technical Profile
- **Primary Languages**: Python / JavaScript / ...
- **Tech Stack Preferences**: ...
- **Open Source Contributions**: N repos, M stars
- **Areas of Interest**: ...

### Social Media
- GitHub: xxx
- Bilibili: xxx
- Zhihu: xxx
- ...

### Associated Information
- Same ID across platforms: xxx
- Known projects: xxx
- Historical leaks: xxx
```
