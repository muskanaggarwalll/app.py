
import streamlit as st
import streamlit.components.v1 as components
from datetime import date, timedelta
from urllib.parse import quote
import csv
import io
import html

# ============================================================
# WANDERNEST | TRAVEL PLANNING APPLICATION
# Python + Streamlit
# Designed for Windows, macOS and Streamlit Community Cloud
# ============================================================

st.set_page_config(
    page_title="WanderNest | Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- WANDERNEST NAVIGATION BAR ----------

nav_style = """
<style>
.wn-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 18px 24px;
    margin-bottom: 30px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
    font-family: sans-serif;
}

.wn-brand {
    color: #087e8b;
    font-size: 23px;
    font-weight: 800;
    white-space: nowrap;
}

.wn-navlinks {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 26px;
    flex-wrap: wrap;
}

.wn-navlinks a {
    color: #334155 !important;
    text-decoration: none !important;
    font-size: 15px;
    font-weight: 600;
}

.wn-navlinks .wn-cta {
    background: #087e8b;
    color: white !important;
    padding: 12px 18px;
    border-radius: 10px;
}

@media (max-width: 700px) {
    .wn-nav {
        flex-direction: column;
        align-items: flex-start;
    }

    .wn-navlinks {
        justify-content: flex-start;
        gap: 15px;
    }
}
</style>
"""

st.markdown(nav_style, unsafe_allow_html=True)

st.markdown(
    """
    <div class="wn-nav">
        <div class="wn-brand">✈ WANDERNEST</div>
        <div class="wn-navlinks">
            <a href="#discover">Discover</a>
            <a href="#plan">Plan</a>
            <a href="#budget">Budget</a>
            <a href="#offers">Offers</a>
            <a class="wn-cta" href="#plan">Plan a trip →</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
# ------------------------------------------------------------
# 1. DESTINATION DATABASE
# Sample prices are estimates, not live travel quotes.
# ------------------------------------------------------------

DESTINATIONS = {
    "Goa": {
        "region": "Coastal Escape",
        "description": "Golden beaches, sunset cafés, coastal drives and relaxed days.",
        "food": 900,
        "activities": 1200,
        "hotel": 2500,
        "transport": 1800,
        "best_for": "Beaches, friends, nightlife and sunsets",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=85",
        "itinerary": [
            ("Day 1", "Beach walk, explore the local market and enjoy a sunset."),
            ("Day 2", "Discover coastal viewpoints, cafés and sightseeing spots."),
            ("Day 3", "Enjoy a relaxed morning, souvenir shopping and departure."),
        ],
    },
    "Manali": {
        "region": "Mountain Retreat",
        "description": "Pine forests, mountain views, riverside walks and cosy cafés.",
        "food": 750,
        "activities": 1400,
        "hotel": 2700,
        "transport": 2400,
        "best_for": "Mountains, nature, adventure and winter escapes",
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=85",
        "itinerary": [
            ("Day 1", "Explore the town, riverside and local cafés."),
            ("Day 2", "Visit mountain viewpoints and enjoy a nature excursion."),
            ("Day 3", "Take a leisurely walk and shop for souvenirs."),
        ],
    },
    "Jaipur": {
        "region": "Heritage and Culture",
        "description": "Historic architecture, pink-hued streets and colourful bazaars.",
        "food": 700,
        "activities": 1100,
        "hotel": 2300,
        "transport": 1600,
        "best_for": "History, architecture, culture and shopping",
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1200&q=85",
        "itinerary": [
            ("Day 1", "Explore the old city, markets and local food."),
            ("Day 2", "Visit heritage landmarks, forts and gardens."),
            ("Day 3", "Enjoy shopping, photography and a relaxed departure."),
        ],
    },
    "Kerala": {
        "region": "Nature and Backwaters",
        "description": "Lush greenery, peaceful waterways and tropical landscapes.",
        "food": 800,
        "activities": 1500,
        "hotel": 3200,
        "transport": 2200,
        "best_for": "Nature, scenic stays, backwaters and slow travel",
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=85",
        "itinerary": [
            ("Day 1", "Explore the local area, gardens and waterfront."),
            ("Day 2", "Enjoy a backwater experience or nature excursion."),
            ("Day 3", "Visit a local market and enjoy a relaxed morning."),
        ],
    },
    "Shimla": {
        "region": "Classic Hill Station",
        "description": "Mountain air, scenic walks, charming streets and cafés.",
        "food": 700,
        "activities": 1000,
        "hotel": 2200,
        "transport": 1900,
        "best_for": "Cool weather, mountain views and weekend breaks",
        "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=85",
        "itinerary": [
            ("Day 1", "Walk along the main promenade and explore local cafés."),
            ("Day 2", "Discover viewpoints and nearby nature spots."),
            ("Day 3", "Enjoy a relaxed breakfast and souvenir shopping."),
        ],
    },
}

TRAVEL_STYLES = {
    "Budget": 0.75,
    "Comfort": 1.00,
    "Premium": 1.75,
}

# ------------------------------------------------------------
# 2. WEBSITE DESIGN
# ------------------------------------------------------------

st.markdown(
    """
        <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --navy: #102a43;
        --teal: #087e8b;
        --mint: #dff4ef;
        --cream: #f6f8f7;
        --muted: #526777;
    }

    .stApp {
        background: var(--cream);
        color: var(--navy);
    }

    .block-container {
        max-width: 1220px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--navy) !important;
    }

    h1, h2 {
        font-family: 'Playfair Display', Georgia, serif !important;
    }

    p, label, li {
        font-family: 'DM Sans', Arial, sans-serif;
    }

    .brand {
        font-size: 1.15rem;
        letter-spacing: .13em;
        font-weight: 700;
        color: var(--teal);
        margin: 0.2rem 0 1rem 0;
    }

    .hero {
        padding: 3.2rem 2.5rem;
        border-radius: 24px;
        color: white;
        background:
            linear-gradient(100deg, rgba(10,35,55,.93), rgba(10,67,78,.62)),
            url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1800&q=85');
        background-size: cover;
        background-position: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 15px 40px rgba(16,42,67,.12);
        margin-bottom: 1.4rem;
    }

    .hero h1 {
        color: white !important;
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: clamp(2.3rem, 5vw, 4rem);
        line-height: 1.08;
        margin: .5rem 0 1rem 0;
    }

    .hero p {
        color: #f0fdfa;
        font-size: 1.04rem;
        max-width: 650px;
    }

    .eyebrow {
        text-transform: uppercase;
        letter-spacing: .17em;
        font-size: .78rem;
        font-weight: 700;
        color: #9ee8dc;
    }

    .section-note {
        color: var(--muted);
        font-size: .94rem;
    }

    .destination-card {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #e0eae6;
        margin-bottom: 1rem;
    }

    div.stButton > button {
        background: var(--teal);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: .55rem .9rem;
    }

    div.stButton > button:hover {
        background: #065d68;
        color: white;
        border: none;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e0eae6;
        padding: 1rem;
        border-radius: 14px;
    }

    [data-testid="stSidebar"] {
        background: #edf6f3;
    }

    hr {
        border-color: #dce8e4;
    }

    @media (max-width: 700px) {
        .hero {
            padding: 2rem 1.3rem;
            min-height: 260px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 3. HEADER AND NAVIGATION
# ------------------------------------------------------------

st.markdown(
    '<div class="brand">✈ WANDERNEST</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Find your next beautiful escape</div>
        <h1>Travel more.<br>Plan beautifully.</h1>
        <p>
            Discover destinations, plan your stay, explore suggested
            itineraries and estimate your travel budget in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Welcome to WanderNest, your travel-planning companion. "
    "Choose where you want to go and create a trip plan that suits you."
)

st.markdown(
    """
    <div class="section-note">
        DESTINATIONS &nbsp; • &nbsp; TRIP PLANNER &nbsp; • &nbsp;
        BUDGET ESTIMATOR &nbsp; • &nbsp; TRAVEL ITINERARY
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 4. DESTINATION EXPLORER
# ------------------------------------------------------------

st.divider()
st.header("01 · Explore destinations")

destination = st.selectbox(
    "Choose your destination",
    options=list(DESTINATIONS.keys()),
    key="destination",
)

place = DESTINATIONS[destination]

image_col, info_col = st.columns([1.15, 1])

with image_col:
    st.image(
        place["image"],
        caption=f"Explore {destination}",
        use_container_width=True,
    )

with info_col:
    st.subheader(destination)
    st.caption(place["region"])
    st.write(place["description"])
    st.markdown(f"**Best for:** {place['best_for']}")
    st.divider()
    

# ------------------------------------------------------------
# 5. MANALI ATTRACTIONS

if destination == "Manali":
    st.divider()
    st.header("🏔️ Explore Manali Attractions")
    st.write("Select the places you want to visit during your trip.")

    manali_attractions = [
        "Hidimba Devi Temple",
        "Solang Valley",
        "Old Manali",
        "Atal Tunnel & Sissu",
        "Jogini Waterfall",
        "Vashisht Village & Hot Springs",
        "Mall Road",
        "Naggar Castle",
    ]

    selected_attractions = []

    for attraction in manali_attractions:
        if st.checkbox(attraction, key=f"manali_{attraction}"):
            selected_attractions.append(attraction)

    st.session_state["selected_manali_attractions"] = selected_attractions
    
# 4A. GOA ATTRACTIONS

if destination == "Goa":
    st.divider()
    st.header("🏖️ Explore Goa Attractions")
    st.write("Select the places you want to visit during your trip.")

    goa_attractions = [
        "Baga Beach & Calangute Beach",
        "Fort Aguada",
        "Chapora Fort",
        "Anjuna Beach",
        "Fontainhas (Panaji)",
        "Palolem Beach",
        "Agonda Beach",
        "Cabo de Rama Fort",
        "Cola Beach",
        "Basilica of Bom Jesus",
        "Se Cathedral",
        "Dudhsagar Falls",
    ]

    selected_goa_attractions = []

    for attraction in goa_attractions:
        if st.checkbox(attraction, key=f"goa_{attraction}"):
            selected_goa_attractions.append(attraction)

    st.session_state["selected_goa_attractions"] = selected_goa_attractions

# 4B. SHIMLA ATTRACTIONS

if destination == "Shimla":
    st.divider()
    st.header("🏔️ Explore Shimla Attractions")
    st.write("Select the places you want to visit during your trip.")

    shimla_attractions = {
        "In the Heart of the City": [
            {
                "name": "The Ridge & Mall Road",
                "description": "The central hub of Shimla featuring an open-air promenade with panoramic mountain views and a vehicle-free shopping street lined with cafes and handicraft shops."
            },
            {
                "name": "Christ Church",
                "description": "A prominent neo-Gothic landmark built in 1857, located on The Ridge and known for its stained-glass windows and clock tower."
            },
            {
                "name": "Jakhu Temple & Jakhu Ropeway",
                "description": "An ancient Hanuman temple perched on Shimla's highest peak, accessible via a scenic ropeway ride."
            },
            {
                "name": "Viceregal Lodge (Rashtrapati Niwas)",
                "description": "A grand Scottish-Baronial estate from 1888 surrounded by manicured English gardens, where important pre-independence discussions took place."
            },
            {
                "name": "Lakkar Bazaar",
                "description": "A traditional wooden crafts market near The Ridge, famous for wooden toys, walking sticks, and local souvenirs."
            }
        ],
        "Nature & Nearby Excursions": [
            {
                "name": "Kufri",
                "description": "A nearby hill station featuring the Himalayan Nature Park, Kufri Fun World, and seasonal snow activities."
            },
            {
                "name": "Chadwick Falls",
                "description": "A waterfall tucked inside a dense deodar and oak forest, offering a peaceful nature walk."
            },
            {
                "name": "Green Valley",
                "description": "A scenic mountain pass on the way to Kufri, known for its rolling pine forests and photography spots."
            },
            {
                "name": "Kalka-Shimla Toy Train",
                "description": "A historic UNESCO-listed narrow-gauge railway journey passing through tunnels and dramatic mountain viaducts."
            }
        ]
    }

    selected_shimla_attractions = []

    for category, attractions in shimla_attractions.items():
        st.subheader(category)

        for attraction in attractions:
            with st.container(border=True):
                st.markdown(f"### {attraction['name']}")
                st.write(attraction["description"])

                if st.checkbox(
                    f"Add {attraction['name']} to my trip",
                    key=f"shimla_{attraction['name']}"
                ):
                    selected_shimla_attractions.append(attraction["name"])

    st.session_state["selected_shimla_attractions"] = selected_shimla_attractions

# 4C. JAIPUR ATTRACTIONS

if destination == "Jaipur":
    st.divider()
    st.header("🏰 Explore Jaipur Attractions")
    st.write("Select the places you want to visit during your trip.")

    jaipur_attractions = [
        {
            "name": "Amber Palace (Amer Fort)",
            "description": "A majestic 16th-century hilltop fortress combining Rajput and Mughal styles, featuring the glittering Sheesh Mahal and sweeping views of Maota Lake."
        },
        {
            "name": "Hawa Mahal (Palace of Winds)",
            "description": "An iconic five-storey honeycomb facade with 953 intricate jharokhas, built in 1799 so royal women could observe street life unseen."
        },
        {
            "name": "City Palace",
            "description": "A sprawling royal residence blending Mughal and Rajput architecture, housing the Maharaja Sawai Man Singh II Museum and beautiful courtyards."
        },
        {
            "name": "Jantar Mantar",
            "description": "A UNESCO World Heritage Site featuring 19 massive stone astronomical instruments built in the 18th century to track celestial bodies."
        },
        {
            "name": "Nahargarh Fort",
            "description": "Perched on the Aravalli hills, this fort is renowned for its panoramic sunset views over the Pink City."
        },
        {
            "name": "Jal Mahal",
            "description": "A picturesque Water Palace sitting in the middle of Man Sagar Lake, best viewed from the lakeside promenade."
        },
        {
            "name": "Albert Hall Museum",
            "description": "Rajasthan's oldest museum, located in Ram Niwas Garden, showcasing arts, artefacts, and striking Indo-Saracenic architecture."
        },
        {
            "name": "Patrika Gate",
            "description": "A vibrant, hand-painted architectural gateway at Jawahar Circle Garden, popular for colourful photography."
        }
    ]

    selected_jaipur_attractions = []

    for attraction in jaipur_attractions:
        with st.container(border=True):
            st.markdown(f"### {attraction['name']}")
            st.write(attraction["description"])

            if st.checkbox(
                f"Add {attraction['name']} to my trip",
                key=f"jaipur_{attraction['name']}"
            ):
                selected_jaipur_attractions.append(attraction["name"])

    st.session_state["selected_jaipur_attractions"] = selected_jaipur_attractions

# 4D. KERALA ATTRACTIONS

if destination == "Kerala":
    st.divider()
    st.header("🌴 Explore Kerala Attractions")
    st.write("Select the places you want to visit during your trip.")

    kerala_attractions = {
        "Hill Stations": [
            {
                "name": "Munnar",
                "description": "Famous for rolling tea plantations, crisp mountain air, and Eravikulam National Park, home to the endangered Nilgiri Tahr."
            },
            {
                "name": "Wayanad",
                "description": "Known for spice and cardamom plantations, Chembra Peak, and the prehistoric rock carvings of Edakkal Caves."
            },
            {
                "name": "Vagamon",
                "description": "A quiet retreat featuring rolling green meadows and the triple-hill landscape of Kurisumala, Thangal, and Murugan."
            }
        ],
        "Backwaters & Lakes": [
            {
                "name": "Alleppey (Alappuzha)",
                "description": "Widely called the Venice of the East, famous for overnight houseboat cruises through the tranquil backwaters of Kuttanad."
            },
            {
                "name": "Kumarakom",
                "description": "Located around Vembanad Lake and ideal for bird watching at the Kumarakom Bird Sanctuary."
            },
            {
                "name": "Munroe Island",
                "description": "A network of narrow canals where freshwater meets saltwater, offering peaceful canoe tours."
            }
        ],
        "Beaches & Coastal Spots": [
            {
                "name": "Varkala",
                "description": "Famous for dramatic red sandstone cliffs overlooking the Arabian Sea and nearby Edava Beach."
            },
            {
                "name": "Kovalam",
                "description": "A coastal destination known for crescent-shaped beaches, including Lighthouse Beach."
            },
            {
                "name": "Marari Beach",
                "description": "A relaxed, uncrowded stretch of golden sand near Alleppey."
            }
        ],
        "Wildlife & Waterfalls": [
            {
                "name": "Thekkady",
                "description": "Famous for boat safaris across Periyar Lake, where visitors may spot wild elephants, gaurs, and birds."
            },
            {
                "name": "Athirappilly Waterfalls",
                "description": "An impressive waterfall with an approximately 80-foot cascade surrounded by dense rainforest, often called the Niagara of India."
            }
        ],
        "Heritage & Culture": [
            {
                "name": "Kochi (Cochin)",
                "description": "A historic port city featuring Fort Kochi, the iconic Chinese Fishing Nets, Mattancherry Palace, and the Paradesi Synagogue."
            }
        ]
    }

    selected_kerala_attractions = []

    for category, attractions in kerala_attractions.items():
        st.subheader(category)

        for attraction in attractions:
            with st.container(border=True):
                st.markdown(f"### {attraction['name']}")
                st.write(attraction["description"])

                if st.checkbox(
                    f"Add {attraction['name']} to my trip",
                    key=f"kerala_{attraction['name']}"
                ):
                    selected_kerala_attractions.append(attraction["name"])

    st.session_state["selected_kerala_attractions"] = selected_kerala_attractions

# 5. DESTINATION QUICK BROWSE
# ------------------------------------------------------------
st.subheader("Explore all five destinations")
destination_columns = st.columns(len(DESTINATIONS))

for column, (name, details) in zip(
    destination_columns,
    DESTINATIONS.items(),
):
    with column:
        st.image(details["image"], use_container_width=True)
        st.markdown(f"**{name}**")
        st.caption(details["region"])


# ------------------------------------------------------------
# 6. OPTIONAL LOCATION ACCESS
# ------------------------------------------------------------

st.divider()
st.header("02 · Location assistance")

st.write(
    "You can use your browser's location permission to view your approximate "
    "coordinates. Location access is optional and is not required to plan a trip."
)

with st.expander("Use my current browser location"):
    st.caption(
        "Your browser may ask for permission. Location access usually requires "
        "HTTPS or localhost. If permission is denied or unsupported, continue "
        "using the manual location field below."
    )

    components.html(
        """
        <div style="font-family:Arial,sans-serif; color:#102a43;">
            <button id="locate"
                style="background:#087e8b;color:white;border:0;border-radius:8px;
                padding:10px 14px;cursor:pointer;font-weight:bold;">
                Find my location
            </button>
            <p id="status" style="font-size:14px;margin-top:12px;">
                Location has not been requested.
            </p>
            <p id="coords" style="font-size:14px;"></p>
            <script>
                const button = document.getElementById("locate");
                const status = document.getElementById("status");
                const coords = document.getElementById("coords");

                button.addEventListener("click", function() {
                    coords.textContent = "";

                    if (!navigator.geolocation) {
                        status.textContent =
                            "Geolocation is not supported by this browser.";
                        return;
                    }

                    status.textContent =
                        "Requesting location permission...";

                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;

                            status.textContent = "Location found.";
                            coords.textContent =
                                "Latitude: " + lat.toFixed(6) +
                                " | Longitude: " + lon.toFixed(6);
                        },
                        function(error) {
                            const messages = {
                                1: "Permission denied. You can allow location in browser settings.",
                                2: "Location information is unavailable.",
                                3: "Location request timed out."
                            };
                            status.textContent =
                                messages[error.code] ||
                                "Unable to retrieve location.";
                        },
                        {
                            enableHighAccuracy: false,
                            timeout: 10000,
                            maximumAge: 60000
                        }
                    );
                });
            </script>
        </div>
        """,
        height=150,
    )


# ------------------------------------------------------------
# 7. TRIP PLANNER
# ------------------------------------------------------------

st.divider()
st.header("03 · Plan your trip")

today = date.today()
default_start = today + timedelta(days=7)
default_end = default_start + timedelta(days=3)

planner_left, planner_right = st.columns(2)

with planner_left:
    traveller_name = st.text_input(
        "Lead traveller name",
        placeholder="Enter your name",
    )

    start_date = st.date_input(
        "Departure date",
        value=default_start,
        min_value=today,
        key="start_date",
    )

with planner_right:
    adults = st.number_input(
        "Number of adults",
        min_value=1,
        max_value=50,
        value=2,
        step=1,
        key="number_of_adults",
    )

    kids = st.number_input(
        "Number of kids",
        min_value=0,
        max_value=50,
        value=0,
        step=1,
        key="number_of_kids",
    )

    travellers = adults + kids

    st.caption(
        f"Total travellers: {travellers} "
        f"({adults} adults, {kids} kids)"
    )

    end_date = st.date_input(
        "Return date",
        value=default_end,
        min_value=today,
        key="end_date",
    )

room_count = st.number_input(
    "Number of hotel rooms",
    min_value=1,
    max_value=200,
    value=1,
    step=1,
)

travel_style = st.radio(
    "Choose your travel style",
    options=["Budget", "Comfort", "Premium"],
    horizontal=True,
)

style_multiplier = TRAVEL_STYLES[travel_style]

# ------------------------------------------------------------
# 8. OPTIONAL TRAVEL PREFERENCES
# ------------------------------------------------------------

st.subheader("Personalise your trip")

preference_options = [
    "Nature",
    "Food",
    "Shopping",
    "Adventure",
    "Culture",
    "Relaxation",
    "Photography",
]

preferences = st.multiselect(
    "What would you like to include?",
    options=preference_options,
    default=["Nature", "Food"],
)

special_requests = st.text_area(
    "Additional preferences (optional)",
    placeholder="Example: family-friendly places, cafés, scenic walks...",
    max_chars=500,
)

# ------------------------------------------------------------
# 9. TRAVEL BUDGET CALCULATOR
# ------------------------------------------------------------

st.divider()
st.header("04 · Estimate your travel budget")

valid_dates = end_date > start_date

if not valid_dates:
    st.error("Your return date must be after your departure date.")
    nights = 0
else:
    nights = (end_date - start_date).days

days = max(nights, 1)
traveller_count = int(travellers)
room_total = int(room_count)

hotel_per_room = int(
    place["hotel"] * style_multiplier
)

hotel_cost = hotel_per_room * nights * room_total
food_cost = place["food"] * days * traveller_count
activity_cost = place["activities"] * days * traveller_count
transport_cost = place["transport"] * traveller_count

estimated_total = (
    hotel_cost
    + food_cost
    + activity_cost
    + transport_cost
)

per_person = estimated_total // traveller_count

budget_col1, budget_col2, budget_col3 = st.columns(3)

with budget_col1:
    st.metric(
        "Estimated trip total",
        f"₹{estimated_total:,}",
    )

with budget_col2:
    st.metric(
        "Estimated per person",
        f"₹{per_person:,}",
    )

with budget_col3:
    st.metric(
        "Trip duration",
        f"{nights} nights",
    )

with st.expander("View detailed budget breakdown"):
    st.write(f"**Destination:** {destination}")
    st.write(f"**Travel style:** {travel_style}")
    st.write(f"**Travellers:** {traveller_count}")
    st.write(f"**Hotel rooms:** {room_total}")

    st.divider()
    st.markdown("### Estimated daily costs per person")

    place = DESTINATIONS[destination]

    st.write(f"🍽️ Food: ₹{place['food']:,}")
    st.write(f"🎟️ Activities: ₹{place['activities']:,}")
    st.write(f"🏨 Hotel: ₹{place['hotel']:,} per room/night")
    st.write(f"🚆 Transport: ₹{place['transport']:,} per person")

    st.divider()
    st.write(f"**Hotel estimate:** ₹{hotel_cost:,}")
    st.write(f"**Food estimate:** ₹{food_cost:,}")
    st.write(f"**Activities estimate:** ₹{activity_cost:,}")
    st.write(f"**Transport estimate:** ₹{transport_cost:,}")

    st.subheader(f"Estimated total: ₹{estimated_total:,}")

st.caption(
    "All prices are illustrative estimates. They are not live prices or booking "
    "quotes. Actual costs may differ by season, availability and personal choices."
)

# ------------------------------------------------------------
# 10. SUGGESTED ITINERARY
# ------------------------------------------------------------
# ==========================================
# 04A. OFFERS & SPECIAL DEALS
# ==========================================

st.divider()

st.header("🎁 Offers & Special Deals")

st.write(
    "Discover exciting travel experiences and request "
    "a personalised offer for your next adventure!"
)
# ---------- DISCOUNT COUPON CARDS ----------

offer1, offer2, offer3 = st.columns(3)

offers = [
    {
        "title": "🌴 Beach Escapes",
        "destination": "Goa & Kerala",
        "original": 15000,
        "discount": 20,
        "coupon": "BEACH20",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=700&q=80"
    },
    {
        "title": "🏔️ Mountain Getaways",
        "destination": "Manali & Shimla",
        "original": 18000,
        "discount": 25,
        "coupon": "MOUNTAIN25",
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=700&q=80"
    },
    {
        "title": "🏰 Cultural Adventures",
        "destination": "Jaipur & more",
        "original": 12000,
        "discount": 20,
        "coupon": "CULTURE20",
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=700&q=80"
    }
]

columns = [offer1, offer2, offer3]

for index, offer in enumerate(offers):

    final_price = round(
        offer["original"] * (1 - offer["discount"] / 100)
    )

    with columns[index]:

        st.image(
            offer["image"],
            use_container_width=True
        )

        st.subheader(offer["title"])
        st.caption(offer["destination"])

                # Display coupon prices using Streamlit elements
        # so HTML tags do not appear as visible text.
        with st.container(border=True):

            st.caption(
                f"Original Price: ~~₹{offer['original']:,}~~"
            )

            st.markdown(f"## ₹{final_price:,}")

            st.markdown(
                f"**:green[{offer['discount']}% OFF]**"
            )

            st.write(
                "Coupon Code:",
                f"`{offer['coupon']}`"
            )
        st.caption("Illustrative price per person.")

        if st.button(
            f"Apply {offer['coupon']}",
            key=f"coupon_{index}",
            use_container_width=True
        ):
            st.session_state["selected_coupon"] = offer["coupon"]
            st.session_state["selected_offer_price"] = final_price
            st.session_state["selected_destination"] = offer["destination"]

            st.success(
                f"Coupon {offer['coupon']} selected successfully!"
            )

# ---------- SELECTED DEAL ----------

if "selected_coupon" in st.session_state:

    st.markdown("---")
    st.subheader("🎟️ Your Selected Deal")

    st.write(
        f"**Destination:** "
        f"{st.session_state['selected_destination']}"
    )

    st.write(
        f"**Coupon Code:** "
        f"`{st.session_state['selected_coupon']}`"
    )

    st.write(
        f"**Discounted Price:** "
        f"₹{st.session_state['selected_offer_price']:,}"
    )

    st.info(
        "These are demonstration prices, not verified travel quotes. "
        "Selecting a coupon does not confirm a booking."
    )

st.markdown("---")


# ==========================================
# END OF OFFERS & SPECIAL DEALS
# ==========================================
st.divider()
st.header("05 · Your suggested itinerary")

st.write(
    f"Here is a sample itinerary for your trip to {destination}."
)

for index, (day_label, activity) in enumerate(
    place["itinerary"],
    start=1,
):
    with st.container(border=True):
        st.markdown(f"**{day_label}**")
        st.write(activity)

if preferences:
    st.markdown("**Your interests**")
    st.write(", ".join(preferences))

if special_requests.strip():
    st.markdown("**Additional preferences**")
    st.write(special_requests.strip())

st.info(
    "The itinerary is a sample suggestion, not a confirmed tour. "
    "Check local opening hours, weather conditions and transport availability "
    "before travelling."
)

# ------------------------------------------------------------
# 11. MAP SEARCH
# ------------------------------------------------------------

st.divider()
st.header("06 · Explore your destination on a map")

manual_location = st.text_input(
    "Starting city or location (optional)",
    placeholder="Example: Delhi, India",
    help="Enter your starting city to get directions to your destination.",
    key="map_starting_location",
)

if manual_location.strip():
    maps_url = (
        "https://www.google.com/maps/dir/"
        + quote(manual_location.strip())
        + "/"
        + quote(destination)
    )
    st.markdown(
        f"[Get directions from {manual_location} to {destination} on Google Maps ↗]({maps_url})"
    )
else:
    maps_url = (
        "https://www.google.com/maps/search/?api=1&query="
        + quote(destination)
    )
    st.markdown(
        f"[Explore {destination} on Google Maps ↗]({maps_url})"
    )

map_url = (
    "https://www.google.com/maps/search/?api=1&query="
    + quote(destination + ", India")
)

st.markdown(
    f"[Open {destination} in Google Maps ↗]({map_url})"
)

if manual_location.strip():
    route_url = (
        "https://www.google.com/maps/dir/?api=1&origin="
        + quote(manual_location.strip())
        + "&destination="
        + quote(destination + ", India")
    )
    st.markdown(
        f"[View directions from your starting location to {destination} ↗]"
        f"({route_url})"
    )

# ------------------------------------------------------------
# 12. DOWNLOAD TRIP PLAN
# ------------------------------------------------------------

st.divider()
st.header("07 · Save your WanderNest trip plan")

itinerary_text = "\n".join(
    f"{day_label}: {activity}"
    for day_label, activity in place["itinerary"]
)

summary = f"""
WANDERNEST
TRAVEL PLAN
==================================================

TRAVELLER DETAILS
--------------------------------------------------
Lead traveller: {traveller_name.strip() or 'Not provided'}
Starting location: {manual_location.strip() or 'Not provided'}
Destination: {destination}
Travel style: {travel_style}
Departure date: {start_date.strftime('%d %B %Y')}
Return date: {end_date.strftime('%d %B %Y')}
Duration: {nights} nights
Number of travellers: {traveller_count}
Number of hotel rooms: {room_total}

TRAVEL PREFERENCES
--------------------------------------------------
{', '.join(preferences) if preferences else 'No preferences selected'}

Additional requests:
{special_requests.strip() or 'None provided'}

ESTIMATED BUDGET
--------------------------------------------------
Hotel: ₹{hotel_cost:,}
Food: ₹{food_cost:,}
Activities: ₹{activity_cost:,}
Transport: ₹{transport_cost:,}

TOTAL ESTIMATED COST: ₹{estimated_total:,}
Estimated cost per person: ₹{per_person:,}

SUGGESTED ITINERARY
--------------------------------------------------
{itinerary_text}

IMPORTANT INFORMATION
--------------------------------------------------
WanderNest is a travel-planning demonstration application.
Prices are illustrative estimates, not live booking quotes.
No flights, hotels or activities are booked by this application.
Please verify all travel arrangements and prices before booking.
"""

if valid_dates:
    safe_destination = "".join(
        character if character.isalnum() else "_"
        for character in destination
    )

    st.download_button(
        label="⬇ Download my WanderNest trip plan",
        data=summary,
        file_name=f"WanderNest_{safe_destination}_Trip.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.button(
        "⬇ Download my WanderNest trip plan",
        disabled=True,
        use_container_width=True,
    )

# ------------------------------------------------------------
# 13. DOWNLOAD BUDGET AS CSV
# ------------------------------------------------------------

st.subheader("Download budget spreadsheet")

budget_rows = [
    ["Category", "Estimated Amount (INR)"],
    ["Destination", destination],
    ["Travel style", travel_style],
    ["Hotel", hotel_cost],
    ["Food", food_cost],
    ["Activities", activity_cost],
    ["Transport", transport_cost],
    ["Total", estimated_total],
    ["Per person", per_person],
]

csv_buffer = io.StringIO()
csv_writer = csv.writer(csv_buffer)
csv_writer.writerows(budget_rows)

st.download_button(
    label="⬇ Download budget as CSV",
    data=csv_buffer.getvalue(),
    file_name="WanderNest_Budget.csv",
    mime="text/csv",
    use_container_width=True,
)

# ------------------------------------------------------------
# 14. FOOTER
# ------------------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:1.5rem 0;">
        <p style="color:#087e8b; font-size:1.2rem;
                  font-weight:700; letter-spacing:.13em;">
            ✈ WANDERNEST
        </p>
        <p style="color:#526777; font-size:.95rem;">
            Discover more. Plan better. Travel beautifully.
        </p>
        <p style="color:#718096; font-size:.8rem;">
            Python Programming Project · Illustrative travel estimates
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
