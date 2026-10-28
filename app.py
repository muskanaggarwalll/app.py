
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
    st.markdown("**Estimated daily costs per person**")
    st.write(f"🍽️ Food: ₹{place['food']:,}")
    st.write(f"🎟️ Activities: ₹{place['activities']:,}")
    st.write(f"🏨 Hotel: ₹{place['hotel']:,} per room/night")
    st.write(f"🚆 Transport estimate: ₹{place['transport']:,} per person")

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
# 5. DESTINATION QUICK BROWSE
# ------------------------------------------------------------

destination_columns = st.columns(len(DESTINATIONS))

for column, (name, details) in zip(
    destination_columns,
    DESTINATIONS.items(),
):
    with column:
        st.image(details["image"], use_container_width=True)
        st.markdown(f"**{name}**")
        st.caption(details["region"])
if st.button(
    f"Explore {name}",
    key=f"explore_{name}",
    use_container_width=True,
):
    st.session_state["selected_destination"] = name
    st.rerun()

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

manual_location = st.text_input(
    "Starting city or location (optional)",
    placeholder="Example: Delhi, India",
    help="Enter a city or area to help personalise your trip plan.",
)

if manual_location.strip():
    maps_url = (
        "https://www.google.com/maps/search/?api=1&query="
        + quote(manual_location.strip())
    )
    st.markdown(f"[View this location on Google Maps]({maps_url})")

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
        max_value=20,
        value=2,
        step=1,
        key="number_of_adults",
    )

    kids = st.number_input(
        "Number of kids",
        min_value=0,
        max_value=20,
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
    max_value=10,
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
    st.write(f"**Hotel estimate:** ₹{hotel_cost:,}")
    st.write(f"**Food estimate:** ₹{food_cost:,}")
    st.write(f"**Activities estimate:** ₹{activity_cost:,}")
    st.write(f"**Transport estimate:** ₹{transport_cost:,}")
    st.divider()
    st.subheader(f"Estimated total: ₹{estimated_total:,}")

st.caption(
    "All prices are illustrative estimates. They are not live prices or booking "
    "quotes. Actual costs may differ by season, availability and personal choices."
)

# ------------------------------------------------------------
# 10. SUGGESTED ITINERARY
# ------------------------------------------------------------

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
