"""Build the versioned static temple API from editorial data and saved research.

Network-free and deterministic. Source refresh is a separate explicit operation.
"""
import gzip
import hashlib
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlencode

from research import rows

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
DATE = '2026-10-06'
COUNTRIES = {
    'IN': ('India', 'Asia/Kolkata'), 'NP': ('Nepal', 'Asia/Kathmandu'),
    'LK': ('Sri Lanka', 'Asia/Colombo'), 'MY': ('Malaysia', 'Asia/Kuala_Lumpur'),
    'SG': ('Singapore', 'Asia/Singapore'), 'ID': ('Indonesia', None),
    'TH': ('Thailand', 'Asia/Bangkok'), 'BD': ('Bangladesh', 'Asia/Dhaka'),
    'PK': ('Pakistan', 'Asia/Karachi'), 'MU': ('Mauritius', 'Indian/Mauritius'),
    'AE': ('United Arab Emirates', 'Asia/Dubai'), 'GB': ('United Kingdom', 'Europe/London'),
    'US': ('United States', None), 'CA': ('Canada', 'America/Toronto'),
    'AU': ('Australia', None), 'FJ': ('Fiji', 'Pacific/Fiji'),
    'ZA': ('South Africa', 'Africa/Johannesburg'), 'TT': ('Trinidad and Tobago', 'America/Port_of_Spain')
}
DEITIES = {
    'shiva': ('Shiva', 'शिव', ['Shiv', 'Mahadev', 'Shankar', 'Bholenath']),
    'rama': ('Rama', 'राम', ['Ram', 'Raghunath', 'Ram Lalla']),
    'vishnu': ('Vishnu', 'विष्णु', ['Narayan', 'Narayana', 'Venkateswara', 'Balaji', 'Perumal']),
    'krishna': ('Krishna', 'कृष्ण', ['Kanha', 'Govind', 'Gopal', 'Shyam']),
    'hanuman': ('Hanuman', 'हनुमान', ['Bajrangbali', 'Anjaneya', 'Maruti']),
    'ganesha': ('Ganesha', 'गणेश', ['Ganesh', 'Ganapati', 'Ganpati', 'Vinayaka']),
    'devi': ('Devi / Mata', 'माता', ['Maa', 'Shakti', 'Durga', 'Kali', 'Amman', 'Bhagavathy', 'Parvati', 'Lakshmi']),
    'murugan': ('Murugan', 'कार्तिकेय', ['Kartikeya', 'Skanda', 'Subramanya', 'Subramaniar']),
    'brahma': ('Brahma', 'ब्रह्मा', ['Phra Phrom']), 'surya': ('Surya', 'सूर्य', ['Sun', 'Aditya']),
    'ayyappa': ('Ayyappa', 'अय्यप्पा', ['Sastha']), 'swaminarayan': ('Swaminarayan', 'स्वामिनारायण', ['Sahajanand']),
    'sita': ('Sita', 'सीता', ['Janaki']), 'radha': ('Radha', 'राधा', ['Radharani']),
    'ganga': ('Ganga', 'गंगा', []), 'yamuna': ('Yamuna', 'यमुना', []),
    'saraswati': ('Saraswati', 'सरस्वती', ['Sharada']), 'andal': ('Andal', 'आंडाल', ['Goda']),
    'bhairava': ('Bhairava', 'भैरव', ['Bhairav', 'Kaal Bhairav']),
    'jagannath': ('Jagannath', 'जगन्नाथ', []), 'balarama': ('Balarama', 'बलराम', ['Balabhadra']),
    'subhadra': ('Subhadra', 'सुभद्रा', []), 'narasimha': ('Narasimha', 'नरसिंह', ['Narsingh']),
    'nagaraja': ('Nagaraja', 'नागराज', ['Naga', 'Serpent deities']),
    'khatu-shyam': ('Khatu Shyam', 'खाटू श्याम', ['Barbarika']),
    'gorakhnath': ('Gorakhnath', 'गोरखनाथ', []), 'sai-baba': ('Sai Baba', 'साईं बाबा', []),
    'chaitanya': ('Chaitanya', 'चैतन्य', ['Gauranga']),
    'parashurama': ('Parashurama', 'परशुराम', []), 'dattatreya': ('Dattatreya', 'दत्तात्रेय', ['Datta']),
    'sea-deity': ('Balinese sea deity tradition', None, ['Dewa Baruna', 'Bhatara Segara'])
}
COLLECTIONS = {
    'jyotirlinga': ('12 Jyotirlingas', 12, 'A widely followed twelve-shrine selection. Vaidyanath, Nageshwar and Bhimashankar have alternative regional identifications; this is not a ruling on those traditions.'),
    'char-dham': ('Char Dham of India', 4, 'Badrinath, Dwarka, Puri and Rameswaram. Distinct from the four Uttarakhand shrines.'),
    'chota-char-dham': ('Uttarakhand Char Dham', 4, 'Yamunotri, Gangotri, Kedarnath and Badrinath; annual opening dates and registration require current confirmation.'),
    'panch-kedar': ('Panch Kedar', 5, 'Five Himalayan Shiva shrines; collection order is not a driving itinerary.'),
    'ashtavinayaka': ('Ashtavinayaka', 8, 'Eight Ganapati shrines of Maharashtra. Traditional pilgrimage returns to Morgaon.'),
    'arupadai-veedu': ('Six Abodes of Murugan', 6, 'The six traditional Murugan pilgrimage temples in Tamil Nadu.'),
    'pancha-bhoota': ('Pancha Bhoota Shiva Temples', 5, 'Five temples associated with earth, water, fire, air and space.'),
    'great-living-chola': ('Great Living Chola Temples', 3, 'Thanjavur, Gangaikonda Cholapuram and Darasuram.')
}
LOCALITY_ARTICLES = {'Gangotri', 'Yamunotri', 'Vindhyavasini', 'Ambaji', 'Maihar', 'Mayapur',
                     'Murudeshwar', 'Ganga Talao', 'Devi Kanya Kumari', 'Naina Devi', 'Tarapith'}
HERITAGE = {'Konark Sun Temple', 'Modhera Sun Temple', 'Vijaya Vittala Temple', 'Kandariya Mahadeva Temple',
            'Prambanan Temple Compounds', 'Hoysaleswara Temple', 'Airavatesvara Temple'}
SEASONAL = {'Badrinath Temple', 'Kedarnath Temple', 'Gangotri Temple', 'Yamunotri Temple',
            'Tungnath Temple', 'Rudranath Temple', 'Madhyamaheshwar Temple', 'Amarnath Cave Temple', 'Sabarimala Temple'}
TREK = {'Kedarnath Temple', 'Yamunotri Temple', 'Tungnath Temple', 'Rudranath Temple',
        'Madhyamaheshwar Temple', 'Amarnath Cave Temple', 'Vaishno Devi Temple', 'Sabarimala Temple'}


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()).strip('-')


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def main():
    archive = BASE / 'legacy.travel.json.gz'
    if not archive.exists():
        original = (ROOT / 'travel.json').read_bytes()
        if 'schema_version' in json.loads(original.decode('utf-8-sig')):
            raise RuntimeError('Original archive missing; refusing to archive a generated catalogue.')
        archive.write_bytes(gzip.compress(original, mtime=0))
    original = gzip.decompress(archive.read_bytes())
    legacy = json.loads(original.decode('utf-8-sig'))
    refs = json.loads((BASE / 'references.json').read_text(encoding='utf-8'))
    primary = json.loads((BASE / 'primary_sources.json').read_text(encoding='utf-8'))
    image_checks_path = BASE / 'image_checks.json'
    image_checks = json.loads(image_checks_path.read_text(encoding='utf-8')) if image_checks_path.exists() else {}
    registry_path = BASE / 'ids.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8')) if registry_path.exists() else {}
    temples = []
    for name, article, country, region, city, deity_text, collection_text, highlight in rows():
        deity_ids = deity_text.split(',')
        collection_ids = collection_text.split(',') if collection_text else []
        ref = refs.get(article, {})
        country_name, zone = COUNTRIES[country]
        if country == 'US': zone = 'America/Los_Angeles' if region == 'California' else 'America/New_York'
        if country == 'AU': zone = 'Australia/Melbourne' if region == 'Victoria' else 'Australia/Sydney'
        if country == 'ID': zone = 'Asia/Makassar' if region == 'Bali' else 'Asia/Jakarta'
        identity_key = f'{country}:{article}'
        temple_id = registry.setdefault(identity_key, f'{country.lower()}-{slug(city)}-{slug(name)}')
        query = ', '.join(dict.fromkeys([name, city, region, country_name]))
        sources = []
        if name in primary:
            sources.append({'id': 'primary', 'url': primary[name], 'type': 'temple_or_public_institution',
                            'reviewed_on': DATE, 'review_method': 'web_search_excerpt_or_page',
                            'scope': ['identity', 'selected_background'], 'does_not_verify': ['all_visitor_services', 'all_coordinates', 'all_editorial_claims']})
        if ref.get('status') == 'reference_retrieved':
            sources.append({'id': 'reference', 'url': ref.get('resolved_url', ref['url']), 'type': 'encyclopedia',
                            'retrieved_at': ref['retrieved_at'], 'review_method': 'automated_page_and_infobox_retrieval',
                            'scope': ['reference_identity', 'infobox_location', 'infobox_named_facts'],
                            'title': ref.get('page_title')})
        location_status = 'reference_point' if ref.get('latitude') is not None else 'coordinates_pending'
        latitude, longitude = ref.get('latitude'), ref.get('longitude')
        if ref.get('status') != 'reference_retrieved': latitude = longitude = None
        if article in LOCALITY_ARTICLES:
            location_status = 'locality_reference_only' if latitude is not None else 'coordinates_pending'
        photo = ref.get('photo') if article not in LOCALITY_ARTICLES and ref.get('status') == 'reference_retrieved' else None
        if photo:
            check = image_checks.get(photo['url'])
            if check and not check['reachable']:
                photo = None
            elif check:
                photo = dict(photo, link_status='reachable_at_check', link_checked_at=check['checked_at'])
        infobox = ref.get('infobox', {})
        # Named fields can themselves be wrong; apply only explicitly reviewed corrections.
        dedication_text = re.sub(r'\[[^\]]+\]', '', infobox.get('Deity', '')).strip()
        dedication_source = 'reference' if dedication_text else None
        if dedication_text.lower() in ('hindu', 'hinduism'):
            dedication_text = ''
            dedication_source = None
        if name == 'Sri Siva Subramaniya Temple':
            dedication_text = 'Murugan (Subramaniya Swami)'
            dedication_source = 'primary'
        festivals = re.sub(r'\[[^\]]+\]', '', infobox.get('Festivals', '')).strip()
        architecture = re.sub(r'\[[^\]]+\]', '', infobox.get('Architecture', infobox.get('Style', ''))).strip()
        district = re.sub(r'\[[^\]]+\]', '', infobox.get('District', '')).strip() or None
        aliases = sorted(set([article.replace('_', ' ')] if article.lower() != name.lower() else []))
        notes = []
        if name in SEASONAL:
            notes.append('This shrine has seasonal or designated opening periods. Check the current temple calendar before planning travel.')
        if name in TREK:
            notes.append('The pilgrimage includes a walking or hill approach. Confirm route conditions and assistance arrangements before departure.')
        if name == 'Batu Caves Sri Subramaniar Temple':
            notes.append('The main cave approach has 272 steps; confirm alternative access arrangements if required.')
        if name in HERITAGE:
            notes.append('Plan as a heritage visit; do not assume daily darshan or unrestricted access to every structure.')
        if name == 'Muktinath Temple':
            notes.append('This is a high-altitude destination. Allow for acclimatisation and check transport and weather conditions locally.')
        if name == 'BAPS Hindu Mandir, Abu Dhabi':
            notes.append('The official BAPS page states that visitor registration is required. Recheck the booking instructions before travel.')
        if name == 'Tanah Lot Temple':
            notes.append('Tides affect the coastal approach; public sightseeing access does not imply entry into the worship area.')
        if name == 'Umananda Temple':
            notes.append('Confirm local ferry operation and the return crossing before visiting the island.')
        labels = [DEITIES[d][0] for d in deity_ids]
        summary = f'{name} is located in {city}, {region}, {country_name}. {highlight}'
        visiting = {
            'timezone': zone, 'hours': [], 'hours_status': 'not_verified', 'hours_source_id': None,
            'seasonal_opening': name in SEASONAL, 'seasonal_opening_dates': None,
            'entry_fee': {'amount': None, 'currency': None, 'status': 'not_verified'},
            'booking': {'required': True if name == 'BAPS Hindu Mandir, Abu Dhabi' else None,
                        'information_url': primary.get(name), 'status': 'recheck_before_visit'},
            'accessibility': {'wheelchair_accessible': None, 'step_free_route': None, 'status': 'not_verified'},
            'dress_code': {'text': None, 'status': 'confirm_with_temple'},
            'photography': {'allowed': None, 'status': 'confirm_with_temple'},
            'entry_eligibility': {'text': None, 'status': 'confirm_with_temple'},
            'suggested_visit_duration_minutes': None, 'notes': notes,
            'general_etiquette': ['Follow posted footwear and dress requirements.', 'Ask before photographing worship, people or sanctums.', 'Follow the temple\'s current queue and offering arrangements.']
        }
        if name == 'Sri Venkateswara Temple, Helensburgh':
            visiting['hours'] = [
                {'days': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 'sessions': [{'opens':'08:00','closes':'12:00'},{'opens':'16:00','closes':'19:00'}]},
                {'days': ['Saturday','Sunday'], 'sessions': [{'opens':'08:00','closes':'19:00'}]}]
            visiting['hours_status'] = 'source_checked_recheck_before_visit'
            visiting['hours_source_id'] = 'primary'
            visiting['notes'].append('The official site lists continuous 08:00–19:00 opening on public holidays and festival days; exceptions may apply.')
        details = {
            'name': name, 'thumbnail': photo['url'] if photo else '',
            'gallery': [photo['url']] if photo else [],
            'facilities': {key: None for key in ['wheelchair_accessible','parking','food_available','locker','washroom','medical_facility']},
            'opening_time': None, 'closing_time': None,
            'location': {'latitude': latitude, 'longitude': longitude, 'coordinate_status': location_status,
                         'coordinate_source_id': 'reference' if latitude is not None else None,
                         'coordinate_precision': 'Approximate reference position; not a verified visitor entrance.',
                         'address': query, 'address_precision': 'locality', 'country': country_name,
                         'country_code': country, 'state': region, 'city': city, 'district': district,
                         'postal_code': None, 'google_place_id': None,
                         'google_maps_url': 'https://www.google.com/maps/search/?' + urlencode({'api':1,'query':query}),
                         'directions_url': 'https://www.google.com/maps/dir/?' + urlencode({'api':1,'destination':query})},
            'description': summary, 'city': city, 'district': district, 'religion': 'Hindu',
            'category': 'Heritage temple' if name in HERITAGE else ('Sacred site' if name == 'Parshuram Kund' else 'Temple'),
            'best_time_to_visit': 'Confirm annual opening season' if name in SEASONAL else None,
            'denotes_to': ', '.join(labels), 'deity_ids': deity_ids, 'primary_deity_id': deity_ids[0],
            'dedication': {'text': dedication_text or ', '.join(labels),
                           'source_id': dedication_source,
                           'status': 'primary_source_checked' if dedication_source == 'primary' else ('reference_extracted' if dedication_text else 'editorial_category')},
            'collection_ids': collection_ids, 'highlights': [highlight],
            'architecture': {'text': architecture or None, 'source_id': 'reference' if architecture else None, 'status':'reference_extracted' if architecture else 'not_verified'},
            'festivals': {'text': festivals or None, 'source_id':'reference' if festivals else None, 'dates': [], 'status':'reference_extracted_dates_not_verified' if festivals else 'not_verified'},
            'visiting': visiting, 'contact': {'phone': None, 'email': None, 'information_url': primary.get(name)},
            'media': {'items': [dict(photo, alt=name, role='article_lead_photo')] if photo else [],
                      'status': 'attributed_reference_photo' if photo else 'photo_pending',
                      'fallback_asset': 'travel/assets/temple-placeholder.svg',
                      'fallback_is_temple_photo': False},
            'sources': sources,
            'data_quality': {'identity': 'primary_source_located' if name in primary else ('reference_located' if sources else 'needs_source_review'),
                             'editorial': 'written_summary_needs_full_fact_check',
                             'visitor_information': visiting['hours_status'],
                             'google_maps_listing_verified': False,
                             'last_editorial_update': DATE,
                             'unverified_fields': ['facilities','entry_fee','accessibility','dress_code','photography','entry_eligibility','phone','email','postal_code','google_place_id']}
        }
        keywords = set([name, city, region, country_name] + aliases)
        for deity in deity_ids:
            en, hi, terms = DEITIES[deity]
            keywords.update([en] + ([hi] if hi else []) + terms)
        temples.append({'id': temple_id, 'slug': slug(name), 'name': name, 'thumbnail': details['thumbnail'],
                        'aliases': aliases, 'country_code': country, 'state_name': region,
                        'search_keywords': sorted(keywords), 'details': details})
    ids = [t['id'] for t in temples]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate stable IDs')
    write(registry_path, registry)
    countries = []
    for code, (label, _) in COUNTRIES.items():
        subset = [t for t in temples if t['country_code'] == code]
        countries.append({'country_code': code, 'country_name': label, 'temple_count': len(subset),
                          'regions': [{'region_name': region, 'temple_ids': [t['id'] for t in subset if t['state_name'] == region]}
                                      for region in sorted({t['state_name'] for t in subset})]})
    # The legacy states branch is intentionally India-only. Countries references every entry once.
    states = [{'state_name': region, 'country_code': 'IN', 'temple_count': len(group), 'temples': group}
              for region in sorted({t['state_name'] for t in temples if t['country_code'] == 'IN'})
              if (group := [t for t in temples if t['country_code'] == 'IN' and t['state_name'] == region])]
    international = [t for t in temples if t['country_code'] != 'IN']
    collections = [{'id': key, 'name': title, 'expected_count': count, 'notes': note,
                    'temple_ids': [t['id'] for t in temples if key in t['details']['collection_ids']]}
                   for key, (title, count, note) in COLLECTIONS.items()]
    deity_catalogue = [{'id': key, 'name': label, 'name_hi': hi, 'aliases': aliases,
                        'temple_count': sum(key in t['details']['deity_ids'] for t in temples)}
                       for key, (label, hi, aliases) in DEITIES.items()]
    stats = {'temples': len(temples), 'india_temples': len(temples)-len(international),
             'international_temples': len(international), 'countries': len(countries), 'india_states_and_uts':len(states),
             'with_reference_coordinates': sum(t['details']['location']['latitude'] is not None for t in temples),
             'with_attributed_photos': sum(bool(t['thumbnail']) for t in temples),
             'with_primary_sources': len(primary), 'pilgrimage_collections':len(collections)}
    metadata = {'title':'Hindu Temple Travel Catalogue', 'updated_on':DATE, 'language':'en',
                'coverage':'Curated international catalogue; not an exhaustive census of Hindu temples.',
                'status':'research_catalogue_with_field_level_review_status', 'statistics':stats,
                'coordinate_system':'WGS84 / decimal degrees', 'null_policy':'null means unknown or not verified; never interpret as false, free, closed, or zero.',
                'map_policy':'Google Maps links are name-and-locality searches, not verified Place IDs, ratings or entrance coordinates.',
                'media_policy':'Display author, source link, license link and changes alongside every photo. Some photos still require visual identity review.',
                'source_policy':'Primary excerpts corroborate selected facts. Encyclopedia retrieval does not verify every claim. Current arrangements require rechecking.',
                'legacy_archive':'tools/travel/legacy.travel.json.gz', 'api_guide':'tools/travel/README.md',
                'schema':'travel.schema.json',
                'index':'travel/index.json', 'first_page':'travel/pages/001.json'}
    data = {'schema_version':'2.0.0', 'metadata':metadata, 'deities':deity_catalogue, 'collections':collections,
            'countries':countries, 'states':states, 'international_temples':international}
    write(ROOT/'travel.json', data)
    summaries=[]
    for t in temples:
        d=t['details']
        summaries.append({key:t[key] for key in ['id','name','thumbnail','country_code','state_name','search_keywords']} |
                         {'city':d['city'], 'deity_ids':d['deity_ids'], 'collection_ids':d['collection_ids'],
                          'summary':d['highlights'][0], 'detail_path':f'travel/temples/{t["id"]}.json',
                          'photo_credit': d['media']['items'][0] if d['media']['items'] else None})
        write(ROOT/f'travel/temples/{t["id"]}.json', {'schema_version':'2.0.0','temple':t})
    page_size=24
    total_pages=math.ceil(len(summaries)/page_size)
    for i in range(total_pages):
        write(ROOT/f'travel/pages/{i+1:03}.json', {'schema_version':'2.0.0','page':i+1,'page_size':page_size,
              'total_items':len(summaries),'total_pages':total_pages,
              'previous':f'travel/pages/{i:03}.json' if i else None,
              'next':f'travel/pages/{i+2:03}.json' if i+1<total_pages else None,
              'items':summaries[i*page_size:(i+1)*page_size]})
    write(ROOT/'travel/index.json', {'schema_version':'2.0.0','metadata':metadata, 'deities':deity_catalogue,
          'collections':collections,'countries':countries,'items':summaries})
    name_index=defaultdict(list)
    for t in temples:
        for n in [t['name']]+t['aliases']: name_index[slug(n)].append(t)
    migration=[]
    for si, state in enumerate(legacy['states']):
        for ti, old in enumerate(state['temples']):
            candidates={t['id']:t for t in name_index[slug(old['name'])]}
            # Refuse ambiguous aliases; localities and former state labels need editorial review.
            resolved=list(candidates)[0] if len(candidates)==1 and any(
                slug(state['state_name']) in {slug(t['state_name']),slug(t['details']['city'])}
                for t in candidates.values()) else None
            migration.append({'legacy_pointer':f'/states/{si}/temples/{ti}', 'name':old['name'],
                              'legacy_group':state['state_name'], 'temple_id':resolved,
                              'status':'matched_name_and_region' if resolved else 'needs_identity_scope_and_location_review'})
    write(BASE/'migration.json', {'original_sha256':hashlib.sha256(original).hexdigest(),
          'original_record_count':len(migration),'archive':'legacy.travel.json.gz','records':migration})
    write(BASE/'report.json', stats | {'original_records_preserved':len(migration),
          'legacy_records_needing_review':sum(x['temple_id'] is None for x in migration),
          'unresolved_reference_names':[t['name'] for t in temples if not t['details']['sources']]})
    print(json.dumps(stats, indent=2))


if __name__ == '__main__': main()
