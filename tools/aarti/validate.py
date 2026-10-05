"""Validate API structure and known completeness anchors; no dependencies.

Run: python tools/aarti/validate.py
These checks do not replace literary proofreading against a printed edition.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from transliterate import romanize

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_VERSES = {3:17,6:9,20:31,21:21,22:9,23:33,33:8,34:9,
    38:8,46:12,47:38,60:11,61:8,71:21,73:6,74:6,79:8,
    80:9,81:6,82:8,83:9,84:8,85:9,86:7,87:9,90:9,93:8,94:8,95:5,
    103:8,104:7,105:9}
REQUIRED = {'id','name','god_name','language','category','lyrics','audio_url','image_url','duration'}
DIGITS = str.maketrans('०१२३४५६७८९', '0123456789')

def validate():
    data=json.loads((ROOT/'aarti.json').read_text(encoding='utf-8'))
    items=data['Aarti']
    assert data['meta']['total_aartis']==len(items), 'Stale metadata count'
    assert len(items)==105, 'Expected the reviewed 85 entries plus 20 additions'
    ids=[x['id'] for x in items]
    assert len(ids)==len(set(ids)), 'Duplicate IDs'
    assert len({x['name'].casefold() for x in items})==len(items), 'Duplicate names'
    assert not {9,45,77,89}.intersection(ids), 'Retired filler IDs returned'
    assert set(range(92,97)).issubset(ids), 'Missing new entries'
    expected_ids=set(range(1,117))-{9,31,32,45,53,54,57,58,59,77,89}
    assert set(ids)==expected_ids, 'Missing, reused, or unexpected catalog IDs'
    assert set(range(97,117)).issubset(ids), 'Missing expansion entries'
    normalized_lyrics=[re.sub(r'\s+', '',x['lyrics']['hindi']) for x in items]
    assert len(normalized_lyrics)==len(set(normalized_lyrics)), 'Duplicate complete texts'
    by_id={x['id']:x for x in items}
    for x in items:
        ident=x['id']
        assert REQUIRED==set(x), f'{ident}: changed API fields'
        assert isinstance(ident,int) and ident>0
        for key in ('name','god_name','language','category'):
            assert isinstance(x[key],str) and x[key].strip(), (ident,key)
        assert set(x['lyrics'])=={'hindi','english'}
        hi,en=x['lyrics']['hindi'],x['lyrics']['english']
        assert hi.strip() and en.strip(), f'{ident}: missing lyrics'
        assert re.search('[\u0900-\u097f]',hi)
        assert not re.search('[\u0900-\u097f]',en), f'{ident}: unconverted Roman lyrics'
        assert en==romanize(hi), f'{ident}: scripts no longer match'
        assert not re.search(r'undefined|\ufffd|L\d+:|\[Button|https?://|x2|\.\.\.',hi), f'{ident}: source debris'
        assert hi.count('(')==hi.count(')'), f'{ident}: unbalanced alternative reading'
        for key in ('image_url','audio_url'):
            assert isinstance(x[key],str)
            if x[key]:
                parsed=urlparse(x[key])
                assert parsed.scheme=='https' and parsed.netloc, (ident,key)
        assert isinstance(x['duration'],str)
        assert not x['duration'] or re.fullmatch(r'\d+:[0-5]\d',x['duration'])
        if ident in EXPECTED_VERSES:
            numbers={int(n.translate(DIGITS)) for n in re.findall(r'॥\s*([०-९0-9]+)\s*॥',hi)}
            required=set(range(1,EXPECTED_VERSES[ident]+1))
            assert required.issubset(numbers), f'{ident}: missing verses {required-numbers}'
    text=re.sub(r'\s+', '', by_id[19]['lyrics']['hindi'])
    names=text.split('॥नामस्तोत्रम्॥',1)[1].split('सर्वप्रहरणायुधॐनमइति',1)[0]
    numbers=[int(n.translate(DIGITS)) for n in re.findall(r'॥\s*([०-९0-9]+)\s*॥',names)]
    assert numbers==list(range(1,108)), 'Vishnu Sahasranamam name-stanza sequence'
    assert len(re.findall('त्वदीयपादपङ्कजं',by_id[87]['lyrics']['hindi']))==8
    assert len(re.findall('गतिस्त्वं गतिस्त्वं',by_id[84]['lyrics']['hindi']))==8
    assert len(re.findall('मधुराधिपतेरखिलं',by_id[61]['lyrics']['hindi']))==8
    assert len(re.findall('जय जय हे महिषासुर',by_id[71]['lyrics']['hindi']))==21
    assert 'पातु रामोऽखिलं वपुः' in by_id[47]['lyrics']['hindi']
    krishna=by_id[107]['lyrics']['hindi'].split('॥ चौपाई ॥',1)[1].split('॥ दोहा ॥',1)[0]
    assert krishna.count('॥')==40, 'Krishna Chalisa: expected 40 chaupai couplets'
    assert 'नयन कमल अभिराम' in by_id[107]['lyrics']['hindi']
    assert 'रवि तनय' not in by_id[107]['lyrics']['hindi'], 'Mixed Shani invocation'
    bajrang=by_id[102]['lyrics']['hindi'].split('॥ चौपाई ॥',1)[1].split('॥ दोहा ॥',1)[0]
    assert bajrang.count('॥')==35, 'Bajrang Baan: expected 35 chaupai couplets'
    assert by_id[100]['language']=='Marathi'
    assert by_id[100]['lyrics']['hindi'].count('जय देव जय देव')==3
    for ident in range(97,117):
        assert by_id[ident]['audio_url']=='' and by_id[ident]['duration']==''
    ram=by_id[40]['lyrics']['hindi']
    for word in ('ईश्वर','अल्लाह','रहीम','करीम','सन्मति'):
        assert word not in ram
    for line in ('सुन्दर विग्रह मेघश्याम','भद्रगिरीश्वर सीता राम','जानकीरमण सीता राम'):
        assert line in ram
    assert romanize('वक्रतुण्ड')=='vakratuṇḍa'
    assert romanize('त्र्यम्बकं')=='tryambakaṃ'
    assert romanize('मृत्योर्मुक्षीय')=='mṛtyormukṣīya'
    assert romanize('नमोऽस्तु')=="namo'stu"
    print(f'PASS: {len(items)} entries; unique IDs/names; schema, bilingual parity, source debris, verse sequences, and prayer anchors.')

if __name__=='__main__':
    validate()
