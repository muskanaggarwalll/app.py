
import streamlit as st
import pandas as pd
from io import StringIO

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TripNest | Smart Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. COLOUR PALETTE
# --------------------------------------------------

TEAL_BLUE = "#167D8D"
ROYAL_BLUE = "#3155C6"
IVORY_WHITE = "#FFFEF7"
MUSTARD_YELLOW = "#E5B83F"
DARK_TEXT = "#17333D"
PALE_TEAL = "#E8F5F4"
PALE_BLUE = "#EEF1FF"
BORDER = "#DCE7E5"

# --------------------------------------------------
# 3. CUSTOM WEBSITE STYLING
# --------------------------------------------------

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {IVORY_WHITE};
        color: {DARK_TEXT};
    }}

    [data-testid="stSidebar"] {{
        background-color: {PALE_TEAL};
        border-right: 2px solid {BORDER};
    }}

    .hero {{
        background: linear-gradient(
            120deg,
            {TEAL_BLUE},
            {ROYAL_BLUE}
        );
        color: white;
        padding: 32px;
        border-radius: 22px;
        margin-bottom: 24px;
    }}

    .hero h1 {{
        color: white;
        font-size: 42px;
        margin-bottom: 8px;
    }}

    .hero p {{
        color: #F3F7FF;
        font-size: 16px;
    }}

    .section-card {{
        background-color: white;
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }}

    .section-heading {{
        color: {TEAL_BLUE};
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 10px;
    }}

    .price-card {{
        background-color: {PALE_BLUE};
        border-left: 5px solid {ROYAL_BLUE};
        padding: 18px;
        border-radius: 12px;
        margin: 8px 0;
    }}

    .highlight-card {{
        background-color: #FFF5D5;
        border-left: 5px solid {MUSTARD_YELLOW};
        padding: 18px;
        border-radius: 12px;
        margin: 8px 0;
    }}

    div.stButton > button {{
        background-color: {TEAL_BLUE};
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }}

    div.stButton > button:hover {{
        background-color: {ROYAL_BLUE};
        color: white;
    }}

    div[data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid {BORDER};
        padding: 16px;
        border-radius: 14px;
    }}

    h1, h2, h3 {{
        color: {DARK_TEXT};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 4. SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    st.markdown(f"# ✈️ TripNest")
    st.caption("Your personal travel planning studio")
    st.divider()

    page = st.radio(
        "Explore TripNest",
        [
            "Trip Planner",
            "Budget Breakdown",
            "Travel Checklist",
            "About TripNest"
        ]
    )

    st.divider()
    st.markdown("### Your travel palette")
    st.markdown(
        f"""
        <div style="display:flex;gap:7px;">
            <div title="Teal Blue"
                 style="background:{TEAL_BLUE};height:24px;
                 width:24px;border-radius:6px;"></div>
            <div title="Royal Blue"
                 style="background:{ROYAL_BLUE};height:24px;
                 width:24px;border-radius:6px;"></div>
            <div title="Ivory White"
                 style="background:{IVORY_WHITE};height:24px;
                 width:24px;border:1px solid #ccc;
                 border-radius:6px;"></div>
            <div title="Mustard Yellow"
                 style="background:{MUSTARD_YELLOW};height:24px;
                 width:24px;border-radius:6px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# 5. HERO HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>✈️ TripNest</h1>
        <p>
            Plan smarter. Travel farther. Spend wisely.
        </p>
        <p>
            Your destination planner, itinerary organiser,
            and travel budget companion in one place.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 6. TRIP PLANNER PAGE
# --------------------------------------------------

if page == "Trip Planner":

    st.markdown(
        '<div class="section-heading">🌍 Plan Your Next Adventure</div>',
        unsafe_allow_html=True
    )

    with st.form("trip_planner_form"):

        col1, col2 = st.columns(2)

        with col1:
            destination = st.text_input(
                "Destination",
                placeholder="e.g. Goa, Jaipur, Manali, Paris"
            )

            origin = st.text_input(
                "Starting city",
                placeholder="e.g. Delhi, Mumbai"
            )

            start_date = st.date_input(
                "Departure date"
            )

            travellers = st.number_input(
                "Number of travellers",
                min_value=1,
                max_value=50,
                value=2
            )

        with col2:
            travel_style = st.selectbox(
                "Travel style",
                [
                    "Adventure",
                    "Relaxation",
                    "Culture and History",
                    "Food and Shopping",
                    "Luxury",
                    "Nature and Wildlife",
                    "Budget Travel"
                ]
            )

            transport = st.selectbox(
                "Main transport",
                [
                    "Flight",
                    "Train",
                    "Bus",
                    "Car",
                    "Other"
                ]
            )

            trip_days = st.number_input(
                "Trip duration (days)",
                min_value=1,
                max_value=90,
                value=3
            )

            total_budget = st.number_input(
                "Total trip budget (₹)",
                min_value=0,
                value=20000,
                step=1000
            )

        submitted = st.form_submit_button(
            "Create My Trip Plan ✨",
            use_container_width=True
        )

    if submitted:

        if not destination.strip():
            st.error("Please enter a destination.")

        elif total_budget <= 0:
            st.error("Please enter a budget greater than zero.")

        else:
            st.session_state["trip"] = {
                "destination": destination.strip(),
                "origin": origin.strip() or "Not specified",
                "start_date": str(start_date),
                "travellers": int(travellers),
                "travel_style": travel_style,
                "transport": transport,
                "trip_days": int(trip_days),
                "total_budget": float(total_budget)
            }

            st.success("Your trip details have been saved!")

    if "trip" in st.session_state:

        trip = st.session_state["trip"]

        st.divider()
        st.subheader(f"📍 Your Trip to {trip['destination']}")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Travellers", trip["travellers"])
        c2.metric("Duration", f"{trip['trip_days']} days")
        c3.metric("Total Budget", f"₹{trip['total_budget']:,.0f}")
        c4.metric(
            "Budget per Person",
            f"₹{trip['total_budget'] / trip['travellers']:,.0f}"
        )

        st.write(f"**Starting city:** {trip['origin']}")
        st.write(f"**Departure date:** {trip['start_date']}")
        st.write(f"**Transport:** {trip['transport']}")
        st.write(f"**Travel style:** {trip['travel_style']}")

        if st.button("Calculate My Budget Breakdown"):
            st.session_state["show_budget"] = True
            st.session_state["budget_trip"] = trip

        if st.button("Clear Saved Trip"):
            st.session_state.pop("trip", None)
            st.session_state.pop("show_budget", None)
            st.session_state.pop("budget_trip", None)
            st.rerun()

# --------------------------------------------------
# 7. BUDGET BREAKDOWN PAGE
# --------------------------------------------------

elif page == "Budget Breakdown":

    st.markdown(
        '<div class="section-heading">💰 Smart Travel Budget</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter estimated expenses for your trip. "
        "TripNest will calculate your total spending, "
        "remaining budget, and cost per traveller."
    )

    saved_trip = st.session_state.get("trip", {})

    with st.form("budget_form"):

        budget_limit = st.number_input(
            "Total available budget (₹)",
            min_value=1,
            value=int(saved_trip.get("total_budget", 20000)),
            step=1000
        )

        st.markdown("#### 🏨 Accommodation")
        accommodation = st.number_input(
            "Total accommodation cost (₹)",
            min_value=0,
            value=5000,
            step=500
        )

        st.markdown("#### 🚆 Transportation")
        transport_cost = st.number_input(
            "Flights, trains, buses or fuel (₹)",
            min_value=0,
            value=4000,
            step=500
        )

        local_transport = st.number_input(
            "Local travel and transfers (₹)",
            min_value=0,
            value=1000,
            step=100
        )

        st.markdown("#### 🍽️ Food and Activities")
        food = st.number_input(
            "Food and drinks (₹)",
            min_value=0,
            value=2000,
            step=250
        )

        activities = st.number_input(
            "Sightseeing, tickets and activities (₹)",
            min_value=0,
            value=1500,
            step=250
        )

        shopping = st.number_input(
            "Shopping and souvenirs (₹)",
            min_value=0,
            value=1000,
            step=250
        )

        st.markdown("#### 🧾 Other Expenses")
        insurance = st.number_input(
            "Travel insurance and fees (₹)",
            min_value=0,
            value=500,
            step=100
        )

        miscellaneous = st.number_input(
            "Emergency and miscellaneous expenses (₹)",
            min_value=0,
            value=1000,
            step=250
        )

        travellers_for_budget = st.number_input(
            "Number of travellers",
            min_value=1,
            max_value=50,
            value=int(saved_trip.get("travellers", 2))
        )

        calculate = st.form_submit_button(
            "Calculate Total Expenses 💰",
            use_container_width=True
        )

    if calculate:

        expense_items = [
            ("Accommodation", accommodation),
            ("Main Transport", transport_cost),
            ("Local Transport", local_transport),
            ("Food and Drinks", food),
            ("Activities and Sightseeing", activities),
            ("Shopping and Souvenirs", shopping),
            ("Insurance and Fees", insurance),
            ("Emergency and Miscellaneous", miscellaneous)
        ]

        total_expenses = sum(amount for name, amount in expense_items)
        remaining_budget = budget_limit - total_expenses
        per_person = total_expenses / travellers_for_budget

        expense_data = []

        for category, amount in expense_items:
            percentage = (
                (amount / total_expenses) * 100
                if total_expenses > 0 else 0
            )

            expense_data.append({
                "Expense Category": category,
                "Estimated Cost (₹)": amount,
                "Share of Expenses (%)": round(percentage, 1)
            })

        expense_df = pd.DataFrame(expense_data)

        st.session_state["budget_results"] = {
            "budget_limit": budget_limit,
            "total_expenses": total_expenses,
            "remaining_budget": remaining_budget,
            "per_person": per_person,
            "travellers": travellers_for_budget,
            "expenses": expense_df
        }

    if "budget_results" in st.session_state:

        result = st.session_state["budget_results"]

        st.divider()
        st.subheader("📊 Your Expense Summary")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Total Expenses",
            f"₹{result['total_expenses']:,.2f}"
        )

        m2.metric(
            "Budget Remaining",
            f"₹{result['remaining_budget']:,.2f}",
            delta=f"{result['remaining_budget']:,.2f}"
        )

        m3.metric(
            "Expense per Person",
            f"₹{result['per_person']:,.2f}"
        )

        if result["remaining_budget"] < 0:
            st.error(
                f"You are over budget by "
                f"₹{abs(result['remaining_budget']):,.2f}. "
                "Consider reducing some expenses."
            )
        else:
            st.success(
                f"You are within budget with "
                f"₹{result['remaining_budget']:,.2f} remaining."
            )

        st.markdown("#### Detailed Expense Table")

        st.dataframe(
            result["expenses"],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("#### Expense Distribution")

        chart_data = result["expenses"].set_index("Expense Category")[
            "Estimated Cost (₹)"
        ]

        st.bar_chart(chart_data, color=TEAL_BLUE)

        # Download expense report as CSV
        csv_buffer = StringIO()
        result["expenses"].to_csv(csv_buffer, index=False)

        summary_df = pd.DataFrame([
            {"Metric": "Available Budget (₹)", "Value": result["budget_limit"]},
            {"Metric": "Total Expenses (₹)", "Value": result["total_expenses"]},
            {"Metric": "Remaining Budget (₹)", "Value": result["remaining_budget"]},
            {"Metric": "Travellers", "Value": result["travellers"]},
            {"Metric": "Cost per Person (₹)", "Value": round(result["per_person"], 2)}
        ])

        summary_buffer = StringIO()
        summary_df.to_csv(summary_buffer, index=False)

        st.download_button(
            label="Download Detailed Expense CSV 📥",
            data=csv_buffer.getvalue(),
            file_name="tripnest_expenses.csv",
            mime="text/csv"
        )

        st.download_button(
            label="Download Budget Summary 📄",
            data=summary_buffer.getvalue(),
            file_name="tripnest_budget_summary.csv",
            mime="text/csv"
        )

# --------------------------------------------------
# 8. TRAVEL CHECKLIST
# --------------------------------------------------

elif page == "Travel Checklist":

    st.markdown(
        '<div class="section-heading">🧳 Travel Checklist</div>',
        unsafe_allow_html=True
    )

    st.write("Tick items as you prepare for your journey.")

    st.markdown("#### 📄 Documents")
    st.checkbox("Passport or government ID")
    st.checkbox("Tickets and booking confirmations")
    st.checkbox("Hotel reservation details")
    st.checkbox("Travel insurance documents")

    st.markdown("#### 👕 Essentials")
    st.checkbox("Clothing and footwear")
    st.checkbox("Toiletries and personal care")
    st.checkbox("Phone charger and power bank")
    st.checkbox("Medicines and first-aid essentials")

    st.markdown("#### 💳 Money and Safety")
    st.checkbox("Payment cards and cash")
    st.checkbox("Emergency contact information")
    st.checkbox("Destination weather checked")
    st.checkbox("Transport to airport or station arranged")

    st.info(
        "Checklist progress is currently temporary and is not saved "
        "after a full browser session reset."
    )

# --------------------------------------------------
# 9. ABOUT TRIPNEST
# --------------------------------------------------

elif page == "About TripNest":

    st.markdown(
        '<div class="section-heading">💙 About TripNest</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        TripNest is a travel planning prototype designed to help
        travellers organise basic trip information and estimate
        their travel expenses in one place.
        """
    )

    st.markdown("#### What TripNest offers")

    st.markdown(
        """
        - **Trip Planning:** Record destinations, dates, travellers,
          travel styles, and budgets.
        - **Budget Management:** Estimate costs for accommodation,
          transport, food, activities, shopping, and other expenses.
        - **Cost Analysis:** Calculate remaining budget and
          estimated expenses per person.
        - **Expense Reports:** Download travel expense information
          as CSV files.
        - **Travel Checklist:** Organise essential travel tasks.
        """
    )

    st.markdown("#### Technology used")

    st.markdown(
        """
        - Python
        - Streamlit
        - Pandas
        - StringIO for CSV generation
        - GitHub for source-code storage
        - Streamlit Community Cloud for deployment
        """
    )

    st.warning(
        "TripNest uses user-entered estimates. It does not currently "
        "fetch live ticket prices, hotel availability, exchange rates, "
        "or real-time destination information."
    )

# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    f"""
    <div style="text-align:center; padding:14px;
    color:{TEAL_BLUE};">
        <b>✈️ TripNest</b><br>
        Plan smarter. Travel farther. Spend wisely.<br>
        <span style="font-size:12px;">
            Travel planning made simple.
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
