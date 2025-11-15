import streamlit as st
import datetime
import time
import random

# --- (A) V5: Enhanced Simulation & Data Functions ---

def get_rental_options(origin_city, transport_mode):
    # (Same as before)
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
    # (Same as before)
    costs = {}
    costs['fuel_transport'] = {"Personal Bike": 1200, "Personal Car": 2500, "Rented Bike": 1800, "Rented Car": 4000, "Public Transport": 2800}.get(mode, 2000)
    costs['stay'] = {"Cheap": 1200, "Standard": 2800, "Branded": 8000}.get(hotel_pref, 2000)
    costs['food'] = {"Cheap": 500, "Standard": 1500, "Branded": 4000}.get(food_pref, 1000)
    subtotal = costs['fuel_transport'] + costs['stay'] + costs['food']
    costs['contingency'] = int(subtotal * 0.15)
    costs['total_per_day'] = subtotal + costs['contingency']
    return costs

def calculate_total_budget(mode, hotel_pref, food_pref, duration_days, is_peak_season):
    # (Same as before)
    daily = get_daily_costs(mode, hotel_pref, food_pref)
    total_fuel_transport = daily['fuel_transport'] * duration_days
    total_food = daily['food'] * duration_days
    total_contingency = daily['contingency'] * duration_days
    total_stay = daily['stay'] * (duration_days - 1)
    base_budget = total_fuel_transport + total_food + total_stay + total_contingency
    final_budget = base_budget * 1.30 if is_peak_season else base_budget
    return int(final_budget)

def get_sightseeing_spots(location):
    # (Same as before)
    sightseeing_db = {
        "delhi": ["India Gate", "Red Fort", "Qutub Minar"], "agra": ["Taj Mahal", "Agra Fort"],
        "jaipur": ["Hawa Mahal", "Amber Fort"], "manali": ["Hadimba Temple", "Solang Valley"],
        "leh": ["Pangong Lake", "Shanti Stupa"], "ladakh": ["Nubra Valley", "Khardung La"],
        "kolkata": ["Victoria Memorial", "Howrah Bridge"], "varanasi": ["Kashi Vishwanath Temple", "Ganga Aarti"],
        "jammu": ["Raghath Temple", "Bahu Fort"], "srinagar": ["Dal Lake", "Mughal Gardens"]
    }
    loc_lower = location.lower().strip()
    return sightseeing_db.get(loc_lower, ["Local City Center", "Famous Local Market"])

def get_special_permissions(places_list):
    # (Same as before)
    db = {"leh": "ILP Required", "ladakh": "ILP Required", "manali": "Rohtang Permit", "sikkim": "PAP Required", "tawang": "ILP Required"}
    perms = [f"{p}: {v}" for p in places_list for k, v in db.items() if k in p.lower()]
    return perms if perms else ["No special permits found in database."]


# --- NEW: Function for Public Transport Simulation ---
def get_public_transport_recommendation(origin, destination):
    """
    Simulates the best public transport mode for a leg.
    """
    origin, dest = origin.lower(), destination.lower()
    
    if "leh" in dest or "ladakh" in dest:
        return f"Fly from {origin.capitalize()} to Leh (IXL). This is the fastest and most reliable route."
    if "delhi" in origin and "manali" in dest:
        return f"Take an overnight AC Volvo bus (e.g., HPTDC) from ISBT Kashmere Gate, Delhi."
    if "delhi" in origin and "agra" in dest:
        return "Take the morning Shatabdi Express or Gatimaan Express train. It's fast (2 hours)."
    if "kolkata" in origin and "delhi" in dest:
        return f"Take a direct flight (CCU -> DEL) or an overnight train (e.g., Rajdhani Express)."
    
    # Generic fallback
    return f"Look for overnight state transport buses or direct trains from {origin.capitalize()} to {destination.capitalize()}."


# --- UPDATED: Itinerary function now handles Public Transport ---
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
        
        # --- Generate Day 1 (Travel Day) ---
        day_plan = []
        
        # --- Logic fork based on transport mode ---
        if transport_mode == "Public Transport":
            recommendation = get_public_transport_recommendation(origin, destination)
            day_plan.append({"icon": "☕", "time": "08:00 AM", "activity": f"Breakfast at {origin} and head to the bus/train station or airport."})
            spots = get_sightseeing_spots(origin)
            day_plan.append({"icon": "📸", "time": "11:00 AM", "activity": f"Quickly visit: {', '.join(spots[:1])}."})
            day_plan.append({"icon": "🎫", "time": "02:00 PM", "activity": f"**Travel:** {recommendation}"})
            day_plan.append({"icon": "HOTEL", "time": "09:00 PM", "activity": "Arrive at your destination or travel overnight."})
        else: # Personal or Rented
            day_plan.append({"icon": "☕", "time": "08:00 AM", "activity": f"Breakfast at {origin}."})
            spots = get_sightseeing_spots(origin)
            day_plan.append({"icon": "📸", "time": "10:00 AM", "activity": f"Visit: {', '.join(spots[:2])}."})
            mid_point = "Scenic Highway Stop"
            day_plan.append({"icon": "🚗", "time": "01:00 PM", "activity": f"Drive towards {destination}. Stop for lunch at a {random.choice(list(eateries.values()))}."})
            day_plan.append({"icon": "HOTEL", "time": "07:00 PM", "activity": f"Halt at {mid_point}. Check into a {stays[hotel_pref]}."})
        
        itinerary_data.append({
            "type": "day_card", "day_num": day_counter, "route": f"{origin} ➔ {destination} (Leg 1/2)",
            "events": day_plan, "budget": daily_costs
        })
        day_counter += 1
        
        # --- Generate Day 2 (Arrival & Explore) ---
        day_plan_2 = []
        dest_spots = get_sightseeing_spots(destination)
        
        if transport_mode == "Public Transport":
            day_plan_2.append({"icon": "🏁", "time": "09:00 AM", "activity": f"Arrive in **{destination}**. Check into your {stays[hotel_pref]}."})
            day_plan_2.append({"icon": "🚕", "time": "11:00 AM", "activity": "Hire a local auto/taxi for sightseeing."})
            day_plan_2.append({"icon": "📸", "time": "01:00 PM", "activity": f"Explore {destination}: Visit {', '.join(dest_spots)}."})
        else: # Personal or Rented
            day_plan_2.append({"icon": "🛣️", "time": "09:00 AM", "activity": "Resume journey. Enjoy the landscape."})
            day_plan_2.append({"icon": "🏁", "time": "02:00 PM", "activity": f"Arrive in **{destination}**! Check into your {stays[hotel_pref]}."})
            day_plan_2.append({"icon": "📸", "time": "04:00 PM", "activity": f"Explore {destination}: Visit {', '.join(dest_spots)}."})
            
        day_plan_2.append({"icon": "🍽️", "time": "08:30 PM", "activity": f"Dinner at a {random.choice(list(eateries.values()))} in {destination}."})
        
        itinerary_data.append({
            "type": "day_card", "day_num": day_counter, "route": f"Arrive at {destination} (
