import json
import os

file_path = "c:/Users/DMT/Documents/GitHub/Api/travel.json"

def get_helper_info(name, state, city, lat, lon):
    return {
        "travel_information": {
            "from": "Delhi",
            "routes": [
                {
                    "travel_type": "Car",
                    "distance_km": 1000,
                    "estimated_duration": "20 hours",
                    "estimated_cost": 15000,
                    "fuel_required": "100 Liters",
                    "road_condition": "Mixed, mostly good highways",
                    "difficulty": "Moderate",
                    "toll_cost": 1200,
                    "google_maps_link": f"https://maps.google.com/route_delhi_{city.lower()}",
                    "alternative_route": "Via alternative highway",
                    "fastest_route": "Via Main Expressways",
                    "shortest_route": "Via NH",
                    "scenic_route": "Via state highways",
                    "route_stops": [
                        {
                            "name": "Delhi",
                            "state": "Delhi",
                            "latitude": 28.6139,
                            "longitude": 77.2090,
                            "distance_from_previous": 0,
                            "travel_time": "0 mins",
                            "road_type": "Highway",
                            "food": True,
                            "fuel": True,
                            "hotel": True,
                            "hospital": True,
                            "atm": True,
                            "washroom": True,
                            "police": True,
                            "tourist_spot": False,
                            "photo": "https://api.example.com/images/delhi.jpg"
                        },
                        {
                            "name": city,
                            "state": state,
                            "latitude": lat,
                            "longitude": lon,
                            "distance_from_previous": 1000,
                            "travel_time": "20 hours",
                            "road_type": "Highway",
                            "food": True,
                            "fuel": True,
                            "hotel": True,
                            "hospital": True,
                            "atm": True,
                            "washroom": True,
                            "police": True,
                            "tourist_spot": True,
                            "photo": f"https://api.example.com/images/{city.lower().replace(' ','_')}.jpg"
                        }
                    ]
                }
            ],
            "train_information": {
                "train_name": "Express",
                "train_number": "12345",
                "departure_station": "New Delhi (NDLS)",
                "arrival_station": f"{city} Jn",
                "departure_time": "18:00",
                "arrival_time": "08:00",
                "duration": "14 hours",
                "available_classes": ["1A", "2A", "3A", "SL"],
                "important_intermediate_stations": ["Intermediate 1", "Intermediate 2"],
                "irctc_placeholder": "https://www.irctc.co.in/"
            },
            "flight_information": {
                "departure_airport": "Indira Gandhi International Airport (DEL)",
                "arrival_airport": f"{city} Airport",
                "airlines": ["IndiGo", "Air India", "Vistara"],
                "estimated_fare": 6000,
                "airport_to_destination_distance": 25,
                "airport_transfer_options": ["Taxi", "Bus"]
            },
            "bus_information": {
                "government_bus": True,
                "private_bus": True,
                "volvo": True,
                "sleeper": True,
                "departure": "ISBT Kashmere Gate",
                "arrival": f"{city} Bus Stand",
                "major_stops": ["Stop 1", "Stop 2"],
                "fare": 1500,
                "booking_placeholder": "https://www.redbus.in/"
            }
        },
        "weather": {
            "summer": "35°C to 40°C",
            "winter": "15°C to 25°C",
            "monsoon": "25°C to 30°C, heavy rainfall",
            "best_season": "Winter",
            "snowfall": False
        },
        "accommodation": {
            "hotel": True,
            "dharamshala": True,
            "ashram": True,
            "guest_house": True,
            "budget_range": "1000 - 8000 INR",
            "contact": "+91-0000000000",
            "booking_placeholder": "https://booking.example.com"
        },
        "food": {
            "local_food": ["Local Dish 1", "Local Dish 2"],
            "satvik_food": True,
            "prasad": "Sweet Prasad",
            "restaurants": ["Restaurant A", "Restaurant B"]
        }
    }

places = [
    {
        "religion_name": "Hindu",
        "region_name": "South India",
        "state_name": "Tamil Nadu",
        "dest": {
            "id": "hnd-tn-001",
            "name": "Meenakshi Amman Temple",
            "alternative_names": ["Meenakshi Sundareswarar Temple"],
            "religion": "Hindu",
            "category": "Temple",
            "subcategory": "Shiva/Parvati Temple",
            "state": "Tamil Nadu",
            "district": "Madurai",
            "city": "Madurai",
            "village": "",
            "region": "South India",
            "latitude": 9.9195,
            "longitude": 78.1193,
            "elevation": "101m",
            "description": "A historic Hindu temple located on the southern bank of the Vaigai River in the temple city of Madurai, Tamil Nadu, India.",
            "history": "Built by Pandayan emperor Sadayavarman Kulasekaran I in 1190-1205 AD.",
            "religious_significance": "Dedicated to Meenakshi (a form of Parvati) and Sundareshwar (a form of Shiva).",
            "architecture": "Dravidian architecture with massive gopurams.",
            "main_deity_or_revered_person": "Goddess Meenakshi",
            "established_year": "12th century",
            "founder": "Pandya Dynasty",
            "best_time_to_visit": "October to March",
            "climate": "Tropical",
            "opening_time": "05:00",
            "closing_time": "22:00",
            "entry_fee": 0,
            "dress_code": "Traditional wear",
            "photography_allowed": False,
            "wheelchair_accessible": True,
            "parking": True,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["hotel", "dharamshala"],
            "official_website": "https://maduraimeenakshi.hrce.tn.gov.in/",
            "google_maps": "https://maps.google.com/?q=9.9195,78.1193",
            "thumbnail": "https://api.example.com/images/meenakshi_thumb.jpg",
            "banner": "https://api.example.com/images/meenakshi_banner.jpg",
            "gallery": ["https://api.example.com/images/meenakshi_1.jpg", "https://api.example.com/images/meenakshi_2.jpg"],
            "popularity_rating": 4.9,
            "estimated_visit_duration": "4 hours",
            "travel_tips": "Start early, the temple covers a large area.",
            "nearby_attractions": [
                {
                    "name": "Thirumalai Nayakkar Mahal",
                    "category": "Palace",
                    "distance": "1.5 km",
                    "travel_time": "10 mins",
                    "description": "17th century palace built by King Tirumala Nayaka."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Meenakshi Tirukalyanam",
                    "month": "April",
                    "importance": "High",
                    "duration": "10 days",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 1000000
                }
            ]
        }
    },
    {
        "religion_name": "Hindu",
        "region_name": "East India",
        "state_name": "Odisha",
        "dest": {
            "id": "hnd-od-001",
            "name": "Jagannath Temple",
            "alternative_names": ["Shree Jagannath Temple"],
            "religion": "Hindu",
            "category": "Char Dham",
            "subcategory": "Vaishnav Temple",
            "state": "Odisha",
            "district": "Puri",
            "city": "Puri",
            "village": "",
            "region": "East India",
            "latitude": 19.8049,
            "longitude": 85.8179,
            "elevation": "0m",
            "description": "An important Hindu temple dedicated to Jagannath, a form of Vishnu, in Puri.",
            "history": "Built by King Anantavarman Chodaganga Deva in the 12th century.",
            "religious_significance": "One of the Char Dham pilgrimage sites.",
            "architecture": "Kalinga architecture.",
            "main_deity_or_revered_person": "Lord Jagannath",
            "established_year": "1161",
            "founder": "Anantavarman Chodaganga",
            "best_time_to_visit": "October to February",
            "climate": "Tropical",
            "opening_time": "05:00",
            "closing_time": "23:00",
            "entry_fee": 0,
            "dress_code": "Traditional/Modest clothing",
            "photography_allowed": False,
            "wheelchair_accessible": True,
            "parking": True,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["ashram", "hotel", "dharamshala"],
            "official_website": "https://shreejagannatha.in/",
            "google_maps": "https://maps.google.com/?q=19.8049,85.8179",
            "thumbnail": "https://api.example.com/images/jagannath_thumb.jpg",
            "banner": "https://api.example.com/images/jagannath_banner.jpg",
            "gallery": ["https://api.example.com/images/jagannath_1.jpg", "https://api.example.com/images/jagannath_2.jpg"],
            "popularity_rating": 4.9,
            "estimated_visit_duration": "3 hours",
            "travel_tips": "Do not carry leather items. Enjoy the Mahaprasad.",
            "nearby_attractions": [
                {
                    "name": "Puri Beach",
                    "category": "Beach",
                    "distance": "2 km",
                    "travel_time": "10 mins",
                    "description": "Famous beach on the Bay of Bengal."
                },
                {
                    "name": "Konark Sun Temple",
                    "category": "Temple",
                    "distance": "35 km",
                    "travel_time": "1 hour",
                    "description": "13th-century Sun Temple (UNESCO World Heritage)."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Rath Yatra",
                    "month": "July",
                    "importance": "High",
                    "duration": "9 days",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 2000000
                }
            ]
        }
    },
    {
        "religion_name": "Hindu",
        "region_name": "West India",
        "state_name": "Maharashtra",
        "dest": {
            "id": "hnd-mh-001",
            "name": "Siddhivinayak Temple",
            "alternative_names": ["Shree Siddhivinayak Ganapati Mandir"],
            "religion": "Hindu",
            "category": "Temple",
            "subcategory": "Ganesha Temple",
            "state": "Maharashtra",
            "district": "Mumbai City",
            "city": "Mumbai",
            "village": "Prabhadevi",
            "region": "West India",
            "latitude": 19.0168,
            "longitude": 72.8298,
            "elevation": "14m",
            "description": "A Hindu temple dedicated to Lord Shri Ganesha.",
            "history": "Built in 1801 by Laxman Vithu and Deubai Patil.",
            "religious_significance": "One of the richest temples in India, heavily visited by devotees.",
            "architecture": "Modern temple architecture with a gold-plated inner roof.",
            "main_deity_or_revered_person": "Lord Ganesha",
            "established_year": "1801",
            "founder": "Laxman Vithu",
            "best_time_to_visit": "Throughout the year",
            "climate": "Tropical",
            "opening_time": "05:30",
            "closing_time": "21:50",
            "entry_fee": 0,
            "dress_code": "Modest clothing",
            "photography_allowed": False,
            "wheelchair_accessible": True,
            "parking": False,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["hotel"],
            "official_website": "https://www.siddhivinayak.org/",
            "google_maps": "https://maps.google.com/?q=19.0168,72.8298",
            "thumbnail": "https://api.example.com/images/siddhi_thumb.jpg",
            "banner": "https://api.example.com/images/siddhi_banner.jpg",
            "gallery": ["https://api.example.com/images/siddhi_1.jpg", "https://api.example.com/images/siddhi_2.jpg"],
            "popularity_rating": 4.8,
            "estimated_visit_duration": "2 hours",
            "travel_tips": "Expect heavy crowds on Tuesdays.",
            "nearby_attractions": [
                {
                    "name": "Dadar Chowpatty",
                    "category": "Beach",
                    "distance": "2 km",
                    "travel_time": "10 mins",
                    "description": "A quiet beach near the temple."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Ganesh Chaturthi",
                    "month": "August/September",
                    "importance": "High",
                    "duration": "11 days",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 500000
                }
            ]
        }
    },
    {
        "religion_name": "Hindu",
        "region_name": "North India",
        "state_name": "Uttar Pradesh",
        "dest": {
            "id": "hnd-up-001",
            "name": "Kashi Vishwanath Temple",
            "alternative_names": ["Golden Temple of Varanasi"],
            "religion": "Hindu",
            "category": "Jyotirlinga",
            "subcategory": "Shiva Temple",
            "state": "Uttar Pradesh",
            "district": "Varanasi",
            "city": "Varanasi",
            "village": "",
            "region": "North India",
            "latitude": 25.3109,
            "longitude": 83.0107,
            "elevation": "80m",
            "description": "One of the most famous Hindu temples dedicated to Lord Shiva.",
            "history": "Reconstructed in 1780 by Ahilyabai Holkar.",
            "religious_significance": "One of the twelve Jyotirlingas, the holiest of Shiva temples.",
            "architecture": "Classic North Indian style.",
            "main_deity_or_revered_person": "Lord Shiva",
            "established_year": "1780 (current structure)",
            "founder": "Ahilyabai Holkar",
            "best_time_to_visit": "October to March",
            "climate": "Humid subtropical",
            "opening_time": "03:00",
            "closing_time": "23:00",
            "entry_fee": 0,
            "dress_code": "Modest clothing",
            "photography_allowed": False,
            "wheelchair_accessible": True,
            "parking": False,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["ashram", "hotel", "dharamshala"],
            "official_website": "https://shrikashivishwanath.org/",
            "google_maps": "https://maps.google.com/?q=25.3109,83.0107",
            "thumbnail": "https://api.example.com/images/kashi_thumb.jpg",
            "banner": "https://api.example.com/images/kashi_banner.jpg",
            "gallery": ["https://api.example.com/images/kashi_1.jpg"],
            "popularity_rating": 4.9,
            "estimated_visit_duration": "3 hours",
            "travel_tips": "Mobile phones and electronic items are strictly prohibited.",
            "nearby_attractions": [
                {
                    "name": "Dashashwamedh Ghat",
                    "category": "Ghat",
                    "distance": "0.5 km",
                    "travel_time": "10 mins",
                    "description": "Main ghat in Varanasi on the Ganga River."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Maha Shivaratri",
                    "month": "February/March",
                    "importance": "High",
                    "duration": "1 day",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 300000
                }
            ]
        }
    },
    {
        "religion_name": "Muslim",
        "region_name": "North India",
        "state_name": "Delhi",
        "dest": {
            "id": "mus-dl-001",
            "name": "Jama Masjid",
            "alternative_names": ["Masjid-i Jehan-Numa"],
            "religion": "Muslim",
            "category": "Mosque",
            "subcategory": "Historical Mosque",
            "state": "Delhi",
            "district": "Central Delhi",
            "city": "New Delhi",
            "village": "",
            "region": "North India",
            "latitude": 28.6507,
            "longitude": 77.2334,
            "elevation": "216m",
            "description": "One of the largest mosques in India, built by Mughal Emperor Shah Jahan.",
            "history": "Built between 1650 and 1656 by Emperor Shah Jahan.",
            "religious_significance": "A central place of worship for Muslims in Delhi.",
            "architecture": "Mughal architecture, built with red sandstone and white marble.",
            "main_deity_or_revered_person": "Allah",
            "established_year": "1656",
            "founder": "Shah Jahan",
            "best_time_to_visit": "October to March",
            "climate": "Humid subtropical",
            "opening_time": "07:00",
            "closing_time": "18:00",
            "entry_fee": 0,
            "dress_code": "Modest clothing, head cover",
            "photography_allowed": True,
            "wheelchair_accessible": False,
            "parking": True,
            "food_available": True,
            "locker": False,
            "washroom": True,
            "medical_facility": False,
            "accommodation": ["hotel"],
            "official_website": "",
            "google_maps": "https://maps.google.com/?q=28.6507,77.2334",
            "thumbnail": "https://api.example.com/images/jama_thumb.jpg",
            "banner": "https://api.example.com/images/jama_banner.jpg",
            "gallery": ["https://api.example.com/images/jama_1.jpg"],
            "popularity_rating": 4.7,
            "estimated_visit_duration": "2 hours",
            "travel_tips": "Avoid visiting during prayer times if you are a tourist.",
            "nearby_attractions": [
                {
                    "name": "Red Fort",
                    "category": "Fort",
                    "distance": "1 km",
                    "travel_time": "5 mins",
                    "description": "Historic fort complex built by Shah Jahan."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Eid al-Fitr",
                    "month": "Varies",
                    "importance": "High",
                    "duration": "1 day",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 100000
                }
            ]
        }
    },
    {
        "religion_name": "Muslim",
        "region_name": "North India",
        "state_name": "Rajasthan",
        "dest": {
            "id": "mus-rj-001",
            "name": "Ajmer Sharif Dargah",
            "alternative_names": ["Dargah Sharif", "Ajmer Dargah"],
            "religion": "Muslim",
            "category": "Dargah",
            "subcategory": "Sufi Shrine",
            "state": "Rajasthan",
            "district": "Ajmer",
            "city": "Ajmer",
            "village": "",
            "region": "North India",
            "latitude": 26.4560,
            "longitude": 74.6282,
            "elevation": "486m",
            "description": "Sufi shrine of the revered Sufi saint, Moinuddin Chishti.",
            "history": "Built in the 13th century.",
            "religious_significance": "One of the holiest places of worship in India for Muslims and people of all faiths.",
            "architecture": "Mughal architecture.",
            "main_deity_or_revered_person": "Moinuddin Chishti",
            "established_year": "13th century",
            "founder": "Sultanate/Mughal rulers",
            "best_time_to_visit": "October to March",
            "climate": "Hot semi-arid",
            "opening_time": "04:00",
            "closing_time": "22:00",
            "entry_fee": 0,
            "dress_code": "Modest clothing, head cover",
            "photography_allowed": False,
            "wheelchair_accessible": False,
            "parking": False,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["hotel", "guest_house"],
            "official_website": "",
            "google_maps": "https://maps.google.com/?q=26.4560,74.6282",
            "thumbnail": "https://api.example.com/images/ajmer_thumb.jpg",
            "banner": "https://api.example.com/images/ajmer_banner.jpg",
            "gallery": ["https://api.example.com/images/ajmer_1.jpg"],
            "popularity_rating": 4.7,
            "estimated_visit_duration": "3 hours",
            "travel_tips": "Be prepared for large crowds.",
            "nearby_attractions": [
                {
                    "name": "Ana Sagar Lake",
                    "category": "Lake",
                    "distance": "3 km",
                    "travel_time": "15 mins",
                    "description": "Artificial lake in Ajmer."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Urs Festival",
                    "month": "Rajab",
                    "importance": "High",
                    "duration": "6 days",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 500000
                }
            ]
        }
    },
    {
        "religion_name": "Christian",
        "region_name": "South India",
        "state_name": "Goa",
        "dest": {
            "id": "chr-ga-001",
            "name": "Basilica of Bom Jesus",
            "alternative_names": ["Borea Jezuchi Bajilika"],
            "religion": "Christian",
            "category": "Church",
            "subcategory": "Basilica",
            "state": "Goa",
            "district": "North Goa",
            "city": "Old Goa",
            "village": "",
            "region": "South India",
            "latitude": 15.5009,
            "longitude": 73.9116,
            "elevation": "5m",
            "description": "A Roman Catholic basilica located in Goa, known for holding the mortal remains of St. Francis Xavier.",
            "history": "Construction began in 1594 and it was consecrated in 1605.",
            "religious_significance": "A UNESCO World Heritage Site and a major pilgrimage center.",
            "architecture": "Baroque architecture.",
            "main_deity_or_revered_person": "Jesus Christ / St. Francis Xavier",
            "established_year": "1605",
            "founder": "Jesuits",
            "best_time_to_visit": "November to February",
            "climate": "Tropical monsoon",
            "opening_time": "09:00",
            "closing_time": "18:30",
            "entry_fee": 0,
            "dress_code": "Modest clothing",
            "photography_allowed": True,
            "wheelchair_accessible": True,
            "parking": True,
            "food_available": True,
            "locker": False,
            "washroom": True,
            "medical_facility": False,
            "accommodation": ["hotel"],
            "official_website": "https://www.bomjesus.org/",
            "google_maps": "https://maps.google.com/?q=15.5009,73.9116",
            "thumbnail": "https://api.example.com/images/bom_thumb.jpg",
            "banner": "https://api.example.com/images/bom_banner.jpg",
            "gallery": ["https://api.example.com/images/bom_1.jpg"],
            "popularity_rating": 4.8,
            "estimated_visit_duration": "2 hours",
            "travel_tips": "Maintain silence inside the basilica.",
            "nearby_attractions": [
                {
                    "name": "Se Cathedral",
                    "category": "Church",
                    "distance": "0.5 km",
                    "travel_time": "5 mins",
                    "description": "One of the largest churches in Asia."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Feast of St. Francis Xavier",
                    "month": "December",
                    "importance": "High",
                    "duration": "1 day",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 100000
                }
            ]
        }
    },
    {
        "religion_name": "Buddhist",
        "region_name": "East India",
        "state_name": "Bihar",
        "dest": {
            "id": "bud-br-001",
            "name": "Mahabodhi Temple",
            "alternative_names": ["Great Awakening Temple"],
            "religion": "Buddhist",
            "category": "Temple",
            "subcategory": "Buddhist Temple",
            "state": "Bihar",
            "district": "Gaya",
            "city": "Bodh Gaya",
            "village": "",
            "region": "East India",
            "latitude": 24.6959,
            "longitude": 84.9914,
            "elevation": "113m",
            "description": "An ancient, but much rebuilt and restored, Buddhist temple in Bodh Gaya, marking the location where the Buddha is said to have attained enlightenment.",
            "history": "Originally built by Emperor Ashoka in the 3rd century BCE.",
            "religious_significance": "One of the four holy sites related to the life of the Lord Buddha.",
            "architecture": "Indian brick architecture.",
            "main_deity_or_revered_person": "Gautama Buddha",
            "established_year": "3rd century BCE",
            "founder": "Emperor Ashoka",
            "best_time_to_visit": "October to March",
            "climate": "Humid subtropical",
            "opening_time": "05:00",
            "closing_time": "21:00",
            "entry_fee": 0,
            "dress_code": "Modest clothing",
            "photography_allowed": True,
            "wheelchair_accessible": True,
            "parking": True,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["hotel", "monastery guest house"],
            "official_website": "https://mahabodhitample.bihar.gov.in/",
            "google_maps": "https://maps.google.com/?q=24.6959,84.9914",
            "thumbnail": "https://api.example.com/images/mahabodhi_thumb.jpg",
            "banner": "https://api.example.com/images/mahabodhi_banner.jpg",
            "gallery": ["https://api.example.com/images/mahabodhi_1.jpg"],
            "popularity_rating": 4.9,
            "estimated_visit_duration": "3 hours",
            "travel_tips": "Mobile phones must be deposited outside.",
            "nearby_attractions": [
                {
                    "name": "Bodhi Tree",
                    "category": "Sacred Tree",
                    "distance": "0 km",
                    "travel_time": "0 mins",
                    "description": "The sacred fig tree under which Buddha attained enlightenment."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Buddha Purnima",
                    "month": "May",
                    "importance": "High",
                    "duration": "1 day",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 200000
                }
            ]
        }
    },
    {
        "religion_name": "Sikh",
        "region_name": "North India",
        "state_name": "Punjab",
        "dest": {
            "id": "skh-pb-002",
            "name": "Anandpur Sahib",
            "alternative_names": ["Takht Sri Keshgarh Sahib"],
            "religion": "Sikh",
            "category": "Takht Sahib",
            "subcategory": "Gurudwara",
            "state": "Punjab",
            "district": "Rupnagar",
            "city": "Anandpur Sahib",
            "village": "",
            "region": "North India",
            "latitude": 31.2330,
            "longitude": 76.4984,
            "elevation": "310m",
            "description": "One of the most sacred places in Sikhism, closely linked with the religious traditions and history of Sikhism.",
            "history": "Founded in 1665 by the ninth Sikh Guru, Guru Tegh Bahadur.",
            "religious_significance": "The birthplace of the Khalsa.",
            "architecture": "Sikh architecture.",
            "main_deity_or_revered_person": "Guru Gobind Singh",
            "established_year": "1665",
            "founder": "Guru Tegh Bahadur",
            "best_time_to_visit": "October to March",
            "climate": "Humid subtropical",
            "opening_time": "03:00",
            "closing_time": "22:00",
            "entry_fee": 0,
            "dress_code": "Head covered, bare feet, modest clothing",
            "photography_allowed": True,
            "wheelchair_accessible": True,
            "parking": True,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": True,
            "accommodation": ["niwas", "hotel"],
            "official_website": "",
            "google_maps": "https://maps.google.com/?q=31.2330,76.4984",
            "thumbnail": "https://api.example.com/images/anandpur_thumb.jpg",
            "banner": "https://api.example.com/images/anandpur_banner.jpg",
            "gallery": ["https://api.example.com/images/anandpur_1.jpg"],
            "popularity_rating": 4.8,
            "estimated_visit_duration": "4 hours",
            "travel_tips": "Attend the Hola Mohalla festival for a unique experience.",
            "nearby_attractions": [
                {
                    "name": "Virasat-e-Khalsa",
                    "category": "Museum",
                    "distance": "2 km",
                    "travel_time": "10 mins",
                    "description": "Museum of Sikhism."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Hola Mohalla",
                    "month": "March",
                    "importance": "High",
                    "duration": "3 days",
                    "crowd_level": "Extremely High",
                    "estimated_visitors": 2000000
                }
            ]
        }
    },
    {
        "religion_name": "Jain",
        "region_name": "West India",
        "state_name": "Rajasthan",
        "dest": {
            "id": "jan-rj-001",
            "name": "Ranakpur Jain Temple",
            "alternative_names": ["Chaturmukha Dharanavihara"],
            "religion": "Jain",
            "category": "Temple",
            "subcategory": "Jain Temple",
            "state": "Rajasthan",
            "district": "Pali",
            "city": "Ranakpur",
            "village": "Ranakpur",
            "region": "West India",
            "latitude": 25.1154,
            "longitude": 73.4716,
            "elevation": "486m",
            "description": "A Jain temple at Ranakpur dedicated to Tirthankara Rishabhanatha.",
            "history": "Built in the 15th century by Dharna Shah, a Jain businessman.",
            "religious_significance": "One of the most important Jain shrines in India.",
            "architecture": "Māru-Gurjara architecture.",
            "main_deity_or_revered_person": "Adinath",
            "established_year": "1437",
            "founder": "Dharna Shah",
            "best_time_to_visit": "October to March",
            "climate": "Hot semi-arid",
            "opening_time": "12:00",
            "closing_time": "17:00",
            "entry_fee": 0,
            "dress_code": "Strictly modest, no leather items",
            "photography_allowed": True,
            "wheelchair_accessible": False,
            "parking": True,
            "food_available": True,
            "locker": True,
            "washroom": True,
            "medical_facility": False,
            "accommodation": ["dharamshala", "hotel"],
            "official_website": "",
            "google_maps": "https://maps.google.com/?q=25.1154,73.4716",
            "thumbnail": "https://api.example.com/images/ranakpur_thumb.jpg",
            "banner": "https://api.example.com/images/ranakpur_banner.jpg",
            "gallery": ["https://api.example.com/images/ranakpur_1.jpg"],
            "popularity_rating": 4.8,
            "estimated_visit_duration": "2 hours",
            "travel_tips": "Photography requires a separate ticket.",
            "nearby_attractions": [
                {
                    "name": "Kumbhalgarh Fort",
                    "category": "Fort",
                    "distance": "33 km",
                    "travel_time": "1 hour",
                    "description": "Historic fort with the second longest wall in the world."
                }
            ],
            "festivals": [
                {
                    "festival_name": "Mahavir Janma Kalyanak",
                    "month": "April",
                    "importance": "High",
                    "duration": "1 day",
                    "crowd_level": "High",
                    "estimated_visitors": 10000
                }
            ]
        }
    }
]

# Apply helper to add repetitive but complete details
for place in places:
    lat = place["dest"]["latitude"]
    lon = place["dest"]["longitude"]
    name = place["dest"]["name"]
    state = place["dest"]["state"]
    city = place["dest"]["city"]
    
    helper = get_helper_info(name, state, city, lat, lon)
    place["dest"]["travel_information"] = helper["travel_information"]
    place["dest"]["weather"] = helper["weather"]
    place["dest"]["accommodation"] = helper["accommodation"]
    place["dest"]["food"] = helper["food"]

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Group destinations by religion/region/state
for p in places:
    r_name = p["religion_name"]
    reg_name = p["region_name"]
    st_name = p["state_name"]
    destination = p["dest"]
    
    # find or create religion
    rel = next((r for r in data["religions"] if r["name"] == r_name), None)
    if not rel:
        rel = {"name": r_name, "regions": []}
        data["religions"].append(rel)
        
    # find or create region
    reg = next((r for r in rel["regions"] if r["region"] == reg_name), None)
    if not reg:
        reg = {"region": reg_name, "states": []}
        rel["regions"].append(reg)
        
    # find or create state
    st = next((s for s in reg["states"] if s["state"] == st_name), None)
    if not st:
        st = {"state": st_name, "destinations": []}
        reg["states"].append(st)
        
    # add destination
    st["destinations"].append(destination)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Added 10 places successfully!")
