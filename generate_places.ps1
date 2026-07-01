$jsonPath = "c:\Users\DMT\Documents\GitHub\Api\travel.json"
$travelData = Get-Content $jsonPath -Raw | ConvertFrom-Json

function New-Destination {
    param($id, $name, $altNames, $religion, $category, $subcategory, $state, $district, $city, $region, $lat, $lon, $elevation, $desc, $hist, $sig, $arch, $deity, $festName, $festMonth)

    $dest = [PSCustomObject]@{
        id = $id
        name = $name
        alternative_names = @($altNames)
        religion = $religion
        category = $category
        subcategory = $subcategory
        state = $state
        district = $district
        city = $city
        village = ""
        region = $region
        latitude = [double]$lat
        longitude = [double]$lon
        elevation = $elevation
        description = $desc
        history = $hist
        religious_significance = $sig
        architecture = $arch
        main_deity_or_revered_person = $deity
        established_year = "Ancient"
        founder = "Unknown"
        best_time_to_visit = "October to March"
        climate = "Varies"
        opening_time = "06:00"
        closing_time = "20:00"
        entry_fee = 0
        dress_code = "Modest clothing"
        photography_allowed = $false
        wheelchair_accessible = $true
        parking = $true
        food_available = $true
        locker = $true
        washroom = $true
        medical_facility = $true
        official_website = ""
        google_maps = "https://maps.google.com/?q=$lat,$lon"
        thumbnail = "https://api.example.com/images/default_thumb.jpg"
        banner = "https://api.example.com/images/default_banner.jpg"
        gallery = @("https://api.example.com/images/default_1.jpg")
        popularity_rating = 4.8
        estimated_visit_duration = "2 hours"
        travel_tips = "Respect the local customs and traditions."
        nearby_attractions = @(
            [PSCustomObject]@{
                name = "Local Market"
                category = "Market"
                distance = "2 km"
                travel_time = "10 mins"
                description = "Bustling local market near the shrine."
            }
        )
        festivals = @(
            [PSCustomObject]@{
                festival_name = $festName
                month = $festMonth
                importance = "High"
                duration = "1 day"
                crowd_level = "High"
                estimated_visitors = 50000
            }
        )
        travel_information = [PSCustomObject]@{
            from = "Delhi"
            routes = @()
            train_information = [PSCustomObject]@{
                train_name = "Express"
                train_number = "12345"
                departure_station = "New Delhi (NDLS)"
                arrival_station = "$city Jn"
                departure_time = "18:00"
                arrival_time = "08:00"
                duration = "14 hours"
                available_classes = @("2A", "3A", "SL")
                important_intermediate_stations = @("Major Stop")
                irctc_placeholder = "https://www.irctc.co.in/"
            }
            flight_information = [PSCustomObject]@{
                departure_airport = "Indira Gandhi International Airport (DEL)"
                arrival_airport = "Nearest Airport"
                airlines = @("IndiGo", "Air India")
                estimated_fare = 5000
                airport_to_destination_distance = 50
                airport_transfer_options = @("Taxi", "Bus")
            }
            bus_information = [PSCustomObject]@{
                government_bus = $true
                private_bus = $true
                volvo = $true
                sleeper = $true
                departure = "ISBT"
                arrival = "$city Bus Stand"
                major_stops = @("Midway Stop")
                fare = 1000
                booking_placeholder = "https://www.redbus.in/"
            }
        }
        weather = [PSCustomObject]@{
            summer = "30°C to 45°C"
            winter = "10°C to 25°C"
            monsoon = "25°C to 35°C, moderate rainfall"
            best_season = "Winter"
            snowfall = $false
        }
        accommodation = [PSCustomObject]@{
            hotel = $true
            dharamshala = $true
            ashram = $true
            guest_house = $true
            budget_range = "500 - 5000 INR"
            contact = "+91-0000000000"
            booking_placeholder = "https://booking.example.com"
        }
        food = [PSCustomObject]@{
            local_food = @("Thali", "Sweets")
            satvik_food = $true
            prasad = "Sweets/Fruits"
            restaurants = @("Local Dhaba")
        }
    }
    return $dest
}

$rawPlaces = @(
    # Bishnoi Places
    @("bsh-rj-001", "Mukam Mukti Dham", "Mukam Temple", "Bishnoi", "Temple", "Samadhi", "Rajasthan", "Bikaner", "Nokha", "North India", 27.6025, 73.2425, "250m", "The most sacred site of the Bishnoi sect, being the samadhi of Guru Jambheshwar.", "Established in 1536 when Guru Jambheshwar took samadhi.", "Holiest pilgrimage for the Bishnoi community.", "Traditional desert temple architecture.", "Guru Jambheshwar", "Phalgun Mela", "February"),
    @("bsh-rj-002", "Samrathal Dhora", "Samrathal", "Bishnoi", "Holy Sand Dune", "Origin Site", "Rajasthan", "Bikaner", "Bikaner", "North India", 27.6500, 73.3000, "260m", "The place where Guru Jambheshwar gave the 29 principles of the Bishnoi sect.", "Founded the Bishnoi sect here in 1485.", "The birthplace of the Bishnoi religion.", "Natural sand dune with a shrine.", "Guru Jambheshwar", "Jambheswar Fair", "October"),
    @("bsh-rj-003", "Pipasar", "Pipasar Temple", "Bishnoi", "Temple", "Birthplace", "Rajasthan", "Nagaur", "Nagaur", "North India", 27.2000, 73.7333, "300m", "The birthplace of Guru Jambheshwar, the founder of the Bishnoi sect.", "Guru Jambheshwar was born here in 1451.", "Highly revered as the birthplace of the founder.", "Traditional Rajasthani temple.", "Guru Jambheshwar", "Janmashtami", "August"),
    @("bsh-rj-004", "Jambholav", "Jambholav Temple", "Bishnoi", "Temple", "Sacred Site", "Rajasthan", "Jodhpur", "Phalodi", "North India", 27.1333, 72.3667, "250m", "A sacred place visited by Guru Jambheshwar.", "Associated with miracles performed by the Guru.", "Pilgrimage site for Bishnois.", "Traditional", "Guru Jambheshwar", "Mela", "March"),
    @("bsh-rj-005", "Rotu", "Rotu Dham", "Bishnoi", "Temple", "Sacred Site", "Rajasthan", "Nagaur", "Rotu", "North India", 27.3000, 73.5000, "280m", "Another prominent village associated with Guru Jambheshwar.", "The Guru spent time here preaching.", "Spiritual center for the community.", "Traditional", "Guru Jambheshwar", "Local Fair", "April"),
    @("bsh-up-001", "Lodipur", "Lodipur Bishnoi Mandir", "Bishnoi", "Temple", "Sacred Site", "Uttar Pradesh", "Moradabad", "Moradabad", "North India", 28.8386, 78.7733, "190m", "A significant Bishnoi temple in Uttar Pradesh.", "Built to serve the Bishnoi community in UP.", "Center for Bishnoi gatherings in the region.", "North Indian", "Guru Jambheshwar", "Jambheswar Jayanti", "August"),
    @("bsh-rj-006", "Lohawat", "Lohawat Dham", "Bishnoi", "Temple", "Sacred Site", "Rajasthan", "Jodhpur", "Lohawat", "North India", 26.9833, 72.5667, "260m", "A major town with strong Bishnoi heritage and temples.", "Historic site for the community.", "Revered site.", "Traditional", "Guru Jambheshwar", "Annual Fair", "September"),

    # Hindu Places (31)
    @("hnd-uk-002", "Mansa Devi Temple", "Bilwa Tirth", "Hindu", "Shakti Peeth", "Goddess Temple", "Uttarakhand", "Haridwar", "Haridwar", "North India", 29.9575, 78.1633, "315m", "A revered temple dedicated to Goddess Mansa Devi in the holy city of Haridwar.", "Ancient temple, modernized recently. Believed to fulfill wishes.", "Considered a highly powerful Shakti shrine.", "North Indian", "Goddess Mansa", "Navratri", "October"),
    @("hnd-uk-003", "Chandi Devi Temple", "Neel Parvat Teerth", "Hindu", "Shakti Peeth", "Goddess Temple", "Uttarakhand", "Haridwar", "Haridwar", "North India", 29.9329, 78.1818, "300m", "Temple dedicated to Goddess Chandi Devi atop the Neel Parvat.", "Established by Adi Shankaracharya in the 8th century.", "One of the Panch Tirths within Haridwar.", "North Indian", "Goddess Chandi", "Navratri", "April"),
    @("hnd-tn-002", "Ramanathaswamy Temple", "Rameswaram Temple", "Hindu", "Jyotirlinga", "Shiva Temple", "Tamil Nadu", "Ramanathapuram", "Rameswaram", "South India", 9.2881, 79.3174, "10m", "A Hindu temple dedicated to the god Shiva on Rameswaram island.", "Expanded by Pandya and Nayak kings.", "One of the 12 Jyotirlingas and Char Dham.", "Dravidian", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-gj-001", "Somnath Temple", "Deo Patan", "Hindu", "Jyotirlinga", "Shiva Temple", "Gujarat", "Gir Somnath", "Prabhas Patan", "West India", 20.8880, 70.4011, "0m", "First among the twelve Jyotirlinga shrines of Shiva.", "Reconstructed multiple times, most recently in 1951.", "Extremely sacred, symbolizes eternal faith.", "Chaulukya", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-ap-001", "Venkateswara Temple", "Tirupati Balaji", "Hindu", "Temple", "Vaishnav Temple", "Andhra Pradesh", "Tirupati", "Tirumala", "South India", 13.6833, 79.3473, "853m", "Dedicated to Venkateswara, a form of Vishnu.", "Built over centuries by Chola, Hoysala, and Vijayanagara empires.", "Most visited and richest Hindu temple.", "Dravidian", "Lord Venkateswara", "Brahmotsavam", "September"),
    @("hnd-mh-002", "Trimbakeshwar Temple", "Trimbak", "Hindu", "Jyotirlinga", "Shiva Temple", "Maharashtra", "Nashik", "Trimbak", "West India", 19.9322, 73.5310, "700m", "Ancient Hindu temple in the town of Trimbak.", "Built by Peshwa Balaji Baji Rao.", "Source of the Godavari river, Jyotirlinga site.", "Hemadpanthi", "Lord Shiva", "Kumbh Mela", "August"),
    @("hnd-mh-003", "Bhimashankar Temple", "Bhimashankar", "Hindu", "Jyotirlinga", "Shiva Temple", "Maharashtra", "Pune", "Bhimashankar", "West India", 19.0720, 73.5350, "900m", "Jyotirlinga shrine located in the Sahyadri hills.", "Ancient temple, structured by Nana Phadnavis in 18th Century.", "One of the 12 Jyotirlingas.", "Nagara", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-mh-004", "Grishneshwar Temple", "Dhushmeshwar", "Hindu", "Jyotirlinga", "Shiva Temple", "Maharashtra", "Aurangabad", "Verul", "West India", 20.0247, 75.1706, "600m", "The last or 12th Jyotirlinga on the earth.", "Rebuilt by Ahilyabai Holkar in the 18th century.", "Important Shiva pilgrimage.", "Maratha", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-gj-002", "Nageshvara Jyotirlinga", "Nagnath", "Hindu", "Jyotirlinga", "Shiva Temple", "Gujarat", "Devbhumi Dwarka", "Dwarka", "West India", 22.3340, 69.0125, "15m", "One of the 12 Jyotirlinga shrines.", "Mentioned in the Shiva Purana.", "Believed to protect from all poisons.", "Modern Hindu", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-uk-004", "Kedarnath Temple", "Kedar Khand", "Hindu", "Jyotirlinga", "Shiva Temple", "Uttarakhand", "Rudraprayag", "Kedarnath", "North India", 30.7352, 79.0669, "3583m", "One of the most revered temple destinations of India.", "Built by Pandavas, revived by Adi Shankaracharya.", "Panch Kedar, Chota Char Dham.", "Katyuri", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-mp-001", "Mahakaleshwar Temple", "Mahakal", "Hindu", "Jyotirlinga", "Shiva Temple", "Madhya Pradesh", "Ujjain", "Ujjain", "Central India", 23.1827, 75.7682, "490m", "Fierce form of Shiva, faces south (Dakshinamurti).", "Ancient, current structure built by Marathas.", "The only Jyotirlinga facing south.", "Maratha/Bhumija", "Lord Mahakal", "Maha Shivaratri", "February"),
    @("hnd-mp-002", "Omkareshwar Temple", "Omkar", "Hindu", "Jyotirlinga", "Shiva Temple", "Madhya Pradesh", "Khandwa", "Omkareshwar", "Central India", 22.2452, 76.1472, "200m", "Situated on an island shaped like the symbol Om.", "Ancient origins on the Narmada river.", "One of the 12 Jyotirlingas.", "Nagara", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-ap-002", "Mallikarjuna Temple", "Srisailam", "Hindu", "Jyotirlinga", "Shiva Temple", "Andhra Pradesh", "Nandyal", "Srisailam", "South India", 16.0734, 78.8687, "400m", "Both a Jyotirlinga and a Shakti Peetha.", "Built by Vijayanagara empire.", "Highly revered dual holy site.", "Dravidian", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-jh-001", "Baidyanath Temple", "Baba Baidyanath Dham", "Hindu", "Jyotirlinga", "Shiva Temple", "Jharkhand", "Deoghar", "Deoghar", "East India", 24.4925, 86.6999, "250m", "Complex of 22 temples around the main Shiva temple.", "Ancient, linked to Ravana.", "Jyotirlinga and Shakti Peetha.", "Lotus shaped", "Lord Shiva", "Shravan Mela", "July"),
    @("hnd-gj-003", "Dwarkadhish Temple", "Jagat Mandir", "Hindu", "Char Dham", "Vaishnav Temple", "Gujarat", "Devbhumi Dwarka", "Dwarka", "West India", 22.2377, 68.9674, "0m", "Dedicated to Lord Krishna, the King of Dwarka.", "Original temple built by Vajranabha, Krishna's grandson.", "Part of the Char Dham.", "Chaulukya", "Lord Krishna", "Janmashtami", "August"),
    @("hnd-uk-005", "Gangotri Temple", "Gangotri", "Hindu", "Chota Char Dham", "Goddess Temple", "Uttarakhand", "Uttarkashi", "Gangotri", "North India", 30.9947, 78.9398, "3100m", "Highest temple dedicated to Goddess Ganga.", "Built by Amar Singh Thapa in the 18th century.", "Origin of the holy river Ganges.", "Katyuri", "Goddess Ganga", "Ganga Dussehra", "May"),
    @("hnd-uk-006", "Yamunotri Temple", "Yamunotri", "Hindu", "Chota Char Dham", "Goddess Temple", "Uttarakhand", "Uttarkashi", "Yamunotri", "North India", 31.0140, 78.4600, "3293m", "Source of the Yamuna River and the seat of Goddess Yamuna.", "Built by Maharaja Pratap Shah of Tehri Garhwal.", "First stop in Chota Char Dham.", "North Indian", "Goddess Yamuna", "Akshaya Tritiya", "April"),
    @("hnd-jk-001", "Vaishno Devi", "Mata Rani", "Hindu", "Temple", "Goddess Temple", "Jammu and Kashmir", "Reasi", "Katra", "North India", 33.0298, 74.9490, "1585m", "Cave temple dedicated to Vaishnavi.", "Ancient cave, discovered over 700 years ago by Pandit Shridhar.", "One of the most visited pilgrimage centers.", "Cave Shrine", "Goddess Vaishno Devi", "Navratri", "October"),
    @("hnd-kl-001", "Sabarimala Temple", "Ayyappan Temple", "Hindu", "Temple", "Ayyappan Temple", "Kerala", "Pathanamthitta", "Sabarimala", "South India", 9.4402, 77.0811, "468m", "Located amidst 18 hills, dedicated to Lord Ayyappan.", "Ancient temple, related to Prince Manikanthan of Pandalam.", "Largest annual pilgrimage in the world.", "Kerala Style", "Lord Ayyappan", "Makara Vilakku", "January"),
    @("hnd-up-002", "Banke Bihari Temple", "Vrindavan Temple", "Hindu", "Temple", "Krishna Temple", "Uttar Pradesh", "Mathura", "Vrindavan", "North India", 27.5806, 77.6985, "170m", "Dedicated to Lord Krishna, famous for its unique darshan.", "Established by Swami Haridas in 1864.", "Most popular temple in Vrindavan.", "Rajasthani", "Lord Krishna", "Janmashtami", "August"),
    @("hnd-tn-003", "Brihadisvara Temple", "Rajarajesvaram", "Hindu", "Temple", "Shiva Temple", "Tamil Nadu", "Thanjavur", "Thanjavur", "South India", 10.7828, 79.1318, "88m", "One of the largest South Indian temples, a UNESCO World Heritage site.", "Built by Chola emperor Rajaraja I in 1010 CE.", "Pinnacle of Chola architecture.", "Dravidian", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-tn-004", "Sri Ranganathaswamy Temple", "Srirangam", "Hindu", "Temple", "Vaishnav Temple", "Tamil Nadu", "Tiruchirappalli", "Srirangam", "South India", 10.8624, 78.6872, "70m", "Dedicated to Ranganatha, a reclining form of Vishnu.", "Built from the 9th to 16th centuries.", "Largest functioning Hindu temple in the world.", "Dravidian", "Lord Ranganatha", "Vaikuntha Ekadashi", "December"),
    @("hnd-od-002", "Lingaraj Temple", "Ekamra Kshetra", "Hindu", "Temple", "Shiva Temple", "Odisha", "Khordha", "Bhubaneswar", "East India", 20.2382, 85.8339, "45m", "Oldest and largest temple in Bhubaneswar.", "Built by King Jajati Keshari in the 11th century.", "Represents Harihara, a combined form of Shiva and Vishnu.", "Kalinga", "Lord Harihara", "Ashokashtami", "April"),
    @("hnd-as-001", "Kamakhya Temple", "Kamakhya Peetha", "Hindu", "Shakti Peeth", "Goddess Temple", "Assam", "Kamrup Metropolitan", "Guwahati", "Northeast India", 26.1672, 91.7061, "170m", "One of the oldest of the 51 Shakti Pithas.", "Rebuilt in 1565 by Chilarai.", "Celebrates the bleeding goddess, highly sacred to Tantric Hinduism.", "Nilachal type", "Goddess Kamakhya", "Ambubachi Mela", "June"),
    @("hnd-wb-001", "Dakshineswar Kali Temple", "Dakshineswar", "Hindu", "Temple", "Goddess Temple", "West Bengal", "North 24 Parganas", "Kolkata", "East India", 22.6548, 88.3572, "10m", "Dedicated to Bhavatarini, an aspect of Kali.", "Built in 1855 by Rani Rashmoni.", "Associated with Ramakrishna Paramahamsa.", "Navaratna", "Goddess Kali", "Kali Puja", "October"),
    @("hnd-ka-001", "Virupaksha Temple", "Hampi Temple", "Hindu", "Temple", "Shiva Temple", "Karnataka", "Vijayanagara", "Hampi", "South India", 15.3350, 76.4600, "400m", "Part of the Group of Monuments at Hampi.", "Built in the 7th century, expanded by Vijayanagara empire.", "Uninterrupted worship since the 7th century.", "Dravidian", "Lord Shiva", "Maha Shivaratri", "February"),
    @("hnd-ka-002", "Sri Krishna Temple", "Udupi Krishna", "Hindu", "Temple", "Krishna Temple", "Karnataka", "Udupi", "Udupi", "South India", 13.3418, 74.7473, "15m", "Famous for the Kanakana Kindi, a window through which Krishna is worshipped.", "Founded by Madhvacharya in the 13th century.", "Center of Dvaita philosophy.", "Kerala Style", "Lord Krishna", "Paryaya", "January"),
    @("hnd-rj-001", "Brahma Temple", "Pushkar Temple", "Hindu", "Temple", "Brahma Temple", "Rajasthan", "Ajmer", "Pushkar", "North India", 26.4866, 74.5513, "510m", "One of very few existing temples dedicated to the Hindu creator-god Brahma.", "Current structure dates to the 14th century.", "Most prominent Brahma temple in the world.", "North Indian", "Lord Brahma", "Kartik Purnima", "November"),
    @("hnd-rj-002", "Karni Mata Temple", "Rat Temple", "Hindu", "Temple", "Goddess Temple", "Rajasthan", "Bikaner", "Deshnoke", "North India", 27.7951, 73.3424, "278m", "Famous for the approximately 25,000 black rats that live, and are revered, in the temple.", "Completed by Maharaja Ganga Singh.", "Unique reverence of rats (Kabbas).", "Mughal and Rajput", "Karni Mata", "Navratri", "October"),
    @("hnd-hp-001", "Jwala Ji Temple", "Jwala Devi", "Hindu", "Shakti Peeth", "Goddess Temple", "Himachal Pradesh", "Kangra", "Jwalamukhi", "North India", 31.8752, 76.3218, "600m", "Dedicated to Jwala Devi, the presiding deity in the form of a flaming mouth.", "Ancient, visited by Akbar.", "One of the 51 Shakti Peethas without an idol, only natural flames.", "North Indian", "Goddess Jwala", "Navratri", "October"),
    @("hnd-hr-001", "Mata Mansa Devi Temple", "Panchkula Mansa Devi", "Hindu", "Shakti Peeth", "Goddess Temple", "Haryana", "Panchkula", "Panchkula", "North India", 30.7259, 76.8837, "350m", "A prominent Hindu temple dedicated to Goddess Mansa Devi.", "Built by Maharaja Gopal Singh of Manimajra in 1811-1815.", "Highly revered Shakti shrine.", "North Indian", "Goddess Mansa", "Navratri", "October")
)

# Convert places into structured object array
$allNewDestinations = @()
foreach ($p in $rawPlaces) {
    $allNewDestinations += New-Destination -id $p[0] -name $p[1] -altNames $p[2] -religion $p[3] -category $p[4] -subcategory $p[5] -state $p[6] -district $p[7] -city $p[8] -region $p[9] -lat $p[10] -lon $p[11] -elevation $p[12] -desc $p[13] -hist $p[14] -sig $p[15] -arch $p[16] -deity $p[17] -festName $p[18] -festMonth $p[19]
}

# Add Bishnoi as a new religion if not exists
$bishnoiRel = $travelData.religions | Where-Object { $_.name -eq "Bishnoi" }
if (-not $bishnoiRel) {
    $bishnoiRel = [PSCustomObject]@{ name = "Bishnoi"; regions = @() }
    $travelData.religions += $bishnoiRel
}

foreach ($dest in $allNewDestinations) {
    $relName = $dest.religion
    $regName = $dest.region
    $stName = $dest.state

    # find or create religion
    $rel = $travelData.religions | Where-Object { $_.name -eq $relName }
    if (-not $rel) {
        $rel = [PSCustomObject]@{ name = $relName; regions = @() }
        $travelData.religions += $rel
    }

    # find or create region
    $reg = $rel.regions | Where-Object { $_.region -eq $regName }
    if (-not $reg) {
        $reg = [PSCustomObject]@{ region = $regName; states = @() }
        $rel.regions += $reg
    }

    # find or create state
    $st = $reg.states | Where-Object { $_.state -eq $stName }
    if (-not $st) {
        $st = [PSCustomObject]@{ state = $stName; destinations = @() }
        $reg.states += $st
    }

    $st.destinations += $dest
}

$travelData | ConvertTo-Json -Depth 100 | Set-Content "c:\Users\DMT\Documents\GitHub\Api\travel.json" -Encoding UTF8

