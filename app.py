import streamlit as st
import datetime
import time

# --- (A) Placeholder/Simulation Functions ---
# In a real app, these functions would call external APIs (Google Maps, Hotel APIs, etc.)
# or query a complex database. For this prototype, they return dummy data.

def get_route_and_details(places_list, mode):
    """
    Simulates fetching a route, sightseeing spots, and permissions.
    """
    # 1. Simulate Route Generation
    best_route = " -> ".join(places_list)
    alt_route = " -> ".join(reversed(places_list)) + " (Alternate Route)"
    
    # 2. Simulate Sightseeing Recommendations
    # (Dummy data - would be queried based on route)
    sightseeing_db = {
        "Delhi": ["India Gate", "Qutub Minar", "Humayun's Tomb"],
        "Manali": ["Solang Valley", "Hadimba Temple", "Rohtang Pass (requires permit)"],
        "Leh": ["Pangong Tso", "Khardung La", "Nubra Valley"],
        "Goa": ["Baga Beach", "Old Goa Churches", "Dudhsagar Falls"],
        "Jaipur": ["Hawa Mahal", "Amer Fort", "City Palace"],
    }
    
    route_sightseeing = []
    for place in places_list:
        if place in sightseeing_db:
            route_sightseeing.extend(sightseeing_db[place])
            
    if not route_sightseeing:
        route_sightseeing = ["No specific sightseeing recommendations available for this custom route."]

    # 3. Simulate Permission Requirements
    # (Dummy data - would be queried based on route and dates)
    permission_db = {
        "Leh": "Inner Line Permit (ILP) required for areas like Pangong Tso & Nubra Valley.",
        "Manali": "Permit required for Rohtang Pass (check online portal).",
        "Sikkim": "Protected Area Permit (PAP) required for North Sikkim (e.g., Gurudongmar Lake)."
    }
    
    route_permissions = []
    for place in places_list:
        if place in permission_db:
            route_permissions.append(f"For {place}: {permission_db[place]}")
            
    if not route_permissions:
        route_permissions = ["No special permissions noted for this route. Always double-check official government websites before travel."]

    return best_route, alt_route, route_sightseeing, route_permissions

def calculate_budget(mode, hotel_pref, food_pref, duration_days, is_peak_season):
    """
    Simulates a budget calculation based on user preferences.
    """
    # Base daily costs (dummy values in INR)
    transport_cost_per_day = {
        "Personal Bike": 1200,  # Fuel + Maintenance
        "Personal Car": 2500,   # Fuel + Tolls + Maintenance
        "Rented Bike": 1800,
        "Rented Car": 4000,
        "Public Transport (Bus/Train/Flight)": 3000 # Averaged
    }
    
    hotel_cost_per_night = {
        "Cheap": 1000,
        "Standard": 2800,
        "Branded": 8000
    }
    
    food_cost_per_day = {
        "Cheap": 500,       # Local dhabas, street food
        "Standard": 1500,   # Mid-range restaurants
        "Branded": 4000     # Fine dining, high-end cafes
    }

    # Calculate base cost
    total_transport = transport_cost_per_day.get(mode, 0) * duration_days
    total_hotel = hotel_cost_per_night.get(hotel_pref, 0) * (duration_days - 1) # Nights = Days - 1
    total_food = food_cost_per_day.get(food_pref, 0) * duration_days
    
    base_budget = total_transport + total_hotel + total_food
    
    # Add peak season multiplier (Point 9)
    if is_peak_season:
        # Applying a 30% surcharge for peak season
        final_budget = base_budget * 1.30
        season_note = "Includes a 30% estimated peak season surcharge."
    else:
        final_budget = base_budget
        season_note = "Off-season pricing applied."

    return int(final_budget), season_note

# --- (B) Streamlit Application UI ---

# Page configuration
st.set_page_config(page_title="Your Travel and Adventure", layout="wide")

# Point 1: Title
st.title("🏞️ YOUR TRAVEL AND ADVENTURE 🗺️")
st.subheader("Your personalized itinerary planner for India")

# Point 2: Main service choice
main_choice = st.selectbox(
    "What are you looking for today?",
    ("Select an option", "Build a Custom Itinerary", "Find Hotel Deals", "Browse Pre-made Packages")
)

st.divider()

# --- Main Feature: Itinerary Builder ---
if main_choice == "Build a Custom Itinerary":
    
    st.header("Build Your Custom Itinerary")

    # We use columns to organize the inputs neatly
    col1, col2 = st.columns(2)

    with col1:
        # Point 4: Places to visit
        # For this prototype, we use a predefined list of popular Indian destinations.
        # A real app would use a search box linked to a map API.
        indian_places = [
            "Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", 
            "Goa", "Jaipur", "Agra", "Shimla", "Manali", "Leh", 
            "Srinagar", "Rishikesh", "Udaipur", "Kochi", "Sikkim"
        ]
        
        places_to_visit = st.multiselect(
            "Select the main places you want to visit (in order):",
            options=indian_places,
            help="Select the cities/destinations you plan to cover."
        )

        # Point 3: Mode of Transport
        transport_mode = st.selectbox(
            "How do you plan to travel?",
            (
                "Select a mode", 
                "Personal Bike", 
                "Personal Car", 
                "Rented Bike", 
                "Rented Car", 
                "Public Transport (Bus/Train/Flight)"
            )
        )

    with col2:
        # Point 9: Dates
        st.markdown("**Select Your Travel Dates**")
        start_date = st.date_input("Start Date", min_value=datetime.date.today())
        end_date = st.date_input("End Date", min_value=start_date)

        # Calculate duration and check for peak season
        duration = (end_date - start_date).days + 1
        is_peak = False
        # Dummy peak season logic (e.g., Dec-Jan, Apr-Jun are peak)
        if start_date.month in [12, 1, 4, 5, 6]:
            is_peak = True

        st.caption(f"Total duration: {duration} days")
        if is_peak:
            st.caption("Note: Your dates fall in a potential peak season.")

    # Point 6: Preferences
    st.markdown("### Select Your Budget Preferences")
    col_hotel, col_food = st.columns(2)
    with col_hotel:
        hotel_preference = st.radio(
            "Hotel Preference",
            ("Cheap", "Standard", "Branded"),
            horizontal=True,
            help="Cheap (Hostels/Guesthouses), Standard (3-Star), Branded (4-Star+)"
        )
    with col_food:
        food_preference = st.radio(
            "Restaurant Preference",
            ("Cheap", "Standard", "Branded"),
            horizontal=True,
            help="Cheap (Street Food/Dhabas), Standard (Mid-Range Cafes), Branded (Fine Dining)"
        )

    st.divider()

    # --- Generate Button and Output ---
    if st.button("Generate My Itinerary", type="primary", use_container_width=True):
        
        # Validation checks
        if not places_to_visit:
            st.error("Please select at least one place to visit.")
        elif transport_mode == "Select a mode":
            st.error("Please select a mode of transport.")
        elif duration <= 0:
             st.error("Please select a valid date range (at least 1 day).")
        else:
            with st.spinner("Generating your personalized itinerary... This may take a moment."):
                time.sleep(2) # Simulate processing time
                
                # Call placeholder functions to get data
                best_route, alt_route, sightseeing, permissions = get_route_and_details(places_to_visit, transport_mode)
                
                # Point 5: Estimated Budget
                estimated_budget, season_note = calculate_budget(
                    transport_mode, hotel_preference, food_preference, duration, is_peak
                )

                st.success("Your Itinerary is Ready!")

                st.subheader(f"Your Custom {duration}-Day Trip")
                
                # Display Budget (Point 5, 6, 9)
                st.metric(
                    label="Estimated Total Budget",
                    value=f"₹{estimated_budget:,}",
                    help=f"Based on {duration} days, {transport_mode} transport, {hotel_preference} hotels, {food_preference} food. {season_note}"
                )
                
                # Display Route (Point 4)
                st.markdown("#### 🗺️ Proposed Route")
                st.info(f"**Best Route:** {best_route}")
                st.info(f"**Alternate Route:** {alt_route}")
                
                # Display Sightseeing (Point 8)
                st.markdown("#### 📍 Recommended Sightseeing")
                for spot in sightseeing:
                    st.markdown(f"* {spot}")
                
                # Display Permissions (Point 7)
                st.markdown("#### 📜 Special Permissions & Advisories")
                for perm in permissions:
                    st.warning(f"**Alert:** {perm}")

# --- Placeholder sections for other features ---
elif main_choice == "Find Hotel Deals":
    st.header("Find Hotel Deals")
    st.info("This feature is coming soon! You will be able to search for hotels across India.")
    
    st.text_input("Enter city or region:")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Check-in Date")
    with col2:
        st.date_input("Check-out Date")
    st.button("Search Hotels")

elif main_choice == "Browse Pre-made Packages":
    st.header("Browse Pre-made Packages")
    st.info("This feature is coming soon! This section will show curated packages for all travel styles.")
    
    # Example package layout
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1587740990710-0f6f691b0c03?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NzA5OHwwfDF8c2VhcmNofDEwfHxsYWRha2glMjBiaWtlfGVufDB8fHx8MTY5OTgxNDc4M3ww&ixlib=rb-4.0.3&q=80&w=1080", 
                 caption="Manali-Leh Bike Adventure")
    with col2:
        st.image("https://images.unsplash.com/photo-1507525428034-b723a996c9c8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NzA5OHwwfDF8c2VhcmNofDF8fGdvYSUyMGJlYWNofGVufDB8fHx8MTY5OTgxNDgxMHww&ixlib=rb-4.0.3&q=80&w=1080", 
                 caption="Goa Coastal Escape")

else:
    st.info("Please select an option from the dropdown above to get started.")