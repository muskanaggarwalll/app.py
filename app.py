import streamlit as st
from datetime import date, timedelta
from io import BytesIO

# ============================================================
# WANDERNEST TRAVELS
# A Python Programming Project using Streamlit
# ============================================================

st.set_page_config(
    page_title="WanderNest Travels",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- DESTINATION DATA ----------------------

DESTINATIONS = {
    "Goa": {
        "region": "Coastal Escape",
        "description": "Golden beaches, sunset cafés and relaxed coastal days.",
        "daily_food": 900,
        "activities": 1200,
        "hotel_multiplier": 1.00,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1200&q=85",
        "best_for": "Beaches, friends and sunsets",
        "itinerary": [
            "Day 1: Beach walk and explore a local market",
            "Day 2: Waterfront sightseeing and café time",
            "Day 3: Sunset point and a relaxed evening",
        ],
    },
    "Manali": {
        "region": "Mountain Retreat",
        "description": "Pine forests, mountain views and cosy cafés in the hills.",
        "daily_food": 750,
        "activities": 1400,
        "hotel_multiplier": 1.05,
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1200&q=85",
        "best_for": "Mountains, nature and adventure",
        "itinerary": [
            "Day 1: Explore the town and riverside",
            "Day 2: Mountain viewpoints and local cafés",
            "Day 3: Leisurely walk and souvenir shopping",
        ],
    },
    "Jaipur": {
        "region": "Heritage & Culture",
        "description": "Pink-hued streets, historic architecture and colourful bazaars.",
        "daily_food": 700,
        "activities": 1100,
        "hotel_multiplier": 0.95,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1200&q=85",
        "best_for": "History, architecture and shopping",
        "itinerary": [
            "Day 1: Explore the old city and local bazaar",
            "Day 2: Visit heritage landmarks and gardens",
            "Day 3: Try local food and shop for souvenirs",
        ],
    },
    "Kerala": {
        "region": "Nature & Backwaters",
        "description": "Lush greenery, peaceful waterways and tropical landscapes.",
        "daily_food": 800,
        "activities": 1500,
        "hotel_multiplier": 1.10,
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1200&q=85",
        "best_for": "Nature, slow travel and scenic stays",
        "itinerary": [
            "Day 1: Explore the local area and gardens",
            "Day 2: Enjoy a backwater or nature experience",
            "Day 3: Visit a local market and relax",
        ],
    },
    "Shimla": {
        "region": "Classic Hill Station",
        "description": "Mountain air, historic streets and scenic walks.",
        "daily_food": 700,
        "activities": 1000,
        "hotel_multiplier": 0.90,
        "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1200&q=85",
        "best_for": "Cool weather, walks and weekend breaks",
        "itinerary": [
            "Day 1: Walk along the main promenade",
            "Day 2: Discover viewpoints and nearby nature",
            "Day 3: Enjoy a café stop before departure",
        ],
    },
}

# Illustrative estimates in Indian rupees, not live travel prices.
BASE_HOTEL_PRICE = 2500
TRANSPORT_PER_PERSON = 1800

# -------------------------- CSS -----------------------------
