import streamlit as st
import datetime
import time
import random

# --- (A) V3: Enhanced Simulation & Data Functions ---

def get_sightseeing_spots(location):
    """
    Returns a list of sightseeing spots for a given location.
    (Dummy Database)
    """
    sightseeing_db = {
        "delhi": ["India Gate", "Red Fort", "Qutub Minar", "Lotus Temple"],
        "agra": ["Taj Mahal", "Agra Fort", "Mehtab Bagh"],
        "jaipur": ["Hawa Mahal", "Amber Fort", "City Palace", "Jantar Mantar"],
        "manali": ["Hadimba Temple", "Solang Valley", "Mall Road", "Jogini Falls"],
        "leh": ["Pangong Lake", "Shanti Stupa", "Leh Palace", "Magnetic Hill"],
        "ladakh": ["Nubra Valley", "Thiksey Monastery", "Khardung La Pass"],
        "goa": ["Baga Beach", "Fort Aguada", "Basilica of Bom Jesus"],
        "kerala": ["Alleppey Backwaters", "Munnar Tea Gardens", "Varkala Cliff"],
        "kolkata": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Kali Temple"],
        "varanasi": ["Kashi Vishwanath Temple", "Ganga Aarti at Dashashwamedh Ghat"],
        "jammu": ["Raghunath Temple", "Bahu Fort"],
        "srinagar": ["Dal Lake", "Shankaracharya Temple", "Mughal Gardens"]
    }
    
    # Normalize input to lowercase to match keys
    loc_lower = location.lower().strip()
    
    # Return spots if found, otherwise generic suggestions
    if loc_lower in sightseeing_db:
        return sightseeing_db[loc_lower]
    else:
        return ["Local City Center", "Famous Local Market", "Heritage Sites"]

def generate_structured_itinerary(places_list, hotel_pref, food_pref):
    """
    Generates a LIST of DICTIONARIES. 
    This structure allows the UI to render beautiful cards instead of just text.
    """
    
    itinerary_data = []
    day_counter = 1
    
    # Recommendation styles based on budget
    stays = {
        "Cheap": ["Zostel", "Backpacker Hostel", "Local Guest House", "OYO Rooms"],
        "Standard": ["3-Star City Hotel", "Lemon Tree Hotel", "Ginger Hotel", "Comfort Inn"],
        "Branded": ["Marriott", "Taj Vivanta", "Radisson Blu", "Hyatt Regency"]
    }
    
    eateries = {
        "Cheap": ["Highway Dhaba", "Local Street Food Stall", "Railway Canteen"],
        "Standard": ["Haldiram's", "Barbeque Nation", "Main Market Cafe"],
        "Branded": ["5-Star Hotel Buffet", "Fine Dining Restaurant", "Specialty Continental Cafe"]
    }

    # --- Loop through the journey ---
    for i in range(len(places_list) - 1):
        origin = places_list[i]
        destination = places_list[i+1]
        
        # Create a "Section Header" for the Leg
        itinerary_data.append({
            "type": "leg_header", 
            "text": f"Leg {i+1}: {origin} ➔ {destination}"
        })
        
        # --- DAY 1 of Leg (Travel & Sightseeing at Origin/Midpoint) ---
        day_plan = []
        
        # 1. Breakfast
        day_plan.append({"icon": "☕", "time": "08:00 AM", "activity": f"Breakfast at {origin}."})
        
        # 2. Sightseeing (If available for Origin)
        spots = get_sightseeing_spots(origin)
        if spots:
            spot_text = ", ".join(spots[:2]) # Take top 2 spots
            day_plan.append({"icon": "📸", "time": "10:00 AM", "activity": f"Visit local gems: {spot_text}."})
        
        # 3. Travel
        mid_point = "Scenic Highway Stop"
        day_plan.append({"icon": "🚗", "time": "01:00 PM", "activity": f"Drive towards {destination}. Stop for lunch at a {random.choice(eateries[food_pref])}."})
        
        # 4. Evening Stay
        day_plan.append({"icon": "HOTEL", "time": "07:00 PM", "activity": f"Halt at {mid_point}. Check into a {random.choice(stays[hotel_pref])}."})
        
        itinerary_data.append({
            "type": "day_card",
            "day_num": day_counter,
            "route": f"{origin} ➔ {mid_point}",
            "events": day_plan
        })
        day_counter += 1
        
        # --- DAY 2 of Leg (Reach Destination & Explore) ---
        day_plan_2 = []
        
        # 1. Morning Drive
        day_plan_2.append({"icon": "🛣️", "time": "09:00 AM", "activity": "Resume journey. Enjoy the landscape."})
        
        # 2. Arrival
        day_plan_2.append({"icon": "🏁", "time": "02:00 PM", "activity": f"Arrive in **{destination}**! Check into your {hotel_pref} hotel."})
        
        # 3. Destination Sightseeing
        dest_spots = get_sightseeing_spots(destination)
        if dest_spots:
             spot_text = ", ".join(dest_spots) 
             day_plan_2.append({"icon": "📸", "time": "04:00 PM", "activity": f"Explore {destination}: Visit {spot_text}."})
        
        # 4. Dinner
        day_plan_2.append({"icon": "🍽️", "time": "08:30 PM", "activity": f"Dinner at a {random.choice(eateries[food_pref])} in {destination}."})
        
        itinerary_data.append({
            "type": "day_card",
            "day_num": day_counter,
            "route": f"{mid_point} ➔ {destination}",
            "events": day_plan_2
        })
        day_counter += 1

    return itinerary_data

def calculate_budget(mode, hotel_pref, food_pref, duration_days, is_peak_season):
    # (Same logic as before)
    transport_cost = {"Personal Bike": 1200, "Personal Car": 2500, "Rented Bike": 1800, "Rented Car": 4000, "Public Transport (Bus/Train/Flight)": 3000}
    hotel_cost = {"Cheap": 1000, "Standard": 2800, "Branded": 8000}
    food_cost = {"Cheap": 500, "Standard": 1500, "Branded": 4000}
    
    base = (transport_cost.get(mode, 2000) * duration_days) + (hotel_cost.get(hotel_pref, 2000) * (duration_days-1)) + (food_cost.get(food_pref, 1000) * duration_days)
    final = base * 1.30 if is_peak_season else base
    return int(final)

def get_special_permissions(places_list):
    # (Same logic as before)
    db = {"leh": "ILP Required", "ladakh": "ILP Required", "manali": "Rohtang Permit", "sikkim": "PAP Required", "tawang": "ILP Required"}
    perms = []
    for p in places_list:
        for k, v in db.items():
            if k in p.lower(): perms.append(f"{p}: {v}")
    return perms if perms else ["No special permits found in database."]

# --- (B) Streamlit UI ---
st.set_page_config(page_title="Your Travel and Adventure", layout="wide", page_icon="🏞️")

# Custom CSS to make it look "App-like"
st.markdown("""
<style>
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    div[data-testid="stExpander"] { border: none; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

st.title("🏞️ YOUR TRAVEL AND ADVENTURE")
st.caption("AI-Powered Itinerary Planner for India")

# --- Sidebar for Inputs (Cleaner Layout) ---
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
        budget = calculate_budget(transport_mode, hotel_pref, food_pref, duration, is_peak)
        
        col_b1, col_b2, col_b3 = st.columns(3)
        col_b1.metric("Total Budget", f"₹{budget:,}")
        col_b2.metric("Duration", f"{duration} Days")
        col_b3.metric("Travel Mode", transport_mode)
        
        st.divider()
        
        # 2. Permissions Section
        perms = get_special_permissions(places_list)
        if "No special permits" not in perms[0]:
            st.warning("⚠️ **Permits Required:** " + ", ".join(perms))
        
        # 3. The NEW Structured Itinerary Display
        st.subheader("🗺️ Your Day-by-Day Plan")
        
        structured_data = generate_structured_itinerary(places_list, hotel_pref, food_pref)
        
        for item in structured_data:
            
            # If it's a Header (e.g., Leg 1)
            if item["type"] == "leg_header":
                st.markdown(f"### {item['text']}")
            
            # If it's a Day Card
            elif item["type"] == "day_card":
                # This 'with st.container' creates the visual box
                with st.container(border=True):
                    c_day, c_details = st.columns([1, 5])
                    
                    with c_day:
                        st.markdown(f"## Day {item['day_num']}")
                        st.caption(item['route'])
                    
                    with c_details:
                        # Render events as a clean list
                        for event in item['events']:
                            icon = event['icon']
                            # If icon is HOTEL, we make it look distinct
                            if icon == "HOTEL":
                                st.info(f"**{event['time']} | Stay:** {event['activity']}")
                            else:
                                st.write(f"{icon} **{event['time']}:** {event['activity']}")

        st.success("Trip planning complete! Drive safe.")

elif not generate_btn:
    # Placeholder when app loads
    st.info("👈 Use the sidebar menu to plan your adventure!")
    col1, col2 = st.columns(2)
    
    # FIXED SECTION: Added actual image URLs instead of placeholder text
    with col1:
        st.image("https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800&q=80", caption="Explore Incredible India")
    with col2:
        st.image("https://images.unsplash.com/photo-1558981403-c5f9899a28bc?auto=format&fit=crop&w=800&q=80", caption="Adventure Awaits")
