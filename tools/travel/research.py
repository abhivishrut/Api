"""Retrieve public reference pages; never scrape Google reviews or ratings.

Run explicitly when refreshing sources. Failed pages remain failed, not verified.
The fetch date records retrieval, not factual review of every field.
"""
import concurrent.futures
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
AGENT = {'User-Agent': 'TempleCatalogueResearch/1.0 (public reference verification)'}


def clean(value):
    value = re.sub(r'<(?:script|style)\b.*?</(?:script|style)>', '', value, flags=re.S)
    value = re.sub(r'<br\s*/?>', ', ', value)
    return re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', value))).strip()


def photo_metadata(content):
    """Only publish CC BY/CC BY-SA images with an explicit file-page author."""
    block = re.search(r'class="infobox-image"[^>]*>(.*?)</td>', content, re.S)
    if not block:
        return None
    link = re.search(r'href="([^"]*(?:/wiki/|\./)File:[^"]+)"', block.group(1))
    thumb = re.search(r'<img[^>]+src="([^"]+)"', block.group(1))
    if not link or not thumb:
        return None
    filename = html.unescape(link.group(1)).split('File:', 1)[1]
    file_url = 'https://commons.wikimedia.org/wiki/File:' + filename
    try:
        with urllib.request.urlopen(urllib.request.Request(file_url, headers=AGENT), timeout=25) as response:
            page = html.unescape(response.read().decode('utf-8'))
        licensing = re.search(r'licensed under.{0,1800}?href="((?:https?:)?//creativecommons.org/licenses/(by(?:-sa)?)/([\d.]+)/[^\"]*)"', page, re.S | re.I)
        author_row = re.search(r'<td[^>]*id="fileinfotpl_aut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>', page, re.S)
        if not licensing or not author_row:
            return None
        author = clean(author_row.group(1))
        if not author or len(author) > 250:
            return None
        thumb_url = html.unescape(thumb.group(1)).split('?', 1)[0]
        if thumb_url.startswith('//'):
            thumb_url = 'https:' + thumb_url
        if not urllib.parse.urlparse(thumb_url).hostname.endswith('.wikimedia.org'):
            return None
        return {'url': thumb_url, 'source_page': file_url, 'author': author,
                'license': 'CC ' + licensing.group(2).upper() + ' ' + licensing.group(3),
                'license_url': ('https:' if licensing.group(1).startswith('//') else '') + licensing.group(1), 'changes': 'None; Wikimedia thumbnail rendition.',
                'verification': 'license_and_article_association_checked; visual_identity_not_reviewed'}
    except (urllib.error.URLError, TimeoutError, ValueError):
        return None


def rows():
    for line in (BASE / 'catalogue.tsv').read_text(encoding='utf-8').splitlines():
        if line and not line.startswith('#'):
            values = line.split('|')
            if len(values) != 8:
                raise ValueError(f'Expected eight fields: {line}')
            yield values


def fetch(row):
    title = row[1]
    url = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_'), safe='(),')
    result = {'url': url, 'retrieved_at': datetime.now(timezone.utc).isoformat(),
              'status': 'unavailable', 'latitude': None, 'longitude': None}
    try:
        req = urllib.request.Request(url, headers=AGENT)
        with urllib.request.urlopen(req, timeout=35) as response:
            content = response.read().decode('utf-8')
            result['resolved_url'] = response.url
            result['http_status'] = response.status
        page_title = re.search(r'<title>(.*?)</title>', content, re.S)
        result['page_title'] = html.unescape(page_title.group(1)) if page_title else None
        result['infobox'] = {}
        for block in re.findall(r'<tr\b[^>]*>(.*?)</tr>', content, re.S):
            label = re.search(r'<th\b[^>]*>(.*?)</th>', block, re.S)
            value = re.search(r'<td\b[^>]*>(.*?)</td>', block, re.S)
            if label and value:
                key = clean(label.group(1))
                if key in ('District', 'State', 'Province', 'Country', 'Deity', 'Festivals', 'Architecture', 'Style'):
                    result['infobox'][key] = clean(value.group(1))[:250]
        result['photo'] = photo_metadata(content)
        result['metadata_version'] = 3
        lat = re.search(r'class="latitude"[^>]*>(.*?)</span>', content, re.S)
        lon = re.search(r'class="longitude"[^>]*>(.*?)</span>', content, re.S)
        def decimal(raw):
            value = html.unescape(re.sub('<[^>]+>', '', raw))
            nums = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', value)]
            number = nums[0] + (nums[1] / 60 if len(nums) > 1 else 0) + (nums[2] / 3600 if len(nums) > 2 else 0)
            return round(number * (-1 if re.search('[SW]', value) else 1), 6)
        if lat and lon:
            result['latitude'], result['longitude'] = decimal(lat.group(1)), decimal(lon.group(1))
        else:
            geo = re.search(r'class="geo"[^>]*>\s*([-\d.]+)\s*;\s*([-\d.]+)', content)
            if geo:
                result['latitude'], result['longitude'] = map(float, geo.groups())
        result['status'] = 'reference_retrieved'
        if 'disambiguation' in (result['page_title'] or '').lower() or 'This disambiguation page lists' in clean(content):
            result['status'] = 'identity_needs_review'
            result['latitude'] = result['longitude'] = None
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        result['error'] = str(exc)
    return title, result


def main():
    path = BASE / 'references.json'
    data = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    todo = [r for r in rows() if data.get(r[1], {}).get('status') != 'reference_retrieved' or data.get(r[1], {}).get('metadata_version') != 3]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for i, (key, result) in enumerate(pool.map(fetch, todo), 1):
            data[key] = result
            if result['status'] != 'reference_retrieved':
                print(f'{result["status"]}: {key}', flush=True)
            if i % 20 == 0:
                path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                print(f'Retrieved {i}/{len(todo)} reference pages', flush=True)
            time.sleep(0.05)
    active_titles = {r[1] for r in rows()}
    data = {key: value for key, value in data.items() if key in active_titles}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'total': len(data), 'retrieved': sum(x['status'] == 'reference_retrieved' for x in data.values()),
                      'with_coordinates': sum(x['latitude'] is not None for x in data.values())}))


if __name__ == '__main__':
    main()
