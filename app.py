
import streamlit as st
import pandas as pd
from io import StringIO
from urllib.parse import quote
from datetime import date, timedelta

# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="WanderNest | Discover Your Next Journey",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# 2. BRAND COLOURS
# ==========================================================

TEAL_BLUE = "#167D8D"
ROYAL_BLUE = "#3155C6"
IVORY_WHITE = "#FFFEF7"
MUSTARD_YELLOW = "#E5B83F"
DARK_TEXT = "#17333D"
PALE_TEAL = "#E8F5F4"
PALE_BLUE = "#EEF1FF"
BORDER = "#DCE7E5"
WHITE = "#FFFFFF"

# ==========================================================
# 3. DESTINATION DATABASE
# ==========================================================

DESTINATIONS = {
    "Goa": {
        "state": "Goa",
        "lat": 15.2993,
        "lon": 74.1240,
        "description": "Golden beaches, coastal cafés, sunsets and vibrant markets.",
        "best_for": "Beach lovers, food and relaxation",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=80",
        "activities": [
            "Morning: Relax at a beach and enjoy a coastal breakfast.",
            "Afternoon: Explore Old Goa, local markets and Portuguese heritage.",
            "Evening: Watch the sunset and enjoy a seaside dinner."
        ],
        "places": [
            "Baga Beach",
            "Fort Aguada",
            "Old Goa",
            "Fontainhas"
        ]
    },
    "Manali": {
        "state": "Himachal Pradesh",
        "lat": 32.2432,
        "lon": 77.1892,
        "description": "Mountain scenery, pine forests, cafés and Himalayan adventures.",
        "best_for": "Nature, adventure and mountain escapes",
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=80",
        "activities": [
            "Morning: Explore Old Manali and enjoy a mountain-view breakfast.",
            "Afternoon: Visit Hadimba Temple and nearby forest trails.",
            "Evening: Relax at a café and enjoy the mountain scenery."
        ],
        "places": [
            "Hadimba Temple",
            "Old Manali",
            "Solang Valley",
            "Mall Road"
        ]
    },
    "Jaipur": {
        "state": "Rajasthan",
        "lat": 26.9124,
        "lon": 75.7873,
        "description": "Royal palaces, pink architecture, handicrafts and Rajasthani cuisine.",
        "best_for": "Culture, architecture and shopping",
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1200&q=80",
        "activities": [
            "Morning: Visit Amber Fort and admire its historic architecture.",
            "Afternoon: Explore City Palace and Hawa Mahal.",
            "Evening: Shop for handicrafts and try traditional Rajasthani food."
        ],
        "places": [
            "Amber Fort",
            "Hawa Mahal",
            "City Palace",
            "Jantar Mantar"
        ]
    },
    "Kerala": {
        "state": "Kerala",
        "lat": 10.8505,
        "lon": 76.2711,
        "description": "Lush landscapes, peaceful backwaters, tea gardens and coastal escapes.",
        "best_for": "Nature, wellness and scenic holidays",
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=80",
        "activities": [
            "Morning: Enjoy a relaxed breakfast surrounded by greenery.",
            "Afternoon: Explore local nature spots or a backwater experience.",
            "Evening: Try Kerala cuisine and enjoy a peaceful sunset."
        ],
        "places": [
            "Alleppey Backwaters",
            "Munnar",
            "Fort Kochi",
            "Periyar"
        ]
    },
    "Shimla": {
        "state": "Himachal Pradesh",
        "lat": 31.1048,
        "lon": 77.1734,
        "description": "Colonial architecture, pine-covered hills and scenic mountain walks.",
        "best_for": "Couples, families and quiet mountain trips",
        "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=80",
        "activities": [
            "Morning: Walk along Mall Road and enjoy a warm breakfast.",
            "Afternoon: Visit historic landmarks and scenic viewpoints.",
            "Evening: Explore local cafés and enjoy the mountain atmosphere."
        ],
        "places": [
            "The Ridge",
            "Mall Road",
            "Jakhoo Temple",
            "Kufri"
        ]
    }
}

# ==========================================================
# 4. CUSTOM CSS
# ==========================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {IVORY_WHITE};
        color: {DARK_TEXT};
    }}

    [data-testid="stSidebar"] {{
        background-color: {PALE_TEAL};
        border-right: 1px solid {BORDER};
    }}

    .hero {{
        background: linear-gradient(
            120deg, {TEAL_BLUE}, {ROYAL_BLUE}
        );
        padding: 34px;
        border-radius: 22px;
        color: white;
        margin-bottom: 22px;
    }}

    .hero h1 {{
        color: white;
        font-size: 42px;
        margin-bottom: 8px;
    }}

    .hero p {{
        color: #F3F7FF;
        font-size: 17px;
    }}

    .eyebrow {{
        text-transform: uppercase;
        letter-spacing: 2px;
        color: {MUSTARD_YELLOW};
        font-size: 12px;
        font-weight: bold;
    }}

    .section-title {{
        color: {TEAL_BLUE};
        font-size: 25px;
        font-weight: 750;
        margin-top: 14px;
        margin-bottom: 10px;
    }}

    .info-card {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 18px;
        margin: 8px 0;
    }}

    .mustard-card {{
        background-color: #FFF5D5;
        border-left: 5px solid {MUSTARD_YELLOW};
        padding: 16px;
        border-radius: 12px;
    }}

    .teal-card {{
        background-color: {PALE_TEAL};
        border-left: 5px solid {TEAL_BLUE};
        padding: 16px;
        border-radius: 12px;
    }}

    div.stButton > button {{
        background-color: {TEAL_BLUE};
        color: white;
        border: 0;
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
    }}

    div.stButton > button:hover {{
        background-color: {ROYAL_BLUE};
        color: white;
    }}

    div[data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid {BORDER};
        padding: 14px;
        border-radius: 14px;
    }}

    h1, h2, h3 {{
        color: {DARK_TEXT};
    }}

    a {{
        color: {ROYAL_BLUE};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# 5. SESSION STATE
# ==========================================================

if "trip_plan" not in st.session_state:
    st.session_state["trip_plan"] = None

if "budget_result" not in st.session_state:
    st.session_state["budget_result"] = None

# ==========================================================
# 6. SIDEBAR NAVIGATION
# ==========================================================

with st.sidebar:
    st.markdown("# ✈️ WanderNest")
    st.caption("Find your place in the world.")
    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Home",
            "Explore Destinations",
            "Trip Planner",
            "Maps & Routes",
            "Cost Dashboard",
            "Package Comparison",
            "Download Trip Plan",
            "About WanderNest"
        ]
    )

    st.divider()
    st.markdown("### Our signature colours")

    st.markdown(
        f"""
        <div style="display:flex;gap:8px;">
            <div style="width:25px;height:25px;background:{TEAL_BLUE};
            border-radius:6px;"></div>
            <div style="width:25px;height:25px;background:{ROYAL_BLUE};
            border-radius:6px;"></div>
            <div style="width:25px;height:25px;background:{IVORY_WHITE};
            border:1px solid #ccc;border-radius:6px;"></div>
            <div style="width:25px;height:25px;background:{MUSTARD_YELLOW};
            border-radius:6px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Teal Blue • Royal Blue • Ivory • Mustard")

# ==========================================================
# 7. PREMIUM HERO HEADER
# ==========================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Your next chapter begins elsewhere</div>
        <h1>WanderNest ✈️</h1>
        <p>
            Discover beautiful destinations, design your itinerary,
            compare travel packages and plan your budget.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# 8. HOME PAGE
# ==========================================================

if page == "Home":

    st.markdown(
        '<div class="section-title">Travel should feel effortless.</div>',
        unsafe_allow_html=True
    )

    st.write(
        "WanderNest brings destination discovery, trip planning, "
        "route exploration and budget management into one place."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Destinations", len(DESTINATIONS))
    c2.metric("Travel Packages", 3)
    c3.metric("Planning Tools", 6)

    st.markdown("### ✨ Find your kind of escape")

    featured = ["Goa", "Manali", "Jaipur"]

    cols = st.columns(3)

    for col, name in zip(cols, featured):
        item = DESTINATIONS[name]

        with col:
            st.image(item["image"], use_container_width=True)
            st.subheader(name)
            st.caption(item["best_for"])
            st.write(item["description"])

    st.markdown(
        '<div class="mustard-card">'
        '<b>Your journey, your way.</b><br>'
        'Start with a destination, add your budget, '
        'and let WanderNest organise your travel ideas.'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("Start Planning My Trip ✨"):
        st.session_state["open_planner"] = True
        st.info("Open Trip Planner from the sidebar to continue.")

# ==========================================================
# 9. EXPLORE DESTINATIONS
# ==========================================================

elif page == "Explore Destinations":

    st.markdown(
        '<div class="section-title">🌍 Explore Destinations</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore selected Indian destinations and choose the one "
        "that suits your travel mood."
    )

    selected_destination = st.selectbox(
        "Choose a destination to explore",
        list(DESTINATIONS.keys())
    )

    item = DESTINATIONS[selected_destination]

    st.image(item["image"], use_container_width=True)

    st.subheader(f"Discover {selected_destination}")
    st.write(item["description"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Best for")
        st.write(item["best_for"])

        st.markdown("#### State")
        st.write(item["state"])

    with col2:
        st.markdown("#### Places to explore")

        for place in item["places"]:
            st.write(f"📍 {place}")

    st.markdown("#### Sample day of exploration")

    for activity in item["activities"]:
        st.write(f"• {activity}")

    if st.button("Plan a Trip to " + selected_destination):
        st.session_state["suggested_destination"] = selected_destination
        st.info("Open Trip Planner to enter your travel details.")

    st.caption(
        "Destination descriptions and activities are sample suggestions. "
        "Check local opening hours and conditions before travelling."
    )

# ==========================================================
# 10. TRIP PLANNER
# ==========================================================

elif page == "Trip Planner":

    st.markdown(
        '<div class="section-title">🧳 Create Your Trip</div>',
        unsafe_allow_html=True
    )

    suggested = st.session_state.get(
        "suggested_destination", "Goa"
    )

    destination_options = list(DESTINATIONS.keys())

    if suggested not in destination_options:
        suggested = "Goa"

    with st.form("trip_form"):

        col1, col2 = st.columns(2)

        with col1:
            destination = st.selectbox(
                "Destination",
                destination_options,
                index=destination_options.index(suggested)
            )

            origin = st.text_input(
                "Starting city or address",
                placeholder="e.g. Delhi"
            )

            departure_date = st.date_input(
                "Departure date",
                value=date.today() + timedelta(days=14)
            )

            trip_days = st.number_input(
                "Trip duration in days",
                min_value=1,
                max_value=30,
                value=3
            )

        with col2:
            travellers = st.number_input(
                "Number of travellers",
                min_value=1,
                max_value=50,
                value=2
            )

            travel_style = st.selectbox(
                "Travel style",
                [
                    "Budget",
                    "Standard",
                    "Luxury",
                    "Adventure",
                    "Relaxation",
                    "Culture and History",
                    "Food and Shopping"
                ]
            )

            transport_mode = st.selectbox(
                "Main transport",
                ["Flight", "Train", "Bus", "Car", "Other"]
            )

            total_budget = st.number_input(
                "Your total budget (₹)",
                min_value=1000,
                value=30000,
                step=1000
            )

        submitted = st.form_submit_button(
            "Create My Travel Plan",
            use_container_width=True
        )

    if submitted:

        st.session_state["trip_plan"] = {
            "destination": destination,
            "origin": origin.strip(),
            "departure_date": str(departure_date),
            "trip_days": int(trip_days),
            "travellers": int(travellers),
            "travel_style": travel_style,
            "transport_mode": transport_mode,
            "total_budget": float(total_budget)
        }

        st.session_state["budget_result"] = None

        st.success("Your trip details have been saved!")

    trip = st.session_state.get("trip_plan")

    if trip:

        st.divider()
        st.subheader(f"Your trip to {trip['destination']}")

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Duration", f"{trip['trip_days']} days")
        m2.metric("Travellers", trip["travellers"])
        m3.metric("Trip Budget", f"₹{trip['total_budget']:,.0f}")
        m4.metric(
            "Budget Per Person",
            f"₹{trip['total_budget'] / trip['travellers']:,.0f}"
        )

        st.write(f"**Departure:** {trip['departure_date']}")
        st.write(f"**Starting point:** {trip['origin'] or 'Not provided'}")
        st.write(f"**Travel style:** {trip['travel_style']}")
        st.write(f"**Transport:** {trip['transport_mode']}")

        destination_info = DESTINATIONS[trip["destination"]]

        st.image(
            destination_info["image"],
            use_container_width=True
        )

        st.markdown("### 🗓️ Your sample itinerary")

        for day_number in range(1, trip["trip_days"] + 1):

            with st.expander(f"Day {day_number}"):
                if day_number == 1:
                    st.write("**Morning:** Arrive, settle in and explore nearby.")
                    st.write("**Afternoon:** Visit a major local attraction.")
                    st.write("**Evening:** Enjoy local food and a relaxed walk.")

                elif day_number == trip["trip_days"]:
                    st.write("**Morning:** Enjoy a final sightseeing stop.")
                    st.write("**Afternoon:** Shop for souvenirs or relax.")
                    st.write("**Evening:** Prepare for your return journey.")

                else:
                    activities = destination_info["activities"]

                    for activity in activities:
                        st.write("• " + activity)

                    st.write(
                        "Additional ideas: "
                        + ", ".join(destination_info["places"])
                    )

        st.caption(
            "This itinerary is a planning template, not a live booking. "
            "Travel times, opening hours and availability are not verified."
        )

# ==========================================================
# 11. MAPS, GPS AND ROUTE FINDER
# ==========================================================

elif page == "Maps & Routes":

    st.markdown(
        '<div class="section-title">🗺️ Maps & Route Finder</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore destination locations, open a map to your current "
        "location, and find directions using Google Maps."
    )

    st.markdown("### 📍 Destination map")

    map_rows = []

    for name, info in DESTINATIONS.items():
        map_rows.append({
            "Destination": name,
            "latitude": info["lat"],
            "longitude": info["lon"]
        })

    map_df = pd.DataFrame(map_rows)

    st.map(
        map_df,
        latitude="latitude",
        longitude="longitude",
        color=TEAL_BLUE,
        size=120
    )

    st.caption(
        "Map markers show approximate destination coordinates. "
        "The map does not represent a live customer location."
    )

    st.markdown("### 📱 Use your current location")

    st.write(
        "Open Google Maps and allow location permission in your "
        "browser or device when prompted. WanderNest itself does "
        "not receive or store your GPS coordinates in this version."
    )

    st.link_button(
        "Open Google Maps at My Location",
        "https://www.google.com/maps"
    )

    st.divider()

    st.markdown("### 🚗 Find a route")

    trip = st.session_state.get("trip_plan", {})

    default_origin = trip.get("origin", "")
    default_destination = trip.get("destination", "Goa")

    route_col1, route_col2 = st.columns(2)

    with route_col1:
        route_origin = st.text_input(
            "Route starting point",
            value=default_origin,
            placeholder="e.g. New Delhi Railway Station",
            key="route_origin"
        )

    with route_col2:
        route_destination = st.selectbox(
            "Route destination",
            list(DESTINATIONS.keys()),
            index=(
                list(DESTINATIONS.keys()).index(default_destination)
                if default_destination in DESTINATIONS else 0
            ),
            key="route_destination"
        )

    if route_origin.strip():

        directions_url = (
            "https://www.google.com/maps/dir/?api=1"
            f"&origin={quote(route_origin.strip())}"
            f"&destination={quote(route_destination + ', India')}"
        )

        st.link_button(
            "Open Route and Directions",
            directions_url
        )

        st.info(
            "Google Maps provides the directions. Actual routes, "
            "distances, traffic and journey times are determined "
            "by the mapping service."
        )

    else:
        st.warning(
            "Enter a starting city or address to generate a route link."
        )

    st.caption(
        "WanderNest currently uses external Google Maps directions. "
        "A built-in GPS permission flow and embedded live route "
        "calculation would require additional integration."
    )

# ==========================================================
# 12. COST DASHBOARD AND EXPENSE CALCULATOR
# ==========================================================

elif page == "Cost Dashboard":

    st.markdown(
        '<div class="section-title">💰 Trip Cost Calculator</div>',
        unsafe_allow_html=True
    )

    trip = st.session_state.get("trip_plan", {})

    default_budget = int(trip.get("total_budget", 30000))
    default_travellers = int(trip.get("travellers", 2))
    default_days = int(trip.get("trip_days", 3))

    st.write(
        "Enter estimated expenses to calculate the total trip cost, "
        "tax, remaining budget and per-person expense."
    )

    with st.form("cost_form"):

        budget_limit = st.number_input(
            "Total available budget (₹)",
            min_value=1000,
            value=default_budget,
            step=1000
        )

        travellers = st.number_input(
            "Number of travellers",
            min_value=1,
            max_value=50,
            value=default_travellers
        )

        days = st.number_input(
            "Trip duration (days)",
            min_value=1,
            max_value=30,
            value=default_days
        )

        st.markdown("#### Accommodation")

        accommodation_per_night = st.number_input(
            "Accommodation per night (₹)",
            min_value=0,
            value=2500,
            step=500
        )

        rooms = st.number_input(
            "Number of rooms",
            min_value=1,
            max_value=25,
            value=max(1, (int(travellers) + 1) // 2)
        )

        st.markdown("#### Transport")

        main_transport = st.number_input(
            "Total main transport cost (₹)",
            min_value=0,
            value=6000,
            step=500
        )

        local_transport = st.number_input(
            "Local transport (₹)",
            min_value=0,
            value=1500,
            step=250
        )

        st.markdown("#### Daily and optional expenses")

        food_per_person_day = st.number_input(
            "Food per person per day (₹)",
            min_value=0,
            value=800,
            step=100
        )

        activities_per_person = st.number_input(
            "Activities per person for the whole trip (₹)",
            min_value=0,
            value=1500,
            step=250
        )

        optional_services = st.number_input(
            "Optional services, guides and extras (₹)",
            min_value=0,
            value=1000,
            step=250
        )

        insurance = st.number_input(
            "Insurance and fees (₹)",
            min_value=0,
            value=500,
            step=100
        )

        shopping = st.number_input(
            "Shopping and miscellaneous expenses (₹)",
            min_value=0,
            value=1000,
            step=250
        )

        tax_rate = st.number_input(
            "Estimated tax / contingency percentage",
            min_value=0.0,
            max_value=30.0,
            value=5.0,
            step=0.5
        )

        calculate = st.form_submit_button(
            "Calculate My Trip Cost",
            use_container_width=True
        )

    if calculate:

        accommodation_total = (
            accommodation_per_night * max(0, int(days) - 1) * rooms
        )

        food_total = (
            food_per_person_day * travellers * days
        )

        activities_total = (
            activities_per_person * travellers
        )

        expense_items = [
            ("Accommodation", accommodation_total),
            ("Main Transport", main_transport),
            ("Local Transport", local_transport),
            ("Food and Drinks", food_total),
            ("Activities and Sightseeing", activities_total),
            ("Optional Services", optional_services),
            ("Insurance and Fees", insurance),
            ("Shopping and Miscellaneous", shopping)
        ]

        subtotal = sum(amount for _, amount in expense_items)
        estimated_tax = subtotal * tax_rate / 100
        total_cost = subtotal + estimated_tax
        remaining = budget_limit - total_cost
        cost_per_person = total_cost / travellers

        expense_rows = []

        for category, amount in expense_items:
            expense_rows.append({
                "Expense Category": category,
                "Estimated Cost (₹)": round(amount, 2),
                "Percentage of Subtotal (%)": round(
                    (amount / subtotal * 100) if subtotal else 0,
                    1
                )
            })

        expense_rows.append({
            "Expense Category": "Estimated Tax / Contingency",
            "Estimated Cost (₹)": round(estimated_tax, 2),
            "Percentage of Subtotal (%)": round(tax_rate, 1)
        })

        expenses_df = pd.DataFrame(expense_rows)

        st.session_state["budget_result"] = {
            "budget_limit": budget_limit,
            "travellers": travellers,
            "days": days,
            "subtotal": subtotal,
            "tax_rate": tax_rate,
            "estimated_tax": estimated_tax,
            "total_cost": total_cost,
            "remaining": remaining,
            "cost_per_person": cost_per_person,
            "expenses": expenses_df,
            "expense_items": expense_items
        }

    result = st.session_state.get("budget_result")

    if result:

        st.divider()
        st.markdown("### 📊 Your Cost Dashboard")

        m1, m2, m3 = st.columns(3)

        m1.metric("Estimated Total", f"₹{result['total_cost']:,.0f}")
        m2.metric("Cost per Person", f"₹{result['cost_per_person']:,.0f}")
        m3.metric("Budget Remaining", f"₹{result['remaining']:,.0f}")

        if result["remaining"] < 0:
            st.error(
                f"Your trip exceeds your budget by "
                f"₹{abs(result['remaining']):,.0f}."
            )
        else:
            st.success(
                f"You have ₹{result['remaining']:,.0f} "
                "remaining in your budget."
            )

        st.markdown("#### Detailed Expense Breakdown")

        st.dataframe(
            result["expenses"],
            use_container_width=True,
            hide_index=True
        )

        chart_data = result["expenses"].set_index(
            "Expense Category"
        )["Estimated Cost (₹)"]

        st.markdown("#### Expense Distribution")

        st.bar_chart(chart_data, color=TEAL_BLUE)

        summary_df = pd.DataFrame([
            {"Metric": "Budget Limit (₹)", "Value": result["budget_limit"]},
            {"Metric": "Pre-Tax Subtotal (₹)", "Value": result["subtotal"]},
            {"Metric": "Estimated Tax / Contingency (₹)", "Value": result["estimated_tax"]},
            {"Metric": "Estimated Total (₹)", "Value": result["total_cost"]},
            {"Metric": "Budget Remaining (₹)", "Value": result["remaining"]},
            {"Metric": "Travellers", "Value": result["travellers"]},
            {"Metric": "Trip Duration (days)", "Value": result["days"]},
            {"Metric": "Cost per Person (₹)", "Value": result["cost_per_person"]}
        ])

        expense_buffer = StringIO()
        result["expenses"].to_csv(expense_buffer, index=False)

        summary_buffer = StringIO()
        summary_df.to_csv(summary_buffer, index=False)

        st.download_button(
            "Download Expense Breakdown CSV",
            data=expense_buffer.getvalue(),
            file_name="wandernest_expense_breakdown.csv",
            mime="text/csv"
        )

        st.download_button(
            "Download Cost Summary CSV",
            data=summary_buffer.getvalue(),
            file_name="wandernest_cost_summary.csv",
            mime="text/csv"
        )

        st.caption(
            "All values are estimates entered or calculated for planning. "
            "The tax / contingency percentage is illustrative, not a "
            "verified tax rate. Accommodation is calculated using "
            "the number of nights, which is normally days minus one."
        )

    else:
        st.info(
            "Enter your expenses above and click Calculate My Trip Cost "
            "to see the dashboard."
        )

# ==========================================================
# 13. PACKAGE COMPARISON
# ==========================================================

elif page == "Package Comparison":

    st.markdown(
        '<div class="section-title">⭐ Compare Travel Packages</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Compare illustrative budget, standard and luxury packages "
        "for your selected trip."
    )

    trip = st.session_state.get("trip_plan", {})
    budget_result = st.session_state.get("budget_result")

    base_cost = (
        budget_result["total_cost"]
        if budget_result
        else float(trip.get("total_budget", 30000))
    )

    travellers = int(
        budget_result["travellers"]
        if budget_result
        else trip.get("travellers", 2)
    )

    packages = [
        {
            "Package": "Budget",
            "Multiplier": 0.75,
            "Description": "Simple stays, economical transport and essential activities.",
            "Colour": PALE_TEAL
        },
        {
            "Package": "Standard",
            "Multiplier": 1.00,
            "Description": "Comfortable accommodation, balanced transport and experiences.",
            "Colour": PALE_BLUE
        },
        {
            "Package": "Luxury",
            "Multiplier": 1.80,
            "Description": "Premium stays, upgraded experiences and added comfort.",
            "Colour": "#FFF5D5"
        }
    ]

    package_rows = []

    cols = st.columns(3)

    for col, package in zip(cols, packages):

        package_cost = base_cost * package["Multiplier"]

        package_rows.append({
            "Package": package["Package"],
            "Estimated Total (₹)": round(package_cost, 2),
            "Cost per Person (₹)": round(package_cost / travellers, 2),
            "Relative Estimate": f"{package['Multiplier']:.2f}x base estimate"
        })

        with col:
            st.markdown(
                f"""
                <div style="background:{package['Colour']};
                padding:20px;border-radius:16px;
                border:1px solid {BORDER};min-height:190px;">
                    <h3>{package['Package']}</h3>
                    <h2 style="color:{TEAL_BLUE};">
                    ₹{package_cost:,.0f}</h2>
                    <p>{package['Description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(
                f"Per person: ₹{package_cost / travellers:,.0f}"
            )

    package_df = pd.DataFrame(package_rows)

    st.markdown("### Package Comparison Table")

    st.dataframe(
        package_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Budget, standard and luxury prices are illustrative multipliers "
        "applied to your base estimate. They are not actual supplier "
        "quotes, hotel prices or confirmed travel packages."
    )

    package_buffer = StringIO()
    package_df.to_csv(package_buffer, index=False)

    st.download_button(
        "Download Package Comparison",
        data=package_buffer.getvalue(),
        file_name="wandernest_package_comparison.csv",
        mime="text/csv"
    )

# ==========================================================
# 14. DOWNLOAD TRIP PLAN
# ==========================================================

elif page == "Download Trip Plan":

    st.markdown(
        '<div class="section-title">📥 Download Your Trip Plan</div>',
        unsafe_allow_html=True
    )

    trip = st.session_state.get("trip_plan")
    result = st.session_state.get("budget_result")

    if not trip:

        st.warning(
            "Create a trip first using Trip Planner. "
            "You can then download the trip summary here."
        )

    else:

        destination_info = DESTINATIONS[trip["destination"]]

        st.subheader(f"{trip['destination']} Travel Summary")

        st.write(f"**Starting point:** {trip['origin'] or 'Not provided'}")
        st.write(f"**Departure date:** {trip['departure_date']}")
        st.write(f"**Duration:** {trip['trip_days']} days")
        st.write(f"**Travellers:** {trip['travellers']}")
        st.write(f"**Travel style:** {trip['travel_style']}")
        st.write(f"**Main transport:** {trip['transport_mode']}")
        st.write(f"**Planned budget:** ₹{trip['total_budget']:,.0f}")

        plan_lines = [
            "WANDERNEST TRAVEL PLAN",
            "======================",
            f"Destination: {trip['destination']}",
            f"State: {destination_info['state']}",
            f"Starting point: {trip['origin'] or 'Not provided'}",
            f"Departure date: {trip['departure_date']}",
            f"Trip duration: {trip['trip_days']} days",
            f"Travellers: {trip['travellers']}",
            f"Travel style: {trip['travel_style']}",
            f"Main transport: {trip['transport_mode']}",
            f"Planned budget: INR {trip['total_budget']:,.2f}",
            "",
            "DESTINATION DESCRIPTION",
            destination_info["description"],
            "",
            "PLACES TO EXPLORE"
        ]

        for place in destination_info["places"]:
            plan_lines.append(f"- {place}")

        plan_lines.extend([
            "",
            "SAMPLE DAILY ITINERARY"
        ])

        for day_number in range(1, trip["trip_days"] + 1):
            plan_lines.append(f"Day {day_number}")

            if day_number == 1:
                plan_lines.extend([
                    "- Morning: Arrive and explore nearby.",
                    "- Afternoon: Visit a local attraction.",
                    "- Evening: Enjoy local food and a relaxed walk."
                ])
            elif day_number == trip["trip_days"]:
                plan_lines.extend([
                    "- Morning: Final sightseeing stop.",
                    "- Afternoon: Shopping or relaxation.",
                    "- Evening: Prepare for return travel."
                ])
            else:
                for activity in destination_info["activities"]:
                    plan_lines.append(f"- {activity}")

            plan_lines.append("")

        if result:
            plan_lines.extend([
                "ESTIMATED BUDGET",
                f"Pre-tax subtotal: INR {result['subtotal']:,.2f}",
                f"Estimated tax / contingency: INR {result['estimated_tax']:,.2f}",
                f"Estimated total: INR {result['total_cost']:,.2f}",
                f"Remaining budget: INR {result['remaining']:,.2f}",
                f"Estimated cost per person: INR {result['cost_per_person']:,.2f}",
                ""
            ])

        plan_lines.extend([
            "IMPORTANT NOTE",
            "This is a planning estimate, not a booking confirmation.",
            "Confirm prices, transport schedules, accommodation, opening hours",
            "and local travel conditions before departure."
        ])

        plan_text = "\n".join(plan_lines)

        st.download_button(
            "Download Complete Trip Plan (.txt)",
            data=plan_text,
            file_name="wandernest_trip_plan.txt",
            mime="text/plain",
            use_container_width=True
        )

        trip_summary_df = pd.DataFrame([
            {"Field": "Destination", "Value": trip["destination"]},
            {"Field": "Starting Point", "Value": trip["origin"] or "Not provided"},
            {"Field": "Departure Date", "Value": trip["departure_date"]},
            {"Field": "Duration (days)", "Value": trip["trip_days"]},
            {"Field": "Travellers", "Value": trip["travellers"]},
            {"Field": "Travel Style", "Value": trip["travel_style"]},
            {"Field": "Main Transport", "Value": trip["transport_mode"]},
            {"Field": "Planned Budget (₹)", "Value": trip["total_budget"]}
        ])

        trip_buffer = StringIO()
        trip_summary_df.to_csv(trip_buffer, index=False)

        st.download_button(
            "Download Trip Details CSV",
            data=trip_buffer.getvalue(),
            file_name="wandernest_trip_details.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.info(
            "The downloaded trip plan contains your saved trip details "
            "and sample itinerary. Budget details are included if you "
            "have calculated a budget in Cost Dashboard."
        )

# ==========================================================
# 15. ABOUT WANDERNEST
# ==========================================================

elif page == "About WanderNest":

    st.markdown(
        '<div class="section-title">💙 About WanderNest</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        WanderNest is a travel-planning prototype that helps users
        explore destinations, organise their trip preferences, estimate
        expenses, compare package levels and prepare a downloadable plan.
        """
    )

    st.markdown("### Our Features")

    features = [
        ("Premium Homepage", "A branded landing page with destination highlights."),
        ("Destination Explorer", "Destination descriptions, imagery and suggested places."),
        ("Location Access", "Opens Google Maps so users can allow location access there."),
        ("Interactive Map", "Shows destination markers on a map."),
        ("Route Finder", "Creates external Google Maps directions links."),
        ("Trip Cost Calculator", "Estimates transport, accommodation, food and activities."),
        ("Personalised Itinerary", "Creates a sample itinerary based on destination and duration."),
        ("Cost Dashboard", "Shows totals, per-person costs, budget balance and expenses."),
        ("Download Trip Plan", "Exports trip details and itinerary as a text or CSV file."),
        ("Package Comparison", "Compares illustrative budget, standard and luxury estimates.")
    ]

    for title, description in features:
        st.markdown(
            f"""
            <div class="info-card">
                <b>{title}</b><br>
                {description}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Technology Stack")

    st.write("• Python for calculations and application logic")
    st.write("• Streamlit for the web interface")
    st.write("• Pandas for expense tables and CSV data")
    st.write("• StringIO for preparing downloadable CSV files")
    st.write("• GitHub for source-code management")
    st.write("• Streamlit Community Cloud for deployment")
    st.write("• Google Maps for external maps and directions")

    st.warning(
        "WanderNest is a prototype. It does not book travel, verify live "
        "prices, guarantee tax accuracy, track customers in the background "
        "or access their GPS coordinates inside the application."
    )

# ==========================================================
# 16. FOOTER
# ==========================================================

st.divider()

st.markdown(
    f"""
    <div style="text-align:center;padding:20px;color:{TEAL_BLUE};">
        <h3 style="color:{TEAL_BLUE};">✈️ WanderNest</h3>
        <p>Discover more. Plan better. Wander farther.</p>
        <p style="font-size:12px;">
            Travel planning made simple.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
