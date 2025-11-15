import streamlit as st
import datetime
import time
import random
import pandas as pd
import pydeck as pdk  # --- NEW IMPORT for advanced maps ---

# --- (A) V5: Enhanced Simulation & Data Functions ---

def get_dummy_coordinates(places_list):
    """
    Returns coordinates and specifically formats them for the Map Path.
    """
    coordinates_db = {
        "delhi": {"lat": 28.7041, "lon": 77.1025},
        "manali": {"lat": 32.2432, "lon": 77.1890},
        "leh": {"lat": 34.1526, "lon": 77.5771},
        "ladakh": {"lat": 34.1526, "lon": 77.5771},
        "kolkata": {"lat": 22.5726, "lon": 88.3639},
        "varanasi": {"lat": 25.3176, "lon": 82.9739},
        "mumbai": {"lat": 19.0760, "lon": 72.8777},
        "goa": {"lat": 15.2993, "lon": 74.1240},
        "chennai": {"lat": 13.0827, "lon": 80.2707},
        "bangalore": {"lat": 12.9716, "lon": 77.5946},
        "jaipur": {"lat": 26.9124, "lon": 75.7873},
        "agra": {"lat": 27.1767, "lon": 78.0081},
        "srinagar": {"lat": 34.0837, "lon": 74.7973},
        "jammu": {"lat": 32.7266, "lon": 74.8570},
        "spiti": {"lat": 32.2470, "lon": 78.0280},
        "shimla": {"lat": 31.1048, "lon": 77.1734},
        "rishikesh": {"lat": 30.0869, "lon": 78.2676},
    }
    
    # 1. Get list of valid coordinates in order
    route_coords = []
    valid_places = []
    
    for place in places_list:
        key = place.lower().strip()
        if key in coordinates_db:
            # Pydeck expects [Longitude, Latitude]
            point = [coordinates_db[key]["lon"], coordinates_db[key]["lat"]]
            route_coords.append(point)
            valid_places.append({"name": place, "coordinates": point})
            
    return route_coords, valid_places

def get_rental_options(origin_city, transport_mode):
    db = {
        "delhi": {
            "Rented Bike": [{"name": "Delhi Bike Rentals", "model": "Himalayan 411", "price": 2200}],
            "Rented Car": [{"name": "Zoomcar Delhi", "model": "Tata Nexon", "price": 2500}]
        },
        "manali": {"Rented Bike": [{"name": "Manali Bikes", "model": "Himalayan 411", "price": 2400}]},
        "kolkata": {"Rented Bike": [{"name": "Kolkata on Wheels", "model": "Classic 350", "price": 1700}]}
    }
    city_key = origin_city.lower().strip()
    if city_key in db and transport_mode in db[city_key]:
        return db[city_key][transport_mode]
    return [{"name": f"No specific agencies in DB for {origin_city}", "model": "N/A", "price": 0}]

def get_daily_costs(mode, hotel_pref, food_pref):
    costs = {}
    costs['fuel_transport'] = {"Personal Bike": 1200, "Personal Car": 2500, "Rented Bike": 1800, "Rented Car": 4000, "Public Transport": 2800}.get(mode, 2000)
    costs['stay'] = {"Cheap": 1200, "Standard": 2800, "Branded": 8000}.get(hotel_pref, 2000)
    costs['food'] = {"Cheap": 500, "Standard": 1500, "Branded": 4000}.get(food_pref, 1000)
    subtotal = costs['fuel_transport'] + costs['stay'] + costs['food']
    costs['contingency'] = int(subtotal * 0.15)
    costs['total_per_day'] = subtotal + costs['contingency']
    return costs

def calculate_total_budget(mode, hotel_pref, food_pref, duration_days, is_peak_season):
    daily = get_daily_costs(mode, hotel_pref, food_pref)
    total_fuel_transport = daily['fuel_transport'] * duration_days
    total_food = daily['food'] * duration_days
    total_contingency = daily['contingency'] * duration_days
    total_stay = daily['stay'] * (duration_days - 1)
    base_budget = total_fuel_transport + total_food + total_stay + total_contingency
    final_budget = base_budget * 1.30 if is_peak_season else base_budget
    return int(final_budget)

def get_sightseeing_spots(location):
    sightseeing_db = {
        "delhi": ["India Gate", "Red Fort", "Qutub Minar"], "agra": ["Taj Mahal", "Agra Fort"],
        "jaipur": ["Hawa Mahal", "Amber Fort"], "manali": ["Hadimba Temple", "Solang Valley"],
        "leh": ["Pangong Lake", "Shanti Stupa"], "ladakh": ["Nubra Valley", "Khardung La"],
        "kolkata": ["Victoria Memorial", "Howrah Bridge"], "varanasi": ["Kashi Vishwanath Temple", "Ganga Aarti"],
        "jammu": ["Raghath Temple", "Bahu Fort"], "srinagar": ["Dal Lake", "Mughal Gardens"],
        "spiti": ["Key Monastery", "Chandratal Lake"]
    }
    loc_lower = location.lower().strip()
    return sightseeing_db.get(loc_lower, ["Local City Center", "Famous Local Market"])

def get_special_permissions(places_list):
    db = {"leh": "ILP Required", "ladakh": "ILP Required", "manali": "Rohtang Permit", "sikkim": "PAP Required", "tawang": "ILP Required", "spiti": "Inner Line Permit (for foreigners)"}
    perms = [f"{p}: {v}" for p in places_list for k, v in db.items() if k in p.lower()]
    return perms if perms else ["No special permits found in database."]

def get_public_transport_recommendation(origin, destination):
    origin, dest = origin.lower(), destination.lower()
    if "leh" in dest or "ladakh" in dest:
        return f"Fly from {origin.capitalize()} to Leh (IXL). This is the fastest and most reliable route."
    if "delhi" in origin and "manali" in dest:
        return f"Take an overnight AC Volvo bus (e.g., HPTDC) from ISBT Kashmere Gate, Delhi."
    if "delhi" in origin and "agra" in dest:
        return "Take the morning Shatabdi Express or Gatimaan Express train. It's fast (2 hours)."
    if "kolkata" in origin and "delhi" in dest:
        return f"Take a direct flight (CCU -> DEL) or an overnight train (e.g., Rajdhani Express)."
    return f"Look for overnight state transport buses or direct trains from {origin.capitalize()} to {destination.capitalize()}."

def generate_structured_itinerary(places_list, hotel_pref, food_pref, transport_mode):
    itinerary_data = []
    day_counter = 1
    daily_costs = get_daily_costs(transport_mode, hotel_pref, food_pref)
    stays = {"Cheap": "Zostel/Guest House", "Standard": "3-Star City Hotel", "Branded": "Marriott/Taj"}
    eateries = {"Cheap": "Highway Dhaba", "Standard": "Haldiram's/Cafe", "Branded": "Fine Dining Restaurant"}

    for i in range(len(places_list) - 1):
        origin = places_list[i]
        destination = places_list[i+1]
        itinerary_data.append({"type": "leg_header", "text": f"Leg {i+1}: {origin} ➔ {destination}"})
        
        # Day 1
        day_plan = []
        if transport_mode == "Public Transport":
            recommendation = get_public_transport_recommendation(origin, destination)
            day_plan.append({"icon": "☕", "time": "08:00 AM", "activity": f"Breakfast at {origin} and head to the bus/train station or airport."})
            spots = get_sightseeing_spots(origin)
            day_plan.append({"icon": "📸", "time": "11:00 AM", "activity": f"Quickly visit: {', '.join(spots[:1])}."})
            day_plan.append({"icon": "🎫", "time": "02:00 PM", "activity": f"**Travel:** {recommendation}"})
            day_plan.append({"icon": "HOTEL", "time": "09:00 PM", "activity": "Arrive at your destination or travel overnight."})
        else:
            day_plan.append({"icon": "☕", "time": "08:00 AM", "activity": f"Breakfast at {origin}."})
            spots = get_sightseeing_spots(origin)
            day_plan.append({"icon": "📸", "time": "10:00 AM", "activity": f"Visit: {', '.join(spots[:2])}."})
            mid_point = "Scenic Highway Stop"
            day_plan.append({"icon": "🚗", "time": "01:00 PM", "activity": f"Drive towards {destination}. Stop for lunch at a {random.choice(list(eateries.values()))}."})
            day_plan.append({"icon": "HOTEL", "time": "07:00 PM", "activity": f"Halt at {mid_point}. Check into a {stays[hotel_pref]}."})
        itinerary_data.append({"type": "day_card", "day_num": day_counter, "route": f"{origin} ➔ {destination} (Leg 1/2)", "events": day_plan, "budget": daily_costs})
        day_counter += 1
        
        # Day 2
        day_plan_2 = []
        dest_spots = get_sightseeing_spots(destination)
        if transport_mode == "Public Transport":
            day_plan_2.append({"icon": "🏁", "time": "09:00 AM", "activity": f"Arrive in **{destination}**. Check into your {stays[hotel_pref]}."})
            day_plan_2.append({"icon": "🚕", "time": "11:00 AM", "activity": "Hire a local auto/taxi for sightseeing."})
            day_plan_2.append({"icon": "📸", "time": "01:00 PM", "activity": f"Explore {destination}: Visit {', '.join(dest_spots)}."})
        else:
            day_plan_2.append({"icon": "🛣️", "time": "09:00 AM", "activity": "Resume journey. Enjoy the landscape."})
            day_plan_2.append({"icon": "🏁", "time": "02:00 PM", "activity": f"Arrive in **{destination}**! Check into your {stays[hotel_pref]}."})
            day_plan_2.append({"icon": "📸", "time": "04:00 PM", "activity": f"Explore {destination}: Visit {', '.join(dest_spots)}."})
        day_plan_2.append({"icon": "🍽️", "time": "08:30 PM", "activity": f"Dinner at a {random.choice(list(eateries.values()))} in {destination}."})
        itinerary_data.append({"type": "day_card", "day_num": day_counter, "route": f"Arrive at {destination} (Leg 2/2)", "events": day_plan_2, "budget": daily_costs})
        day_counter += 1

    return itinerary_data

# --- (B) Streamlit UI ---
st.set_page_config(page_title="Your Travel and Adventure", layout="wide", page_icon="🏞️")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Raleway:wght@400;600&display=swap');
    html, body, [class*="st-"], .st-emotion-cache-10trblm { font-family: 'Raleway', sans-serif; }
    h1, .st-emotion-cache-183lzff { font-family: 'Playfair Display', serif; font-weight: 700; letter-spacing: 0.5px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🏞️ YOUR TRAVEL AND ADVENTURE")
st.caption("AI-Powered Itinerary Planner for India")

# --- Sidebar (Inputs) ---
with st.sidebar:
    st.header("Plan Your Trip")
    places_input = st.text_area("Destinations (in order)", "Delhi, Manali, Leh", height=100)
    transport_mode = st.selectbox("Mode of Transport", ["Personal Bike", "Personal Car", "Rented Bike", "Rented Car", "Public Transport"])
    st.subheader("Dates")
    start_date = st.date_input("Start", datetime.date.today())
    is_flexible = st.checkbox("I have a flexible end date", value=True)
    if is_flexible:
        end_date = None
        st.caption("We will suggest an optimal duration for your trip.")
    else:
        end_d_default = start_date + datetime.timedelta(days=7)
        end_date = st.date_input("End", end_d_default)
    st.subheader("Preferences")
    hotel_pref = st.select_slider("Hotel Class", ["Cheap", "Standard", "Branded"], value="Standard")
    food_pref = st.select_slider("Food Class", ["Cheap", "Standard", "Branded"], value="Standard")
    generate_btn = st.button("🚀 Generate Itinerary", type="primary", use_container_width=True)

# --- Main Display Area ---
if generate_btn:
    places_list = [p.strip() for p in places_input.split(',') if p.strip()]
    is_peak = start_date.month in [5, 6, 12, 1]
    
    if len(places_list) < 2:
        st.error("Please enter at least two destinations.")
    else:
        structured_data = generate_structured_itinerary(places_list, hotel_pref, food_pref, transport_mode)
        generated_duration = structured_data[-1]['day_num']
        
        if is_flexible:
            final_duration = generated_duration
            st.info(f"👍 Based on your route, we suggest an optimal **{final_duration}-day** trip.")
        else:
            final_duration = (end_date - start_date).days + 1
            if final_duration <= 0: st.error("Error: End date must be after the start date."); st.stop()
            elif final_duration < generated_duration: st.warning(f"Note: Your {final_duration}-day plan is very rushed! Our suggested plan is {generated_duration} days.")
            elif final_duration > generated_duration: st.info(f"You have {final_duration - generated_duration} extra buffer days. Perfect for rest!")

        budget = calculate_total_budget(transport_mode, hotel_pref, food_pref, final_duration, is_peak)
        
        col_b1, col_b2, col_b3 = st.columns(3)
        col_b1.metric("Total Budget", f"₹{budget:,}")
        col_b2.metric("Duration", f"{final_duration} Days")
        col_b3.metric("Travel Mode", transport_mode)
        st.divider()
        
        # --- NEW: Advanced Route Map with Pydeck ---
        st.subheader("🗺️ Your Visual Route")
        
        # 1. Get Data
        route_coords, valid_places_data = get_dummy_coordinates(places_list)
        
        if len(route_coords) > 0:
            # 2. Define Layers
            
            # Layer 1: The Path (Line)
            layer_path = pdk.Layer(
                "PathLayer",
                data=[{"path": route_coords, "name": "Route"}],
                pickable=True,
                get_color=[255, 75, 75], # Reddish color
                width_scale=20,
                width_min_pixels=3,
                get_path="path",
                get_width=5000,
            )
            
            # Layer 2: The Cities (Dots)
            layer_scatter = pdk.Layer(
                "ScatterplotLayer",
                data=valid_places_data,
                get_position="coordinates",
                get_color=[0, 128, 255], # Blue color
                get_radius=15000, # Radius in meters
                pickable=True,
            )
            
            # 3. Set View State (Center the map)
            # Center on the first city in the list
            initial_view_state = pdk.ViewState(
                latitude=route_coords[0][1],
                longitude=route_coords[0][0],
                zoom=5,
                pitch=0,
            )
            
            # 4. Render
            r = pdk.Deck(
                layers=[layer_path, layer_scatter],
                initial_view_state=initial_view_state,
                tooltip={"text": "{name}"}, # Show city name on hover
                map_style="mapbox://styles/mapbox/outdoors-v11"
            )
            st.pydeck_chart(r)
            st.caption("Map shows the direct path between your destinations.")
        else:
            st.warning("Could not find coordinates for these cities in the prototype database.")
        
        # --- END Map Section ---

        perms = get_special_permissions(places_list)
        if "No special permits" not in perms[0]:
            st.warning("⚠️ **Permits Required:** " + ", ".join(perms))
        
        if transport_mode in ["Rented Bike", "Rented Car"]:
            with st.expander(f"**Rental Options for {transport_mode} from {places_list[0]}**", expanded=True):
                rentals = get_rental_options(places_list[0], transport_mode)
                r_c1, r_c2, r_c3 = st.columns(3)
                r_c1.markdown("**Agency**"); r_c2.markdown("**Example Model**"); r_c3.markdown("**Est. Price/Day**")
                for rental in rentals:
                    r_c1, r_c2, r_c3 = st.columns(3)
                    r_c1.write(rental['name']); r_c2.write(rental['model']); r_c3.write(f"₹{rental['price']:,}")
        
        st.subheader("🗓️ Your Day-by-Day Plan")
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
                            if event['icon'] == "HOTEL":
                                st.info(f"**{event['time']} | Stay:** {event['activity']}")
                            else:
                                st.write(f"{event['icon']} **{event['time']}:** {event['activity']}")
                        with st.expander("💰 **Show Daily Budget Breakdown**"):
                            budget = item['budget']
                            st.markdown(f"* **Stay:** `₹{budget['stay']:,}`\n* **Transport:** `₹{budget['fuel_transport']:,}`\n* **Food:** `₹{budget['food']:,}`\n* **Contingency:** `₹{budget['contingency']:,}`\n* **Day Total:** `₹{budget['total_per_day']:,}`")
        
        st.success("Trip planning complete! Have a safe adventure.")

elif not generate_btn:
    st.info("👈 **Welcome! Use the sidebar menu to plan your adventure.**")
    st.subheader("How It Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🗺️ 1. Plan Your Route")
        st.write("Enter your destinations in order, separated by commas (e.g., `Kolkata, Delhi, Leh`).")
    with col2:
        st.markdown("### ⚙️ 2. Set Your Style")
        st.write("Choose your transport, budget class, and let us know if your dates are flexible.")
    with col3:
        st.markdown("### 🚀 3. Get Your Itinerary")
        st.write("Receive a detailed day-by-day plan with budgets, rental options, and sightseeing tips.")
    st.divider()
    st.subheader("Inspiration for Your Next Ride")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80", caption="Explore Incredible India")
    with col2:
        st.image("https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80", caption="Adventure Awaits")
