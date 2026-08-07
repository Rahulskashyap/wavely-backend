# news_v4/regions.py


# =========================================================
# INDIAN STATES + UNION TERRITORIES
# =========================================================

INDIAN_STATES_UTS = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",

    # Union Territories
    "Andaman and Nicobar Islands",
    "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Lakshadweep",
    "Puducherry",
]


# =========================================================
# STATE / UT LOCATION KEYWORDS
# =========================================================
#
# These aliases help Wavely determine the state of a story
# from its canonical English title/summary.
#
# Keep terms geographically meaningful. Avoid overly broad
# words that can occur in unrelated international stories.
# =========================================================

STATE_KEYWORDS = {

    # =====================================================
    # SOUTH INDIA
    # =====================================================

    "Andhra Pradesh": [
        "andhra pradesh",
        "andhra",
        "amaravati",
        "visakhapatnam",
        "vizag",
        "vijayawada",
        "tirupati",
        "guntur",
        "nellore",
        "kurnool",
        "rajahmundry",
        "rajahmahendravaram",
        "kakinada",
        "anantapur",
        "kadapa",
        "chittoor",
        "ongole",
        "srikakulam",
        "vizianagaram",
    ],

    "Karnataka": [
        "karnataka",
        "bengaluru",
        "bangalore",
        "mysuru",
        "mysore",
        "mangaluru",
        "mangalore",
        "hubballi",
        "hubli",
        "dharwad",
        "belagavi",
        "belgaum",
        "ballari",
        "bellary",
        "gadag",
        "tumakuru",
        "tumkur",
        "shivamogga",
        "shimoga",
        "davanagere",
        "kalaburagi",
        "gulbarga",
        "udupi",
        "hassan",
        "mandya",
        "bidar",
        "raichur",
        "koppal",
        "vijayapura",
        "bijapur",
        "chikkamagaluru",
        "chikmagalur",
        "chitradurga",
        "kodagu",
        "coorg",
        "ramanagara",
        "kolar",
        "chikkaballapur",
        "yadgir",
        "bagalkot",
        "haveri",
        "uttara kannada",
        "dakshina kannada",
        "chamarajanagar",
    ],

    "Kerala": [
        "kerala",
        "thiruvananthapuram",
        "trivandrum",
        "kochi",
        "cochin",
        "kozhikode",
        "calicut",
        "thrissur",
        "kollam",
        "alappuzha",
        "alleppey",
        "kottayam",
        "palakkad",
        "malappuram",
        "kannur",
        "kasaragod",
        "wayanad",
        "idukki",
        "pathanamthitta",
    ],

    "Tamil Nadu": [
        "tamil nadu",
        "chennai",
        "coimbatore",
        "madurai",
        "tiruchirappalli",
        "trichy",
        "salem",
        "tirunelveli",
        "vellore",
        "erode",
        "thoothukudi",
        "tuticorin",
        "thanjavur",
        "dindigul",
        "tiruppur",
        "kanchipuram",
        "cuddalore",
        "kanyakumari",
    ],

    "Telangana": [
        "telangana",
        "hyderabad",
        "warangal",
        "nizamabad",
        "karimnagar",
        "khammam",
        "nalgonda",
        "adilabad",
        "mahbubnagar",
        "siddipet",
        "medak",
    ],

    # =====================================================
    # WEST INDIA
    # =====================================================

    "Goa": [
        "goa",
        "panaji",
        "margao",
        "vasco da gama",
        "mapusa",
        "ponda",
    ],

    "Gujarat": [
        "gujarat",
        "ahmedabad",
        "surat",
        "vadodara",
        "rajkot",
        "gandhinagar",
        "bhavnagar",
        "jamnagar",
        "junagadh",
        "kutch",
        "kachchh",
        "anand",
        "bharuch",
        "porbandar",
    ],

    "Maharashtra": [
        "maharashtra",
        "mumbai",
        "pune",
        "nagpur",
        "nashik",
        "thane",
        "chhatrapati sambhajinagar",
        "aurangabad",
        "kolhapur",
        "solapur",
        "satara",
        "sangli",
        "amravati",
        "akola",
        "nanded",
        "latur",
        "jalgaon",
        "ratnagiri",
        "palghar",
        "navi mumbai",
    ],

    # =====================================================
    # NORTH INDIA
    # =====================================================

    "Haryana": [
        "haryana",
        "gurugram",
        "gurgaon",
        "faridabad",
        "panipat",
        "ambala",
        "rohtak",
        "hisar",
        "karnal",
        "sonipat",
        "panchkula",
        "kurukshetra",
    ],

    "Himachal Pradesh": [
        "himachal pradesh",
        "himachal",
        "shimla",
        "dharamshala",
        "manali",
        "kullu",
        "mandi",
        "solan",
        "kangra",
        "hamirpur",
    ],

    "Punjab": [
        "punjab",
        "chandigarh",
        "amritsar",
        "ludhiana",
        "jalandhar",
        "patiala",
        "bathinda",
        "mohali",
        "pathankot",
        "hoshiarpur",
    ],

    "Rajasthan": [
        "rajasthan",
        "jaipur",
        "jodhpur",
        "udaipur",
        "kota",
        "ajmer",
        "bikaner",
        "jaisalmer",
        "alwar",
        "bharatpur",
        "sikar",
        "barmer",
    ],

    "Uttar Pradesh": [
        "uttar pradesh",
        "lucknow",
        "noida",
        "greater noida",
        "kanpur",
        "varanasi",
        "agra",
        "prayagraj",
        "allahabad",
        "ayodhya",
        "ghaziabad",
        "meerut",
        "gorakhpur",
        "mathura",
        "bareilly",
        "aligarh",
        "jhansi",
        "moradabad",
    ],

    "Uttarakhand": [
        "uttarakhand",
        "dehradun",
        "haridwar",
        "rishikesh",
        "nainital",
        "haldwani",
        "mussoorie",
        "kedarnath",
        "badrinath",
        "chamoli",
        "rudraprayag",
    ],

    # =====================================================
    # CENTRAL INDIA
    # =====================================================

    "Chhattisgarh": [
        "chhattisgarh",
        "raipur",
        "bilaspur",
        "durg",
        "bhilai",
        "bastar",
        "jagdalpur",
        "korba",
        "raigarh",
        "ambikapur",
    ],

    "Madhya Pradesh": [
        "madhya pradesh",
        "bhopal",
        "indore",
        "jabalpur",
        "gwalior",
        "ujjain",
        "sagar",
        "rewa",
        "satna",
        "ratlam",
        "chhindwara",
    ],

    # =====================================================
    # EAST INDIA
    # =====================================================

    "Bihar": [
        "bihar",
        "patna",
        "gaya",
        "muzaffarpur",
        "bhagalpur",
        "darbhanga",
        "purnia",
        "nalanda",
        "begusarai",
        "arrah",
    ],

    "Jharkhand": [
        "jharkhand",
        "ranchi",
        "jamshedpur",
        "dhanbad",
        "bokaro",
        "deoghar",
        "hazaribagh",
        "giridih",
    ],

    "Odisha": [
        "odisha",
        "orissa",
        "bhubaneswar",
        "cuttack",
        "puri",
        "rourkela",
        "sambalpur",
        "berhampur",
        "balasore",
        "koraput",
    ],

    "West Bengal": [
        "west bengal",
        "bengal",
        "kolkata",
        "calcutta",
        "howrah",
        "siliguri",
        "durgapur",
        "asansol",
        "darjeeling",
        "malda",
        "murshidabad",
    ],

    # =====================================================
    # NORTH-EAST INDIA
    # =====================================================

    "Arunachal Pradesh": [
        "arunachal pradesh",
        "arunachal",
        "itanagar",
        "tawang",
        "pasighat",
        "ziro",
    ],

    "Assam": [
        "assam",
        "guwahati",
        "dispur",
        "dibrugarh",
        "silchar",
        "jorhat",
        "tezpur",
        "nagaon",
    ],

    "Manipur": [
        "manipur",
        "imphal",
        "churachandpur",
        "thoubal",
        "bishnupur",
    ],

    "Meghalaya": [
        "meghalaya",
        "shillong",
        "tura",
        "cherrapunji",
        "sohra",
    ],

    "Mizoram": [
        "mizoram",
        "aizawl",
        "lunglei",
        "champhai",
    ],

    "Nagaland": [
        "nagaland",
        "kohima",
        "dimapur",
        "mokokchung",
    ],

    "Sikkim": [
        "sikkim",
        "gangtok",
        "namchi",
        "gyalshing",
    ],

    "Tripura": [
        "tripura",
        "agartala",
        "udaipur tripura",
        "dharmanagar",
    ],

    # =====================================================
    # UNION TERRITORIES
    # =====================================================

    "Andaman and Nicobar Islands": [
        "andaman and nicobar islands",
        "andaman",
        "nicobar",
        "port blair",
        "sri vijaya puram",
    ],

    "Chandigarh": [
        "chandigarh",
    ],

    "Dadra and Nagar Haveli and Daman and Diu": [
        "dadra and nagar haveli",
        "daman and diu",
        "daman",
        "silvassa",
        "diu",
    ],

    "Delhi": [
        "delhi",
        "new delhi",
    ],

    "Jammu and Kashmir": [
        "jammu and kashmir",
        "jammu & kashmir",
        "j&k",
        "srinagar",
        "jammu",
        "anantnag",
        "baramulla",
        "pahalgam",
        "gulmarg",
    ],

    "Ladakh": [
        "ladakh",
        "leh",
        "kargil",
    ],

    "Lakshadweep": [
        "lakshadweep",
        "kavaratti",
        "agatti",
        "minicoy",
    ],

    "Puducherry": [
        "puducherry",
        "pondicherry",
        "karaikal",
        "yanam",
        "mahe",
    ],
}