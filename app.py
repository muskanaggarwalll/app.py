import streamlit as st
from datetime import date, timedelta

# ------------------------------------------------------------
# WanderNest Travels | Python Programming for Business Students
# A single-file Streamlit travel planning application.
# ------------------------------------------------------------

# Set the browser tab and use a wide layout for a modern website.
st.set_page_config(
    page_title="WanderNest Travels",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Keep destination information and sample prices in dictionaries.
# Prices are illustrative estimates in Indian rupees, not live quotes.
DESTINATIONS = {
    "Goa": {
        "region": "Coastal escape",
        "description": "Golden beaches, sunset cafés and relaxed coastal days.",
        "daily_food": 900,
        "activities": 1200,
        "hotel_multiplier": 1.00,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1000&q=85",
        "best_for": "Beaches, friends and sunsets",
        "itinerary": ["Beach walk and local market", "Waterfront sightseeing and café time", "Sunset point and relaxed evening"],
    },
    "Manali": {
        "region": "Mountain retreat",
        "description": "Pine forests, mountain views and cosy cafés in the hills.",
        "daily_food": 750,
        "activities": 1400,
        "hotel_multiplier": 1.05,
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1000&q=85",
        "best_for": "Mountains, nature and adventure",
        "itinerary": ["Explore the town and riverside", "Mountain viewpoints and local cafés", "Leisurely walk and souvenir shopping"],
    },
    "Jaipur": {
        "region": "Heritage & culture",
        "description": "Pink-hued streets, historic architecture and colourful bazaars.",
        "daily_food": 700,
        "activities": 1100,
        "hotel_multiplier": 0.95,
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?auto=format&fit=crop&w=1000&q=85",
        "best_for": "History, architecture and shopping",
        "itinerary": ["Explore the old city and local bazaar", "Visit heritage landmarks and gardens", "Try local food and shop for souvenirs"],
    },
    "Kerala": {
        "region": "Nature & backwaters",
        "description": "Lush greenery, peaceful waterways and tropical landscapes.",
        "daily_food": 800,
        "activities": 1500,
        "hotel_multiplier": 1.10,
        "image": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1000&q=85",
        "best_for": "Nature, slow travel and scenic stays",
        "itinerary": ["Explore the local area and gardens", "Enjoy a backwater or nature experience", "Visit a local market and relax"],
    },
    "Shimla": {
        "region": "Classic hill station",
        "description": "Mountain air, colonial-era streets and scenic walks.",
        "daily_food": 700,
        "activities": 1000,
        "hotel_multiplier": 0.90,
        "image": "https://images.unsplash.com/photo-1597074866923-dc0589150358?auto=format&fit=crop&w=1000&q=85",
        "best_for": "Cool weather, walks and weekend breaks",
        "itinerary": ["Walk along the main promenade", "Discover viewpoints and nearby nature", "Enjoy a relaxed café stop before departure"],
    },
}

# These CSS rules provide the site's colour palette, spacing, cards and buttons.
st.markdown(
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root { --navy: #102a43; --teal: #087e8b; --mint: #dff4ef; --cream: #f7f8f5; }
    .stApp { background: #f6f8f7; color: var(--navy); }
    .block-container { max-width: 1200px; padding-top: 1.5rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: var(--navy) !important; }
    h1, h2 { font-family: 'Playfair Display', Georgia, serif !important; }
    p, label, li, div { font-family: 'DM Sans', Arial, sans-serif; }
    [data-testid="stWidgetLabel"] p { color: #243b53 !important; font-weight: 600; }
    .brand { font-size: 1.05rem; letter-spacing: .08em; font-weight: 700; color: #087e8b; }
    .hero {
        padding: 3rem 2.7rem; border-radius: 24px; color: white;
        background: linear-gradient(100deg, rgba(10,35,55,.92), rgba(10,67,78,.64)),
        url('https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=1800&q=90');
        background-size: cover; background-position: center;
        min-height: 310px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 15px 40px rgba(16,42,67,.14);
    }
    .hero h1 { color: white !important; font-size: clamp(2.3rem, 5vw, 4.1rem); line-height: 1.08; margin: .5rem 0 1rem 0; }
    .hero p { color: #f0fdfa; font-size: 1.08rem; max-width: 620px; }
    .eyebrow { text-transform: uppercase; letter-spacing: .17em; font-size: .78rem; font-weight: 700; color: #9ee8dc; }
