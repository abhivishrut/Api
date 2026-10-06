"""Validate the published catalogue and static endpoints without network access."""
import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
from research import rows


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def check_schema(value, rule, root_schema, path='$'):
    """Dependency-free validation of the keywords used in travel.schema.json.

    This is deliberately not a general-purpose JSON Schema implementation.
    External consumers can use any Draft 2020-12 validator with the schema.
    """
    if '$ref' in rule:
        target=root_schema
        for segment in rule['$ref'][2:].split('/'): target=target[segment]
        check_schema(value,target,root_schema,path)
        return
    kinds={'object':lambda x:isinstance(x,dict), 'array':lambda x:isinstance(x,list),
           'string':lambda x:isinstance(x,str), 'null':lambda x:x is None,
           'boolean':lambda x:type(x) is bool, 'integer':lambda x:type(x) is int,
           'number':lambda x:type(x) in (int,float)}
    if 'type' in rule:
        expected=rule['type'] if isinstance(rule['type'],list) else [rule['type']]
        assert any(kinds[k](value) for k in expected), f'{path}: expected {expected}'
    if 'const' in rule: assert value == rule['const'], f'{path}: const mismatch'
    if 'enum' in rule: assert value in rule['enum'], f'{path}: enum mismatch'
    if isinstance(value,dict):
        assert set(rule.get('required',[])) <= set(value), f'{path}: missing fields {set(rule.get("required",[]))-set(value)}'
        properties=rule.get('properties',{})
        for key,child in value.items():
            if key in properties: check_schema(child,properties[key],root_schema,path+'.'+key)
            elif rule.get('additionalProperties') is False: raise AssertionError(f'{path}.{key}: unexpected')
            elif isinstance(rule.get('additionalProperties'),dict): check_schema(child,rule['additionalProperties'],root_schema,path+'.'+key)
    if isinstance(value,list):
        if rule.get('uniqueItems'): assert len({json.dumps(x,sort_keys=True) for x in value}) == len(value), f'{path}: duplicates'
        if 'items' in rule:
            for i,item in enumerate(value): check_schema(item,rule['items'],root_schema,f'{path}[{i}]')
    if isinstance(value,str) and 'minLength' in rule: assert len(value)>=rule['minLength'], f'{path}: too short'
    if type(value) in (int,float):
        if 'minimum' in rule: assert value>=rule['minimum'], f'{path}: below minimum'
        if 'maximum' in rule: assert value<=rule['maximum'], f'{path}: above maximum'


def validate():
    data = read(ROOT / 'travel.json')
    schema = read(ROOT / 'travel.schema.json')
    check_schema(data,schema,schema)
    references = read(ROOT / 'tools/travel/references.json')
    for row in rows():
        reference_state = references.get(row[1], {}).get('infobox', {}).get('State')
        if row[2] == 'IN' and reference_state:
            assert row[3].lower() in reference_state.lower().replace('&', 'and'), f'Reference state mismatch: {row[0]} / {reference_state}'
    assert data['schema_version'] == '2.1.0'
    all_temples = [t for state in data['states'] for t in state['temples']] + data['international_temples']
    ids = [t['id'] for t in all_temples]
    assert len(ids) == len(set(ids)), 'Duplicate temple IDs'
    by_id = {t['id']: t for t in all_temples}
    deity_ids = {d['id'] for d in data['deities']}
    country_ids = {c['country_code'] for c in data['countries']}
    collection_ids = {c['id'] for c in data['collections']}
    assert len(country_ids) == len(data['countries'])
    stats = data['metadata']['statistics']
    assert stats['temples'] == len(ids)
    assert stats['india_temples'] == sum(t['country_code'] == 'IN' for t in all_temples)
    assert stats['international_temples'] == len(data['international_temples'])
    assert stats['countries'] == len(country_ids)
    assert stats['india_states_and_uts'] == len(data['states'])
    assert stats['with_reference_coordinates'] == sum(t['details']['location']['latitude'] is not None for t in all_temples)
    assert stats['with_attributed_photos'] == sum(bool(t['thumbnail']) for t in all_temples)
    assert stats['with_primary_sources'] == sum(any(s['id'] == 'primary' for s in t['details']['sources']) for t in all_temples)
    for state in data['states']:
        assert state['country_code'] == 'IN'
        assert state['temple_count'] == len(state['temples']) > 0
        assert all(t['country_code'] == 'IN' and t['state_name'] == state['state_name'] for t in state['temples'])
    assert all(t['country_code'] != 'IN' for t in data['international_temples'])
    assigned=[]
    for country in data['countries']:
        member_ids=[i for region in country['regions'] for i in region['temple_ids']]
        assert len(member_ids) == country['temple_count']
        assert all(by_id[i]['country_code'] == country['country_code'] for i in member_ids)
        assigned.extend(member_ids)
    assert Counter(assigned) == Counter(ids), 'Country index missing or duplicating temples'
    for collection in data['collections']:
        assert len(collection['temple_ids']) == collection['expected_count'], collection['id']
        assert set(collection['temple_ids']) == {t['id'] for t in all_temples if collection['id'] in t['details']['collection_ids']}
    for deity in data['deities']:
        assert deity['temple_count'] == sum(deity['id'] in t['details']['deity_ids'] for t in all_temples)
    for required in ['shiva','rama','vishnu','krishna','hanuman','ganesha','devi']:
        assert any(required in t['details']['deity_ids'] for t in all_temples), required
    bounding_boxes = {'IN':(6,38,68,98),'NP':(26,31,80,89),'LK':(5,10,79,82),'MY':(0,8,99,120),
                      'SG':(1,2,103,105),'ID':(-12,7,94,142),'TH':(5,21,97,106),'BD':(20,27,88,93),
                      'PK':(23,38,60,78),'MU':(-21,-19,56,59),'AE':(22,27,51,57),'GB':(49,61,-9,3),
                      'US':(24,50,-125,-66),'CA':(41,84,-141,-52),'AU':(-44,-10,112,154),
                      'FJ':(-21,-12,176,180),'ZA':(-35,-22,16,33),'TT':(10,12,-62,-60)}
    for t in all_temples:
        d=t['details']
        assert t['name'] == d['name']
        assert t['thumbnail'] == d['thumbnail']
        assert t['country_code'] in country_ids
        assert set(d['deity_ids']) <= deity_ids
        assert set(d['collection_ids']) <= collection_ids
        assert d['sources'], f'Missing sources: {t["name"]}'
        assert d['description'] and '\\n' not in d['description'] and not d['highlights'][0].startswith('+')
        assert len(d['description']) > 60
        assert d['data_quality']['google_maps_listing_verified'] is False
        loc=d['location']
        lat,lon=loc['latitude'],loc['longitude']
        assert (lat is None) == (lon is None)
        if lat is not None:
            assert isinstance(lat,(int,float)) and isinstance(lon,(int,float))
            assert math.isfinite(lat) and math.isfinite(lon) and -90<=lat<=90 and -180<=lon<=180
            a,b,c,e=bounding_boxes[t['country_code']]
            assert a<=lat<=b and c<=lon<=e, f'Coordinates outside country: {t["name"]} {lat},{lon}'
            assert loc['coordinate_source_id'] == 'reference'
        for key, query_key in [('google_maps_url','query'),('directions_url','destination')]:
            url=urlparse(loc[key]); params=parse_qs(url.query)
            assert url.scheme == 'https' and url.hostname == 'www.google.com'
            assert params['api'] == ['1'] and t['name'] in params[query_key][0]
            assert loc['country'] in params[query_key][0]
        for source in d['sources']:
            assert urlparse(source['url']).scheme == 'https'
        for value in d['facilities'].values():
            assert value is None or type(value) is bool
        for item in d['media']['items']:
            assert all(item.get(k) for k in ['url','source_page','author','license','license_url','alt'])
            assert item['license'].startswith(('CC BY ', 'CC BY-SA '))
            assert urlparse(item['license_url']).hostname == 'creativecommons.org'
            assert urlparse(item['url']).hostname.endswith('.wikimedia.org')
        assert bool(t['thumbnail']) == bool(d['media']['items'])
        assert d['gallery'] == [m['url'] for m in d['media']['items']]
        assert (ROOT / d['media']['fallback_asset']).is_file()
        for day in d['visiting']['hours']:
            for session in day['sessions']:
                assert session['opens'] < session['closes']
        detail=read(ROOT / f'travel/temples/{t["id"]}.json')
        assert detail['temple'] == t, 'Stale detail endpoint'
    index=read(ROOT/'travel/index.json')
    assert Counter(x['id'] for x in index['items']) == Counter(ids)
    assert index['countries'] == data['countries'] and index['collections'] == data['collections']
    # Build order can differ from state-sorted main payload; use ID equality below.
    pages=[]; path='travel/pages/001.json'; previous=None; visited=set()
    while path:
        assert path not in visited, 'Pagination cycle'
        visited.add(path)
        page=read(ROOT/path)
        assert page['previous'] == previous
        assert page['page'] == len(visited)
        assert page['total_items'] == len(ids)
        assert len(page['items']) <= page['page_size'] == 24
        pages.extend(page['items'])
        previous,path=path,page['next']
    assert Counter(x['id'] for x in pages) == Counter(ids)
    assert pages == index['items']
    assert len(visited) == math.ceil(len(ids)/24)
    for summary in pages:
        assert (ROOT/summary['detail_path']).is_file()
    from validate_ui import validate_ui
    validate_ui(data, all_temples, index)
    migration=read(ROOT/'tools/travel/migration.json')
    original=gzip.decompress((ROOT/'tools/travel/legacy.travel.json.gz').read_bytes())
    assert hashlib.sha256(original).hexdigest() == migration['original_sha256']
    old=json.loads(original.decode('utf-8-sig'))
    assert sum(len(s['temples']) for s in old['states']) == migration['original_record_count'] == len(migration['records'])
    assert all(r['temple_id'] is None or r['temple_id'] in by_id for r in migration['records'])
    assert len(set(r['legacy_pointer'] for r in migration['records'])) == migration['original_record_count']
    print(f'PASS: {len(ids)} temples; {len(country_ids)} countries; {len(data["collections"])} complete collections; {len(visited)} pages; archive integrity and endpoint consistency.')


if __name__ == '__main__': validate()
