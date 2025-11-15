import streamlit as st
import datetime
import time
import random

# --- (A) V2 Placeholder/Simulation Functions ---

def generate_detailed_dummy_itinerary(places_list, hotel_pref, food_pref):
    """
    Simulates a detailed, day-by-day itinerary with generic recommendations.
    This is a "smart" prototype, but the data is still fake.
    """
    
    # --- Fake database of recommendations ---
    hotel_options = {
        "Cheap": ["a local guesthouse", "a Zostel or backpacker hostel", "an OYO Rooms"],
        "Standard": ["a 3-Star hotel like 'Hotel Palace'", "a 'Clarks Inn' or 'Country Inn'"],
        "Branded": ["the 'Marriott'", "a 'Radisson Blu' or 'Taj' property"]
    }
    
    food_options = {
        "Cheap": ["a popular local dhaba", "a street food market", "a Giani's or local tea stall"],
        "Standard": ["a 'Bikanervala' or 'Haldiram's'", "a good multi-cuisine restaurant", "a 'Cafe Coffee Day'"],
        "Branded": ["a high-end restaurant in a 5-star hotel", "a 'Barbeque Nation'", "a 'Starbucks'"]
    }
    
    # --- Itinerary Generation Logic ---
    itinerary_steps = []
    day_counter = 1
    
    if len(places_list) < 2:
        return ["Please enter at least two destinations to create a route."]
        
    itinerary_steps.append(f"### 🏁 Your Trip from {places_list[0]} to {places_list[-1]} ###")
    
    # Loop through each "leg" of the journey (e.g., Delhi -> Manali)
    for i in range(len(places_list) - 1):
        origin = places_list[i]
        destination = places_list[i+1]
        
        itinerary_steps.append(f"\n---\n**Leg {i+1}: {origin} to {destination}**")
        
        # --- This is the core "dummy" logic ---
        # We pretend every leg is a 2-day journey for this prototype.
        # A real app would use the Google Maps API to get the *real* distance
        # and divide it by a 300-400km daily average.
        
        mid_point = f"A major city halfway (e.g., Ambala, Lucknow, etc.)"
        
        # Day 1 of the leg
        itinerary_steps.append(f"**Day {day_counter}: {origin} ➔ {mid_point}**")
        itinerary_steps.append(f"* **Morning:** Start early from {origin}. Enjoy the drive!")
        itinerary_steps.append(f"* **Lunch:** Stop at {random.choice(food_options[food_pref])} on the highway.")
        itinerary_steps.append(f"* **Evening:** Arrive in {mid_point}. Check into your hotel.")
        itinerary_steps.append(f"* **Stay:** We recommend {random.choice(hotel_options[hotel_pref])}.")
        itinerary_steps.append(f"* **Dinner:** Have dinner at {random.choice(food_options[food_pref])} near your hotel.")
        day_counter += 1
        
        # Day 2 of the leg
        itinerary_steps.append(f"**Day {day_counter}: {mid_point} ➔ {destination}**")
        itinerary_steps.append(f"* **Morning:** After breakfast, start the second half of your journey.")
        itinerary_steps.append(f"* **Lunch:** Stop at {random.choice(food_options[food_pref])} for a quick meal.")
        itinerary_steps.append(f"* **Evening:** Arrive in {destination}! You've reached your destination for this leg.")
        itinerary_steps.append(f"* **Stay:** Check into {random.choice(hotel_options[hotel_pref])} for your stay in {destination}.")
        day_counter += 1
        
    itinerary_steps.append("\n---\n**Trip Complete!**")
    return itinerary_steps

def get_special_permissions(places_list):
    """
    This function remains crucial and would be the same in a real app.
    It's a manually curated database of information.
    """
    permission_db = {
        "Leh": "Inner Line Permit (ILP) required for areas like Pangong Tso & Nubra Valley. Check official Leh district website.",
        "Ladakh": "Inner Line Permit (ILP) required. Apply online.",
        "Manali": "Permit required for Rohtang Pass (check online portal). Not needed if just staying in Manali.",
        "Sikkim": "Protected Area Permit (PAP) required for North Sikkim (e.g., Gurudongmar Lake). Check Sikkim Tourism website.",
        "Tawang": "Inner Line Permit (ILP) required for Arunachal Pradesh. Apply online."
    }
    
    route_permissions = []
    for place in places_list:
        # Check if any of our db_keys are in the user's place names
        for db_key in permission_db:
            if db_key.lower() in place.lower().strip():
                route_permissions.append(f"For {place}: {permission_db[db_key]}")

    if not route_permissions:
        route_permissions = ["No special permissions noted for this route. Always double-check official government websites before travel."]
    
    return route_permissions

def calculate_budget(mode, hotel_pref, food_pref, duration_days, is_peak_season):
    """
    Simulates a budget calculation based on user preferences.
    This logic remains the same as V1.
    """
    # Base daily costs (dummy values in INR)
    transport_cost_per_day = {
        "Personal Bike": 1200, "Personal Car": 2500, "Rented Bike": 1800,
        "Rented Car": 4000, "Public Transport (Bus/Train/Flight)": 3000
    }
    hotel_cost_per_night = {"Cheap": 1000, "Standard": 2800, "Branded": 8000}
    food_cost_per_day = {"Cheap": 500, "Standard": 1500, "Branded": 4000}

    # Calculate base cost
    total_transport = transport_cost_per_day.get(mode, 0) * duration_days
    total_hotel = hotel_cost_per_night.get(hotel_pref, 0) * (duration_days - 1) 
    total_food = food_cost_per_day.get(food_pref, 0) * duration_days
    base_budget = total_transport + total_hotel + total_food
    
    # Add peak season multiplier
    if is_peak_season:
        final_budget = base_budget * 1.30
        season_note = "Includes a 30% estimated peak season surcharge."
    else:
        final_budget = base_budget
        season_note = "Off-season pricing applied."

    return int(final_budget), season_note

# --- (B) Streamlit Application UI ---

st.set_page_config(page_title="Your Travel and Adventure", layout="wide")

st.title("🏞️ YOUR TRAVEL AND ADVENTURE 🗺️")
st.subheader("Your personalized itinerary planner for India")

main_choice = st.selectbox(
    "What are you looking for today?",
    ("Select an option", "Build a Custom Itinerary", "Find Hotel Deals", "Browse Pre-made Packages")
)
st.divider()

if main_choice == "Build a Custom Itinerary":
    
    st.header("Build Your Custom Itinerary")
    col1, col2 = st.columns(2)

    with col1:
        # --- POINT 3: UNLIMITED LOCATIONS ---
        # We now use text_input, solving the limited list problem.
        places_input = st.text_input(
            "Enter the places you want to visit, in order, separated by commas:",
            placeholder="e.g., Kolkata, Varanasi, Delhi, Manali, Leh"
        )
        
        transport_mode = st.selectbox(
            "How do you plan to travel?",
            ("Select a mode", "Personal Bike", "Personal Car", "Rented Bike", "Rented Car", "Public Transport (Bus/Train/Flight)")
        )

    with col2:
        st.markdown("**Select Your Travel Dates**")
        start_date = st.date_input("Start Date", min_value=datetime.date.today())
        end_date = st.date_input("End Date", min_value=start_date)
        
        duration = (end_date - start_date).days + 1
        is_peak = False
        if start_date.month in [12, 1, 4, 5, 6]:
            is_peak = True

        st.caption(f"Total duration: {duration} days")
        if is_peak: st.caption("Note: Your dates fall in a potential peak season.")

    st.markdown("### Select Your Budget Preferences")
    col_hotel, col_food = st.columns(2)
    with col_hotel:
        hotel_preference = st.radio("Hotel Preference", ("Cheap", "Standard", "Branded"), horizontal=True)
    with col_food:
        food_preference = st.radio("Restaurant Preference", ("Cheap", "Standard", "Branded"), horizontal=True)

    st.divider()

    if st.button("Generate My Itinerary", type="primary", use_container_width=True):
        
        # Process the new text input
        places_list = [place.strip() for place in places_input.split(',') if place.strip()]
        
        if not places_list or len(places_list) < 2:
            st.error("Please enter at least two places (e.g., 'Delhi, Manali').")
        elif transport_mode == "Select a mode":
            st.error("Please select a mode of transport.")
        elif duration <= 0:
             st.error("Please select a valid date range (at least 1 day).")
        else:
            with st.spinner("Generating your detailed itinerary..."):
                time.sleep(2) # Simulate processing
                
                # --- CALL THE NEW V2 FUNCTIONS ---
                
                # 1. Generate the detailed day-by-day plan
                detailed_itinerary = generate_detailed_dummy_itinerary(places_list, hotel_preference, food_preference)
                
                # 2. Get permissions
                permissions = get_special_permissions(places_list)
                
                # 3. Get budget
                estimated_budget, season_note = calculate_budget(
                    transport_mode, hotel_preference, food_preference, duration, is_peak
                )

                st.success("Your Detailed Itinerary is Ready!")

                # --- Display the new detailed output ---
                
                st.subheader(f"Your Custom {duration}-Day Trip Plan")
                
                # Display Budget
                st.metric(
                    label="Estimated Total Budget",
                    value=f"₹{estimated_budget:,}",
                    help=f"Based on {duration} days, {transport_mode} transport, {hotel_preference} hotels, {food_preference} food. {season_note}"
                )
                
                # Display Permissions (Point 7)
                st.markdown("#### 📜 Special Permissions & Advisories")
                for perm in permissions:
                    st.warning(f"**Alert:** {perm}")

                # Display Detailed Itinerary (Point 1 & 2)
                st.markdown("#### 🗺️ Detailed Day-by-Day Plan")
                st.info("Note: This is a *simulated* plan. Distances and mid-points are examples. A real app would use live map data.")
                
                for line in detailed_itinerary:
                    st.markdown(line)

# --- (Other placeholder sections) ---
elif main_choice == "Find Hotel Deals":
    st.header("Find Hotel Deals")
    st.info("This feature is coming soon!")
elif main_choice == "Browse Pre-made Packages":
    st.header("Browse Pre-made Packages")
    st.info("This feature is coming soon!")
else:
    st.info("Please select an option from the dropdown above to get started.")
