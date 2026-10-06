"""Cross-endpoint and UI-contract regression checks."""
import json
from pathlib import Path
from ui import SECTIONS

def validate_ui(data, temples, index):
    root=Path(__file__).resolve().parents[2]
    config=json.loads((root/'travel/discovery.json').read_text(encoding='utf-8'))
    assert config==data['discovery']
    ids={t['id'] for t in temples}
    cards={t['id']:t['card'] for t in temples}
    for group in ['featured','popular']:
        selected=config[group]['temple_ids']
        assert selected and len(selected)==len(set(selected)) and set(selected)<=ids
    assert len(config['popular']['temple_ids'])==7
    assert {c['id'] for c in config['categories']} >= {'all','shiva','vishnu','krishna','hanuman','devi','ganesha','rama','jyotirlinga','shakti-peeth','char-dham'}
    for c in config['categories']:
        assert set(c['temple_ids'])<=ids
    for s in index['items']: assert s['card']==cards[s['id']]
    for t in temples:
        d=t['details']; u=d['ui']; sources={s['id'] for s in d['sources']}
        assert u['section_order']==[k for k,_ in SECTIONS]
        assert all(k in u for k,_ in SECTIONS)
        assert u['gallery']['items']==d['media']['items']
        assert u['darshan']['hours']==d['visiting']['hours']
        assert u['actions']['save']['storage_key']==t['id']
        for group in ['nearby','related']:
            seen=set()
            for r in u[group]['items']:
                assert r['temple_id'] in ids and r['temple_id']!=t['id'] and r['temple_id'] not in seen
                seen.add(r['temple_id']); assert r['card']==cards[r['temple_id']]
                if group=='nearby': assert r['distance_km'] is None or r['distance_km']>=0
        def check_refs(obj):
            if isinstance(obj,dict):
                if obj.get('source_id'): assert obj['source_id'] in sources
                if 'source_ids' in obj: assert set(obj['source_ids'])<=sources
                for v in obj.values(): check_refs(v)
            elif isinstance(obj,list):
                for v in obj: check_refs(v)
        check_refs(u)
        for row in u['darshan']['schedule']: assert row['opens']<row['closes']
    k=next(t for t in temples if t['name']=='Shri Kashi Vishwanath Temple')['details']['ui']
    assert k['name_hi'] and len(k['darshan']['schedule'])==7 and len(k['history']['items'])==2
    assert len(k['how_to_reach']['items'])==3 and len(k['rituals']['items'])==2
    print('PASS: eight-screen UI contract, cards, filters, source references, recommendations and Kashi content.')
