
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
    "Shimla": {   }
        "region": "Classic Hill Station",
        "description": "Mountain air, scenic walks, charming streets and cafés.",
        "food": 700,
        "activities": 1000,
        "hotel": 2200,
        "transport": 1900,
        "best_for": "Cool weather, mountain views and weekend breaks",
