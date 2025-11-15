import streamlit as st
import datetime
import time
import random

# --- (A) V4: Enhanced Simulation & Data Functions ---

# --- NEW: Dummy database for rental agencies ---
def get_rental_options(origin_city, transport_mode):
    """
    Simulates fetching rental options from the origin city.
    """
    db = {
        "delhi": {
            "Rented Bike": [
                {"name": "Delhi Bike Rentals", "model": "Himalayan 411", "price": 2200},
                {"name": "Roadriders", "model": "Classic 350", "price": 1800},
                {"name": "Gears & Gallop", "model": "KTM 390 Adv", "price": 3000},
            ],
            "Rented Car": [
                {"name": "Zoomcar Delhi", "model": "Tata Nexon", "price": 2500},
                {"name": "Avis India", "model": "Toyota Innova", "price": 4500},
            ]
        },
        "manali": {
            "Rented Bike": [
                {"name": "Manali Bikes", "model": "Himalayan 411", "price": 2400},
                {"name": "Trek & Ride", "model": "Classic 350", "price": 2000},
            ]
        },
        "kolkata": {
            "Rented Bike": [
                {"name": "Kolkata on Wheels", "model": "Classic 350", "price": 1700},
                {"name": "Ride Easy", "model": "Himalayan", "price": 2100},
            ],
            "Rented Car": [
                {"name": "Savaari Car Rentals", "model": "Maruti Dzire", "price": 2200},
            ]
        }
    }
    
    city_key = origin_city.lower().strip()
    if city_key in db and transport_mode in db[city_key]:
        return db[city_key][transport_mode]
    else:
        return [{"name": f"No specific {transport_mode} agencies in database for {origin_city}", "model": "N/A", "price": 0}]

# --- NEW: Central function for daily cost calculation ---
def get_daily_costs(mode, hotel_pref, food_pref):
    """
    Calculates the cost per day for each category.
    This ensures the daily and total budgets are consistent.
    """
    # Base daily costs (dummy values in INR)
    transport_cost = {
        "Personal Bike": 1200,  # Fuel + Maintenance
        "Personal Car": 2500,   # Fuel + Tolls + Maintenance
        "Rented Bike": 1800,    # Rent + Fuel
        "Rented Car": 4000,     # Rent + Fuel
        "Public Transport": 3000 # Averaged
    }
    hotel_cost = {
        "Cheap": 1200,
        "Standard": 2800,
        "Branded": 8000
    }
    food_cost = {
        "Cheap": 500,       # Local dhabas, street food
        "Standard": 1500,   # Mid-range restaurants
        "Branded": 4000     # Fine dining, high-end cafes
    }
    
    costs = {}
    costs['fuel_transport'] = transport_cost.get(mode, 2000)
    costs['stay'] = hotel_cost.get(hotel_pref, 2000)
    costs['food'] = food_cost.get(food_pref, 1000)
    
    # Add a 15% contingency/emergency fund
    subtotal = costs['fuel_transport'] + costs['stay'] + costs['food']
    costs['contingency'] = int(subtotal * 0.15)
    
    costs['total_per_day'] = subtotal + costs['contingency']
    
    return costs

# --- UPDATED: Total budget now uses the daily cost function ---
def calculate_total_budget(mode, hotel_pref, food_pref, duration_days, is_peak_season):
    """
    Calculates the total trip budget using the consistent daily costs.
    """
    daily = get_daily_costs(mode, hotel_pref, food_pref)
    
    # Calculate totals
    # Transport, food, and contingency are for all days
    total_fuel_transport = daily['fuel_transport'] * duration_days
    total_food = daily['food'] * duration_days
    total_contingency = daily['contingency'] * duration_days
    
    # Hotel is per night (duration - 1)
    total_stay = daily['stay'] * (duration_days - 1) 
    
    base_budget = total_fuel_transport + total_food + total_stay + total_contingency
    
    # Add peak season multiplier
    if is_peak_season:
        final_budget = base_budget * 1.30
    else:
        final_budget = base_budget

    return int(final_budget)

def get_sightseeing_spots(location):
    # (Same as before)
    sightseeing_db = {
        "delhi": ["India Gate", "Red Fort", "Qutub Minar"],
        "agra": ["Taj Mahal", "Agra Fort"],
        "jaipur": ["Hawa Mahal", "Amber Fort"],
        "manali": ["Hadimba Temple", "Solang Valley"],
        "leh": ["Pangong Lake", "Shanti Stupa"],
        "ladakh": ["Nubra Valley", "Khardung La"],
        "goa": ["Baga Beach", "Fort Aguada"],
        "kolkata": ["Victoria Memorial", "Howrah Bridge"],
        "varanasi": ["Kashi Vishwanath Temple", "Ganga Aarti"],
        "jammu": ["Raghunath Temple", "Bahu Fort"],
        "srinagar": ["Dal Lake", "Mughal Gardens"]
    }
    loc_lower = location.lower().strip()
    return sightseeing_db.get(loc_lower, ["Local City Center", "Famous Local Market"])

# --- UPDATED: Now accepts transport_mode and adds daily budget data ---
def generate_structured_itinerary(places_list, hotel_pref, food_pref, transport_mode):
    """
    Generates structured itinerary, now including daily budget data.
    """
    
    itinerary_data = []
    day_counter = 1
    
    # Get daily cost breakdown
    daily_costs = get_daily_costs(transport_mode, hotel_pref, food_pref)
    
    # Recommendation styles (same as before)
    stays = {"Cheap": "Zostel/Guest House", "Standard": "3-Star City Hotel", "Branded": "Marriott/Taj"}
    eateries = {"Cheap": "Highway Dhaba", "Standard": "Haldiram's/Cafe", "Branded": "Fine Dining Restaurant"}

    for i in range(len(places_list) - 1):
        origin = places_list[i]
        destination = places_list[i+1]
        
        itinerary_data.append({"type": "leg_header", "text": f"Leg {i+1}: {origin} ➔ {destination}"})
        
        # --- DAY 1 of Leg ---
        day_plan = []
        day_plan.append({"icon": "☕", "time": "08:00 AM", "activity": f"Breakfast at {origin}."})
        spots = get_sightseeing_spots(origin)
        day_plan.append({"icon": "📸", "time": "10:00 AM", "activity": f"Visit: {', '.join(spots[:2])}."})
        mid_point = "Scenic Highway Stop"
        day_plan.append({"icon": "🚗", "time": "01:00 PM", "activity": f"Drive towards {destination}. Stop for lunch at a {random.choice(list(eateries.values()))}."})
        day_plan.append({"icon": "HOTEL", "time": "07:00 PM", "activity": f"Halt at {mid_point}. Check into a {stays[hotel_pref]}."})
        
        itinerary_data.append({
            "type": "day_card",
            "day_num": day_counter,
            "route": f"{origin} ➔ {mid_point}",
            "events": day_plan,
            "budget": daily_costs # --- ADDED DAILY BUDGET ---
        })
        day_counter += 1
        
        # --- DAY 2 of Leg ---
        day_plan_2 = []
        day_plan_2.append({"icon": "🛣️", "time": "09:00 AM", "activity": "Resume journey. Enjoy the landscape."})
        day_plan_2.append({"icon": "🏁", "time": "02:00 PM", "activity": f"Arrive in **{destination}**! Check into your {stays[hotel_pref]}."})
        dest_spots = get_sightseeing_spots(destination)
        day_plan_2.append({"icon": "📸", "time": "04:00 PM", "activity": f"Explore {destination}: Visit {', '.join(dest_spots)}."})
        day_plan_2.append({"icon": "🍽️", "time": "08:30 PM", "activity": f"Dinner at a {random.choice(list(eateries.values()))} in {destination}."})
        
        itinerary_data.append({
            "type": "day_card",
            "day_num": day_counter,
            "route": f"{mid_point} ➔ {destination}",
            "events": day_plan_2,
            "budget": daily_costs # --- ADDED DAILY BUDGET ---
        })
        day_counter += 1

    return itinerary_data

def get_special_permissions(places_list):
    # (Same as before)
    db = {"leh": "ILP Required", "ladakh": "ILP Required", "manali": "Rohtang Permit", "sikkim": "PAP Required", "tawang": "ILP Required"}
    perms = []
    for p in places_list:
        for k, v in db.items():
            if k in p.lower(): perms.append(f"{p}: {v}")
    return perms if perms else ["No special permits found in database."]

# --- (B) Streamlit UI ---
st.set_page_config(page_title="Your Travel and Adventure", layout="wide", page_icon="🏞️")

st.markdown("""<style> .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; } </style>""", unsafe_allow_html=True)

st.title("🏞️ YOUR TRAVEL AND ADVENTURE")
st.caption("AI-Powered Itinerary Planner for India")

# --- Sidebar (Inputs) ---
with st.sidebar:
    st.header("Plan Your Trip")
    places_input = st.text_area("Destinations (in order)", "Delhi, Manali, Leh", height=100)
    transport_mode = st.selectbox("Mode of Transport", ["Personal Bike", "Personal Car", "Rented Bike", "Rented Car", "Public Transport"])
    
    st.subheader("Dates")
    c1, c2 = st.columns(2)
    start_date = c1.date_input("Start", datetime.date.today())
    end_date = c2.date_input("End", datetime.date.today() + datetime.timedelta(days=5))
    
    st.subheader("Preferences")
    hotel_pref = st.select_slider("Hotel Class", ["Cheap", "Standard", "Branded"], value="Standard")
    food_pref = st.select_slider("Food Class", ["Cheap", "Standard", "Branded"], value="Standard")
    
    generate_btn = st.button("🚀 Generate Itinerary", type="primary", use_container_width=True)

# --- Main Display Area ---
if generate_btn:
    places_list = [p.strip() for p in places_input.split(',') if p.strip()]
    duration = (end_date - start_date).days + 1
    is_peak = start_date.month in [5, 6, 12, 1]
    
    if len(places_list) < 2:
        st.error("Please enter at least two destinations.")
    else:
        # 1. Budget Section
        budget = calculate_total_budget(transport_mode, hotel_pref, food_pref, duration, is_peak)
        col_b1, col_b2, col_b3 = st.columns(3)
        col_b1.metric("Total Budget", f"₹{budget:,}")
        col_b2.metric("Duration", f"{duration} Days")
        col_b3.metric("Travel Mode", transport_mode)
        st.divider()
        
        # 2. Permissions Section
        perms = get_special_permissions(places_list)
        if "No special permits" not in perms[0]:
            st.warning("⚠️ **Permits Required:** " + ", ".join(perms))
        
        # --- NEW: 3. Rental Information Section ---
        if transport_mode in ["Rented Bike", "Rented Car"]:
            with st.expander(f"**Rental Options for {transport_mode} from {places_list[0]}**", expanded=True):
                rentals = get_rental_options(places_list[0], transport_mode)
                
                # Create columns for a clean table-like look
                col1, col2, col3 = st.columns(3)
                col1.markdown("**Agency**")
                col2.markdown("**Example Model**")
                col3.markdown("**Est. Price/Day**")
                
                for rental in rentals:
                    col1, col2, col3 = st.columns(3)
                    col1.write(rental['name'])
                    col2.write(rental['model'])
                    col3.write(f"₹{rental['price']:,}")
        
        # 4. The Structured Itinerary Display
        st.subheader("🗺️ Your Day-by-Day Plan")
        
        # --- UPDATED: Pass transport_mode ---
        structured_data = generate_structured_itinerary(places_list, hotel_pref, food_pref, transport_mode)
        
        for item in structured_data:
            if item["type"] == "leg_header":
                st.markdown(f"### {item['text']}")
            
            elif item["type"] == "day_card":
                with st.container(border=True):
                    c_day, c_details = st.columns([1, 5])
                    
                    with c_day:
                        st.markdown(f"## Day {item['day_num']}")
                        st.caption(item['route'])
                    
                    with c_details:
                        for event in item['events']:
                            icon = event['icon']
                            if icon == "HOTEL":
                                st.info(f"**{event['time']} | Stay:** {event['activity']}")
                            else:
                                st.write(f"{icon} **{event['time']}:** {event['activity']}")
                        
                        # --- NEW: Daily Budget Breakdown ---
                        budget = item['budget']
                        with st.expander("💰 **Show Daily Budget Breakdown**"):
                            st.markdown(f"""
                            * **Stay:** `₹{budget['stay']:,}`
                            * **Fuel/Transport:** `₹{budget['fuel_transport']:,}`
                            * **Food:** `₹{budget['food']:,}`
                            * **Contingency (15%):** `₹{budget['contingency']:,}`
                            * **Est. Day Total:** `₹{budget['total_per_day']:,}`
                            """)
                            st.caption("Note: 'Stay' cost is applied to your night halt.")
        
        st.success("Trip planning complete! Drive safe.")

elif not generate_btn:
    st.info("👈 Use the sidebar menu to plan your adventure!")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80", caption="Explore Incredible India")
    with col2:
        st.image("https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80", caption="Adventure Awaits")
