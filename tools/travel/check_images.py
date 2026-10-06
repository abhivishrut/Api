"""Check thumbnail HTTP responses without downloading image bodies."""
import concurrent.futures
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE=Path(__file__).resolve().parent


def check(url):
    result={'checked_at':datetime.now(timezone.utc).isoformat(), 'reachable':False}
    try:
        request=urllib.request.Request(url,method='HEAD',headers={'User-Agent':'TempleCatalogueResearch/1.0 (image link verification)'})
        with urllib.request.urlopen(request,timeout=20) as response:
            result.update(http_status=response.status,content_type=response.headers.get('Content-Type'),resolved_url=response.url)
            result['reachable']=response.status == 200 and response.headers.get('Content-Type','').startswith('image/')
    except Exception as error:
        result['error']=str(error)
    return url,result


def main():
    references=json.loads((BASE/'references.json').read_text(encoding='utf-8'))
    urls=sorted({r['photo']['url'] for r in references.values() if r.get('photo')})
    results={}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for i,(url,result) in enumerate(pool.map(check,urls),1):
            results[url]=result
            if i%25==0: print(f'Checked {i}/{len(urls)} image links',flush=True)
    (BASE/'image_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'checked':len(results),'reachable':sum(x['reachable'] for x in results.values())}))


if __name__=='__main__': main()
