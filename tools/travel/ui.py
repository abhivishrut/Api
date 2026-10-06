"""Additive, deterministic presentation contract for the eight supplied screens."""
from math import radians, sin, cos, asin, sqrt

VERSION = '2.1.0'
FAQ = 'https://www.shrikashivishwanath.org/pdffile/FAQ_SHRI_KASHI_VISHWANTH_TEMPLE_2_0_pdf.pdf'
KASHI = 'Shri Kashi Vishwanath Temple'
SECTIONS = [('overview','About Temple'),('significance','Spiritual Significance'),('history','History'),('architecture','Architecture'),('darshan','Darshan Timings'),('rituals','Aarti & Pooja'),('festivals','Major Festivals'),('gallery','Temple Gallery'),('how_to_reach','How to Reach'),('location','Location'),('before_visit','Before You Visit'),('guidelines','Temple Guidelines'),('nearby','Nearby Sacred Places'),('related','You May Also Like'),('journey','Continue your spiritual journey')]

def field(text=None, source_ids=None, status=None):
    return {'text':text,'source_ids':source_ids or [],'status':status or ('editorial' if text else 'not_verified')}

def enrich(temples, collections, deities, countries):
    by_name={t['name']:t for t in temples}
    titles={c['id']:c['name'] for c in collections}
    k=by_name[KASHI]; kd=k['details']
    for sid,url,scope in [
        ('visitor-faq',FAQ,['hours','rituals','transport','visitor_rules','festivals']),
        ('district','https://varanasi.nic.in/tourist-place/shri-kashi-vishwanath-temple/',['significance']),
        ('heritage','https://www.prod.incredibleindia.gov.in/content/incredible-india-v2/en/destinations/varanasi/vishwanath-mandir.html',['history','architecture']),
        ('dham','https://www.pib.gov.in/Pressreleaseshare.aspx?PRID=1780884',['history'])]:
        kd['sources'].append({'id':sid,'url':url,'type':'temple_or_public_institution','reviewed_on':'2026-10-06','review_method':'web_page_or_official_pdf','scope':scope})
    kd['opening_time']='03:00'; kd['closing_time']='23:00'
    kd['visiting'].update(hours=[{'days':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],'sessions':[{'opens':'03:00','closes':'23:00'}]}],hours_status='source_checked_recheck_before_visit',hours_source_id='visitor-faq')
    kd['data_quality']['visitor_information']=kd['visiting']['hours_status']
    kd['visiting']['dress_code']={'text':'Modest clothing advised.','status':'source_checked_recheck_before_visit','source_id':'visitor-faq'}
    kd['visiting']['photography']={'allowed':None,'text':'Gadgets are prohibited inside; confirm storage arrangements.','status':'source_checked_recheck_before_visit','source_id':'visitor-faq'}
    categories=[{'id':'all','label':'All','group':'all','temple_ids':[t['id'] for t in temples]}]
    for did,label in [('shiva','Shiva'),('vishnu','Vishnu'),('krishna','Krishna'),('hanuman','Hanuman'),('devi','Devi'),('ganesha','Ganesh'),('rama','Ram')]:
        categories.append({'id':did,'label':label,'group':'deity','temple_ids':[t['id'] for t in temples if did in t['details']['deity_ids']]})
    for cid,label in [('jyotirlinga','Jyotirlinga'),('shakti-peeth','Shakti Peeth'),('char-dham','Char Dham')]:
        categories.append({'id':cid,'label':label,'group':'circuit','temple_ids':[t['id'] for t in temples if cid in t['details']['collection_ids'] or (cid=='shakti-peeth' and t['name']=='Kamakhya Temple')]})
    categories[-2].update(coverage='Selected sourced sites; not a complete list. Traditions differ.',source_url='https://www.incredibleindia.gov.in/en/assam/guwahati/kamakhya-temple')
    for t in temples:
        d=t['details']; loc=d['location']; v=d['visiting']
        badges=[{'id':cid,'label':titles[cid],'basis':'pilgrimage_collection'} for cid in d['collection_ids']]
        if not badges and 'devi' in d['deity_ids']: badges=[{'id':'devi','label':'Devi Temple','basis':'deity_category'}]
        t['card']={'title':t['name'],'subtitle':f"{d['city']}, {t['state_name']}",'deity_label':d['denotes_to'],'image':d['media']['items'][0] if d['media']['items'] else None,'fallback_asset':d['media']['fallback_asset'],'badges':badges,'detail_path':f"travel/temples/{t['id']}.json"}
        info_url=d['contact']['information_url']
        u={
            'name_hi':None,'header_title':t['name'],'section_order':[x[0] for x in SECTIONS],
            'overview':{'title':'About Temple','summary':d['highlights'][0],'paragraphs':[d['description']],'status':d['data_quality']['editorial'],'facts':[{'id':'deity','label':'Main deity','value':d['denotes_to']},{'id':'hours','label':'Temple timings','value':'3:00 AM–11:00 PM' if t['name']==KASHI else None,'fallback':'Confirm current hours','status':v['hours_status']},{'id':'location','label':'Location','value':t['card']['subtitle']},{'id':'season','label':'Best season','value':d['best_time_to_visit'],'fallback':'Check local conditions'}]},
            'significance':{'title':'Spiritual Significance','heading':badges[0]['label'] if badges else d['denotes_to'],'body':field(d['highlights'][0],status='editorial_needs_review')},
            'history':{'title':'History','subtitle':'A heritage shaped by faith and renewal.','items':[],'empty_message':'Historical details are being researched.'},
            'architecture':{'title':'Architecture','body':field(d['architecture']['text'],[d['architecture']['source_id']] if d['architecture']['source_id'] else [],d['architecture']['status']),'features':[],'image':t['card']['image']},
            'darshan':{'title':'Darshan Timings','timezone':v['timezone'],'hours':v['hours'],'status':v['hours_status'],'source_id':v['hours_source_id'],'schedule':[],'notice':'Confirm current hours and bookings before visiting. Festival arrangements may differ.','information_url':info_url,'empty_message':'Current timings have not been verified.'},
            'rituals':{'title':'Aarti & Pooja','items':[],'empty_message':'Check the temple source for current rituals and bookings.'},
            'festivals':{'title':'Major Festivals','summary':d['festivals'],'items':[],'notice':'Dates follow the Hindu calendar and vary by year and tradition.','empty_message':'Festival details are being researched.'},
            'gallery':{'title':'Temple Gallery','items':d['media']['items'],'view_all_label':'View All Photos','empty_message':'Temple photos are not yet available.'},
            'how_to_reach':{'title':'How to Reach','items':[],'notice':'Distances and routes depend on the arrival point.','empty_message':'Use directions and confirm local access before travel.'},
            'location':dict(loc,title='Location',map_preview_url=None,map_preview_status='use_client_map_or_placeholder'),
            'before_visit':{'title':'Before You Visit','items':[{'id':key,'title':title,'icon':icon,'body':field(text,status='general_guidance')} for key,title,icon,text in [
                ('dress','Dress respectfully','shirt','Choose modest attire and confirm temple-specific dress guidance.'),('photography','Phones & photography','camera-off','Confirm device and photography restrictions at the entrance.'),('footwear','Footwear','footprints','Follow posted footwear and storage instructions.'),('entry','Entry & special darshan','ticket','Consult the temple source for eligibility, booking and charges.'),('crowds','Crowds & queues','users','Allow extra time on festival days and follow staff guidance.'),('season','Choosing your visit','sun',d['best_time_to_visit'] or 'Check local weather and seasonal access before travelling.')]]},
            'guidelines':{'title':'Temple Guidelines','items':v['general_etiquette']+['Keep valuables secure and follow staff directions.'],'status':'general_guidance'},
            'nearby':{'title':'Nearby Sacred Places','items':[],'basis':'same_locality','notice':'Same-locality suggestions; distances are straight-line estimates, not travel routes.','empty_message':'No other catalogued temples in this locality.'},
            'related':{'title':'You May Also Like','items':[],'basis':'shared_collection_then_deity','empty_message':'More recommendations will appear as the catalogue grows.'},
            'actions':{'directions':{'label':'Get Directions','url':loc['directions_url']},'maps':{'label':'Open in Maps','url':loc['google_maps_url']},'save':{'label':'Save','saved_label':'Saved','action':'toggle_local_favorite','storage_key':t['id']},'share':{'label':'Share','action':'native_share','text':f"{t['name']} — {t['card']['subtitle']}",'url':loc['google_maps_url']},'read_more':{'label':'Read More','action':'expand_overview'}},
            'journey':{'config_path':'travel/discovery.json#/journey'}
        }
        d['ui']=u
    u=kd['ui']; u['name_hi']='श्री काशी विश्वनाथ मंदिर'; u['header_title']='Kashi Vishwanath'
    u['significance'].update(heading='One of the twelve Jyotirlingas',body=field('Kashi Vishwanath is a Shiva shrine beside the Ganga in Varanasi. Its Jyotirlinga holds a central place in the pilgrimage traditions of Kashi.',['district'],'source_checked'))
    u['history']['items']=[{'period':'1780','title':'Rebuilt under Ahilyabai Holkar','body':field('The present temple took shape under the patronage of the queen of Indore.',['heritage'],'source_checked')},{'period':'2021-12-13','title':'Kashi Vishwanath Dham inaugurated','body':field('The Dham project renewed the precinct and its connection to the Ganga.',['dham'],'source_checked')}]
    u['architecture']['body']=field('The gilded spire and dome distinguish the temple in the old city skyline.',['heritage'],'source_checked'); u['architecture']['features']=['Spire','Gold-covered dome']
    u['darshan']['schedule']=[{'label':label,'opens':start,'closes':end,'source_id':'visitor-faq','status':'source_checked_recheck_before_visit'} for label,start,end in [('Mangala Aarti','03:00','04:00'),('General Darshan','04:00','11:00'),('Bhog Aarti','11:15','12:20'),('General Darshan','12:20','19:00'),('Sapta Rishi Aarti','19:00','20:15'),('General Darshan','20:30','21:00'),('Shringar Aarti','21:00','22:15')]]
    u['rituals']['items']=[{'id':rid,'title':title,'icon':icon,'description':desc,'learn_more_label':'Learn More','url':'https://shrikashivishwanath.org/','source_id':'visitor-faq'} for rid,title,icon,desc in [('mangala-aarti','Mangala Aarti','sunrise','Early morning worship.'),('rudrabhishek','Rudrabhishek','droplets','Shiva abhishek; booking information online.')]]
    u['festivals']['items']=[{'id':str(i),'name':name,'icon':'flower','month_label':None,'dates':[],'source_id':'visitor-faq'} for i,name in enumerate(['Rangbhari Ekadashi','Diwali','Monthly Shivratri','Mahashivratri','Kartik observances'])]
    u['how_to_reach']['items']=[{'mode':mode,'title':title,'icon':icon,'arrival_point':point,'distance_km':None,'body':field('Arrange onward local transport and confirm the drop-off point.',['visitor-faq'],'source_checked'),'source_id':'visitor-faq'} for mode,title,icon,point in [('air','By air','plane','Lal Bahadur Shastri International Airport'),('rail','By rail','train','Varanasi Junction'),('road','By road','bus','Chaudhary Charan Singh Bus Stand')]]
    u['before_visit']['items'][0]['body']=field(kd['visiting']['dress_code']['text'],['visitor-faq'],'source_checked_recheck_before_visit')
    u['before_visit']['items'][1]['body']=field(kd['visiting']['photography']['text'],['visitor-faq'],'source_checked_recheck_before_visit')
    for t in temples:
        d=t['details']; ui=d['ui']
        def recommendation(other, distance=False):
            result={'temple_id':other['id'],'card':other['card']}
            if distance:
                a=d['location']; b=other['details']['location']; km=None
                if a['coordinate_status']==b['coordinate_status']=='reference_point' and all(x is not None for x in [a['latitude'],a['longitude'],b['latitude'],b['longitude']]):
                    lat1,lon1,lat2,lon2=map(radians,[a['latitude'],a['longitude'],b['latitude'],b['longitude']]); h=sin((lat2-lat1)/2)**2+cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2; km=round(12742*asin(sqrt(min(1,h))),1)
                result.update(distance_km=km,distance_kind='approximate_straight_line' if km is not None else 'unknown')
            return result
        others=[o for o in temples if o['id']!=t['id']]
        ui['nearby']['items']=[recommendation(o,True) for o in others if (o['country_code'],o['state_name'],o['details']['city'])==(t['country_code'],t['state_name'],d['city'])][:6]
        related=[o for o in others if set(d['collection_ids']) & set(o['details']['collection_ids']) or set(d['deity_ids']) & set(o['details']['deity_ids'])]
        related.sort(key=lambda o:(not bool(set(d['collection_ids']) & set(o['details']['collection_ids'])),o['id']))
        ui['related']['items']=[recommendation(o) for o in related[:3]]
    def choose(names): return [by_name[n]['id'] for n in names if n in by_name]
    return {'schema_version':VERSION,'title':'Famous Temples','brand':'HARINAAM','eyebrow':'YOUR HERITAGE COMPANION','hero':{'title':'Explore Sacred Temples','description':'Discover sacred temples across India and the world, their heritage, traditions and visitor guidance.','image':k['card']['image'],'fallback_asset':kd['media']['fallback_asset']},'search':{'placeholder':'Search temples, cities or deities','fields':['name','search_keywords','city','state_name'],'matching':'case-insensitive substring; Unicode NFKC normalization'},'categories':categories,'additional_deities':deities,'locations':countries,'filters':{'title':'Explore your way','description':'Choose locations and sacred categories.','location_title':'Explore by Location','category_title':'Deity & sacred circuit','all_locations_label':'All locations','selected_count_template':'{count} selected','reset_label':'Reset','apply_label':'Apply Filters','notice':'Selections are combined to refine temple discovery.','within_group':'OR','between_groups':'AND','location_key':['country_code','region_name'],'all_behavior':'Clear deity and circuit selections; retain location and search.','execution':'client_side_over_complete_index'},'featured':{'title':'Featured Temples','view_all_label':'View All','temple_ids':choose(['Kedarnath Temple','Somnath Temple',KASHI]),'selection':'editorial'},'popular':{'title':'Popular Temples','subtitle':'Sacred places, cherished across generations.','temple_ids':choose([KASHI,'Jagannath Temple, Puri','Banke Bihari Temple','Meenakshi Amman Temple','Tirumala Venkateswara Temple','Sankat Mochan Hanuman Temple','Siddhivinayak Temple, Mumbai']),'selection':'editorial; not live visitor rankings'},'states':{'loading':{'message':'Loading temples...','skeleton_sections':['hero','search','categories','featured','popular']},'empty':{'title':'No temples found','message':'Try another location or category.','action_label':'Reset Filters'},'error':{'title':'Unable to load temples','message':'Check your connection and try again.','action_label':'Retry'},'offline':{'message':'Showing saved catalogue. Details may have changed.'}},'labels':{'favorites':'Saved Temples','back':'Back','close':'Close','view_all':'View All','photo_credit':'Photo credit','unknown':'Not yet verified'},'footer':'Discover with reverence. Plan with care.','section_titles':dict(SECTIONS),'journey':{'brand':'HARINAAM','title':'Continue your spiritual journey','subtitle':'Carry a little of this sacred stillness into your everyday practice.','items':[{'id':rid,'title':title,'subtitle':sub,'icon':icon,'action':'app_route','route_key':rid} for rid,title,sub,icon in [('bhagavad-gita','Bhagavad Gita','Wisdom for daily life','book-open'),('bhajans-mantras','Bhajans & Mantras','Listen with devotion','music'),('mala-jaap','Mala Jaap','Make time for your practice','circle'),('panchang','Panchang','Stay connected to sacred days','calendar'),('home','Explore Harinaam','More stories and devotional content','compass')]]},'client_contract':{'favorites':'Store locally per stable temple ID; never shared catalogue state.','navigation':'Map route_key to existing app destinations; keys are not executable URLs. Hide unsupported destinations.','bootstrap':'Bundle this configuration for first-load skeleton and error labels.','images':'Use attributed media only; design images are not licensed API assets.','map':'Render coordinates with a map provider or show a placeholder; do not treat the design illustration as navigation.'}}
