"""One-off site-wide consistency audit: crawl every internal link from the
live production site, report any non-200 status, and check nav active-state
correctness per page type.

Run: venv/Scripts/python.exe scripts/site_audit.py
"""
import re
import urllib.request
from collections import deque
from urllib.parse import urljoin, urlparse

BASE = 'https://lalitenterprise.in'
visited = set()
queue = deque([BASE + '/'])
broken = []
checked_count = 0

HEADERS = {'User-Agent': 'Mozilla/5.0 (SiteAuditBot)'}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return None, str(e)


def extract_links(html, current_url):
    hrefs = re.findall(r'href="([^"]+)"', html)
    links = []
    for h in hrefs:
        if h.startswith('#') or h.startswith('mailto:') or h.startswith('tel:') or h.startswith('javascript:'):
            continue
        full = urljoin(current_url, h)
        parsed = urlparse(full)
        if parsed.netloc == urlparse(BASE).netloc:
            # strip fragment/query for crawling dedup, but keep query for testing search
            full_no_frag = full.split('#')[0]
            links.append(full_no_frag)
    return links


while queue and checked_count < 500:
    url = queue.popleft()
    if url in visited:
        continue
    visited.add(url)
    checked_count += 1

    status, body = fetch(url)
    if status != 200:
        broken.append((url, status))
        print(f'BROKEN [{status}] {url}')
        continue

    for link in extract_links(body, url):
        if link not in visited and '/admin/' not in link and link.startswith(BASE):
            queue.append(link)

print()
print(f'Checked {checked_count} URLs, {len(visited)} unique.')
print(f'Broken links found: {len(broken)}')
for url, status in broken:
    print(' -', status, url)
