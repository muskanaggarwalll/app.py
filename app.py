
import streamlit as st
from datetime import date, timedelta

# ============================================================
# WANDERNEST - TRAVEL PLANNING APPLICATION
# Compatible with Windows, macOS and Streamlit Cloud
# ============================================================

st.set_page_config(
    page_title="WanderNest",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# 1. DESTINATION DATA
# ------------------------------------------------------------

DESTINATIONS = {
    "Goa": {
        "region": "Coastal Escape",
        "description": "Golden beaches, sunset cafes and relaxed coastal days.",
        "food": 900,
        "activities": 1200,
        "hotel_multiplier": 1.00,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1000&q=80",
        "best_for": "Beaches, friends and sunsets",
        "itinerary": [
            "Visit a beach and explore a local market.",
            "Enjoy waterfront sightseeing and cafe time.",
            "Watch the sunset and relax in the evening.",
        ],
    },
    "Manali": {
        "region": "Mountain Retreat",
        "description": "Pine forests, mountain views and cosy cafes.",
        "food": 750,
        "activities": 1400,
        "hotel_multiplier": 1.05,
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1000&q=80",
        "best_for": "Mountains, nature and adventure",
        "itinerary": [
            "Explore the town and riverside.",
            "Visit mountain viewpoints and local cafes.",
            "Enjoy a nature walk and souvenir shopping.",
        ],
    },
    "Jaipur": {
        "region": "Heritage and Culture",
        "description": "Historic architecture, pink streets and colourful bazaars.",
        "food": 700,
        "activities": 1100,
        "hotel_multiplier": 0.95,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1000&q=80",
        "best_for": "History, architecture and shopping",
        "itinerary": [
            "Explore the old city and local bazaar.",
            "Visit heritage landmarks and gardens.",
            "Try local food and shop for souvenirs.",
        ],
    },
    "Kerala": {
        "region": "Nature and Backwaters",
        "description": "Lush greenery, peaceful waterways and tropical landscapes.",
        "food": 800,
        "activities": 1500,
        "hotel_multiplier": 1.10,
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1000&q=80",
        "best_for": "Nature, slow travel and scenic stays",
        "itinerary": [
            "Explore the local area and gardens.",
            "Enjoy a backwater or nature experience.",
            "Visit a local market and relax.",
        ],
    },
    "Shimla": {
        "region": "Classic Hill Station",
        "description": "Mountain air, historic streets and scenic walks.",
        "food": 700,
        "activities": 1000,
        "hotel_multiplier": 0.90,
        "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1000&q=80",
        "best_for": "Cool weather, walks and weekend breaks",
        "itinerary": [
            "Walk along the main promenade.",
            "Discover viewpoints and nearby nature.",
            "Enjoy a relaxed cafe stop before departure.",
        ],
    },
}

# Sample prices in Indian rupees.
# These are estimates for demonstration purposes only.
BASE_HOTEL_PRICE = 2500
TRANSPORT_PER_PERSON = 1800

# ------------------------------------------------------------
# 2. WEBSITE DESIGN
# ------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    .stApp {
        background-color: #f6f8f7;
        color: #102a43;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #102a43 !important;
    }

    h1, h2 {
        font-family: 'Playfair Display', Georgia, serif !important;
    }

    p, label, li {
        font-family: 'DM Sans', Arial, sans-serif;
    }

    .brand {
        font-size: 1.2rem;
        letter-spacing: 0.12em;
        font-weight: 700;
        color: #087e8b;
        margin-bottom: 1.2rem;
    }

    .hero {
        padding: 3rem 2rem;
        border-radius: 22px;
        color: white;
        background:
            linear-gradient(100deg, rgba(10,35,55,0.92), rgba(10,67,78,0.65)),
            url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1600&q=85');
        background-size: cover;
        background-position: center;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: white !important;
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 3rem;
        line-height: 1.1;
        margin: 0.5rem 0 1rem 0;
    }

    .hero p {
        color: #f0fdfa;
        font-size: 1rem;
        max-width: 600px;
    }

    .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.15em;
        font-size: 0.8rem;
        font-weight: 700;
        color: #9ee8dc;
    }

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e3ece9;
        padding: 1rem;
        border-radius: 12px;
    }

    div.stButton > button {
        background-color: #087e8b;
        color: white;
        border-radius: 9px;
        border: none;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #065d68;
        color: white;
    }

    hr {
        border-color: #dce8e4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# 3. HEADER
# ------------------------------------------------------------

st.markdown(
    '<div class="brand">✈ WANDERNEST</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Your journey begins here</div>
        <h1>Find your next<br>beautiful escape.</h1>
        <p>
            Discover destinations, plan your itinerary and estimate
            your travel budget with WanderNest.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write(
    "Welcome to WanderNest, your simple travel-planning companion. "
    "Choose a destination, customise your trip and create a travel plan."
)

# ------------------------------------------------------------
# 4. DESTINATION EXPLORER
# ------------------------------------------------------------

st.header("01 - Explore Destinations")

destination = st.selectbox(
    "Choose your destination",
    list(DESTINATIONS.keys()),
)

place = DESTINATIONS[destination]

left, right = st.columns([1.15, 1])

with left:
    st.image(
        place["image"],
        caption="Discover " + destination,
        use_container_width=True,
    )

with right:
    st.subheader(destination)
    st.caption(place["region"])
    st.write(place["description"])
    st.write("**Best for:** " + place["best_for"])
    st.divider()

    st.write("**Estimated daily costs per person**")
    st.write("Food: Rs. {:,}".format(place["food"]))
    st.write("Activities: Rs. {:,}".format(place["activities"]))

    hotel_estimate = int(
        BASE_HOTEL_PRICE * place["hotel_multiplier"]
    )
    st.write(
        "Hotel: Rs. {:,} per room per night".format(hotel_estimate)
    )

# ------------------------------------------------------------
# 5. TRIP PLANNER
# ------------------------------------------------------------

st.divider()
st.header("02 - Plan Your Trip")

today = date.today()
default_start = today + timedelta(days=7)
default_end = default_start + timedelta(days=3)

col1, col2 = st.columns(2)

with col1:
    traveller_name = st.text_input(
        "Lead traveller name",
        placeholder="Enter your name",
    )

    start_date = st.date_input(
        "Departure date",
        value=default_start,
        min_value=today,
        key="departure_date",
    )

with col2:
    travellers = st.number_input(
        "Number of travellers",
        min_value=1,
        max_value=20,
        value=2,
        step=1,
    )

    end_date = st.date_input(
        "Return date",
        value=default_end,
        min_value=today,
        key="return_date",
    )

room_count = st.number_input(
    "Number of hotel rooms",
    min_value=1,
    max_value=10,
    value=1,
    step=1,
)

travel_style = st.selectbox(
    "Choose your travel style",
    ["Budget", "Comfort", "Premium"],
)

style_multipliers = {
    "Budget": 0.75,
    "Comfort": 1.00,
    "Premium": 1.75,
}

style_multiplier = style_multipliers[travel_style]

# ------------------------------------------------------------
# 6. BUDGET CALCULATOR
# ------------------------------------------------------------

st.divider()
st.header("03 - Estimate Your Travel Budget")

valid_dates = end_date > start_date

if valid_dates:
    nights = (end_date - start_date).days
else:
    nights = 0
    st.warning(
        "Your return date must be later than your departure date."
    )

days = max(nights, 1)

hotel_per_room = int(
    BASE_HOTEL_PRICE
    * place["hotel_multiplier"]
    * style_multiplier
)

hotel_cost = hotel_per_room * nights * int(room_count)

food_cost = (
    place["food"] * days * int(travellers)
)

activity_cost = (
    place["activities"] * days * int(travellers)
)

transport_cost = (
    TRANSPORT_PER_PERSON * int(travellers)
)

estimated_total = (
    hotel_cost
    + food_cost
    + activity_cost
    + transport_cost
)

per_person = estimated_total // int(travellers)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Estimated Trip Total",
        "Rs. {:,}".format(estimated_total),
    )

with metric2:
    st.metric(
        "Estimated Cost Per Person",
        "Rs. {:,}".format(per_person),
    )

with metric3:
    st.metric(
        "Trip Duration",
        "{} nights".format(nights),
    )

st.caption(
    "These are illustrative estimates, not live booking prices. "
    "Actual costs may vary depending on dates and availability."
)

with st.expander("View Detailed Budget Breakdown"):
    st.write("Destination: " + destination)
    st.write("Travel style: " + travel_style)
    st.write("Travellers: {}".format(int(travellers)))
    st.write("Hotel rooms: {}".format(int(room_count)))
    st.write("Hotel cost: Rs. {:,}".format(hotel_cost))
    st.write("Food estimate: Rs. {:,}".format(food_cost))
    st.write("Activities estimate: Rs. {:,}".format(activity_cost))
    st.write("Transport estimate: Rs. {:,}".format(transport_cost))
    st.divider()
    st.subheader(
        "Total estimated budget: Rs. {:,}".format(estimated_total)
    )

# ------------------------------------------------------------
# 7. ITINERARY
# ------------------------------------------------------------

st.divider()
st.header("04 - Your Suggested Itinerary")

st.write(
    "Here is a sample itinerary for your trip to " + destination + "."
)

for index, activity in enumerate(place["itinerary"], start=1):
    st.markdown("**Day {}**".format(index))
    st.write(activity)

st.info(
    "This is a suggested sample itinerary. Check local opening hours, "
    "weather conditions and transport arrangements before travelling."
)

# ------------------------------------------------------------
# 8. DOWNLOAD TRIP SUMMARY
# ------------------------------------------------------------

st.divider()
st.header("05 - Save Your Trip Plan")

itinerary_text = "\n".join(
    "Day {}: {}".format(index, activity)
    for index, activity in enumerate(place["itinerary"], start=1)
)

summary = """
WANDERNEST
YOUR TRIP SUMMARY
========================================

Lead traveller: {name}
Destination: {destination}
Travel style: {style}
Departure date: {departure}
Return date: {return_date}
Duration: {nights} nights
Number of travellers: {travellers}
Number of hotel rooms: {rooms}

ESTIMATED BUDGET
----------------------------------------
Hotel: Rs. {hotel:,}
Food: Rs. {food:,}
Activities: Rs. {activities:,}
Transport: Rs. {transport:,}

TOTAL ESTIMATED COST: Rs. {total:,}
Estimated cost per person: Rs. {per_person:,}

SUGGESTED ITINERARY
----------------------------------------
{itinerary}

IMPORTANT NOTE
----------------------------------------
Prices are illustrative estimates, not live quotes.
WanderNest does not make actual travel bookings.
Verify prices and arrangements before booking.
""".format(
    name=traveller_name if traveller_name else "Not provided",
    destination=destination,
    style=travel_style,
    departure=start_date.strftime("%d %B %Y"),
    return_date=end_date.strftime("%d %B %Y"),
    nights=nights,
    travellers=int(travellers),
    rooms=int(room_count),
    hotel=hotel_cost,
    food=food_cost,
    activities=activity_cost,
    transport=transport_cost,
    total=estimated_total,
    per_person=per_person,
    itinerary=itinerary_text,
)

if valid_dates:
    st.download_button(
        label="Download My WanderNest Trip Plan",
        data=summary,
        file_name="WanderNest_Trip_Plan.txt",
        mime="text/plain",
        use_container_width=True,
    )
else:
    st.button(
        "Download My WanderNest Trip Plan",
        disabled=True,
        use_container_width=True,
    )

# ------------------------------------------------------------
# 9. FOOTER
# ------------------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:1.5rem 0;">
        <p style="color:#087e8b; font-size:1.15rem;
                  font-weight:700; letter-spacing:0.12em;">
            WANDERNEST
        </p>
        <p style="color:#526777; font-size:0.95rem;">
            Discover more. Plan better. Travel beautifully.
        </p>
        <p style="color:#718096; font-size:0.8rem;">
            Python Programming Project | Illustrative travel estimates
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
