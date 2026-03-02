import json
import os
import random
from langchain_core.tools import tool

# --- SETUP PATH DATABASE (SAMA DENGAN HOTEL) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Kita tembak file yang sama biar terpusat
BOOKING_DB = os.path.join(BASE_DIR, "../../data/mock_db/bookings_db.json")

# --- HELPER: LOGO MASKAPAI ---
def get_airline_logo(airline_name):
    if "Garuda" in airline_name:
        return "https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Garuda_Indonesia_Logo.svg/1200px-Garuda_Indonesia_Logo.svg.png"
    elif "Lion" in airline_name:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Lion_Air_logo.svg/1200px-Lion_Air_logo.svg.png"
    else:
        return "https://cdn-icons-png.flaticon.com/512/723/723955.png"

# --- HELPER: SAVE TO DB (Copy Logic dari hotel_tools) ---
def save_flight_booking(data):
    os.makedirs(os.path.dirname(BOOKING_DB), exist_ok=True)
    if not os.path.exists(BOOKING_DB):
        with open(BOOKING_DB, "w") as f: json.dump([], f)
    
    try:
        with open(BOOKING_DB, "r+") as f:
            try:
                bookings = json.load(f)
            except: bookings = []
            
            bookings.append(data)
            f.seek(0)
            json.dump(bookings, f, indent=4)
    except Exception as e:
        print(f"Error saving flight: {e}")

# --- TOOLS ---

@tool
def search_flights(destination: str, origin: str = "Jakarta"):
    """
    Mencari jadwal penerbangan.
    """
    print(f"✈️ [TOOL] Search Flight: {origin} -> {destination}")
    dest_lower = destination.lower()
    
    # Logic Mockup
    if "bali" in dest_lower or "denpasar" in dest_lower:
        found_flights = [
            {
                "airline": "Garuda Indonesia",
                "flight_code": "GA-404",
                "time": "08:00 - 10:50",
                "price": 1800000,
                "logo": get_airline_logo("Garuda")
            },
            {
                "airline": "Lion Air",
                "flight_code": "JT-610",
                "time": "14:00 - 16:50",
                "price": 950000,
                "logo": get_airline_logo("Lion")
            }
        ]
        json_data = json.dumps(found_flights)
        return f":::FLIGHT_DATA:::{json_data}:::END_DATA:::"
    
    return f"Maaf, saat ini belum tersedia jadwal penerbangan dari {origin} ke {destination} di database kami."

@tool
def book_flight(airline_name: str, guest_name: str = "Tamu"):
    """
    Melakukan BOOKING TIKET PESAWAT dan simpan ke database.
    Gunakan tool ini jika user ingin membeli/booking tiket pesawat.
    """
    print(f"🛫 [TOOL] Booking Flight: {airline_name}")
    
    # Generate ID Unik (Flight ID)
    booking_id = f"FLT-{random.randint(10000, 99999)}"
    
    booking_data = {
        "id": booking_id,
        "hotel_name": f"Tiket {airline_name}", # Kita pinjam field hotel_name biar invoice frontend gak perlu diubah
        "guest_name": guest_name,
        "status": "ISSUED",
        "payment_method": "VISA PLATINUM",
        "timestamp": "2026-03-02"
    }
    
    # Simpan ke DB yang sama
    save_flight_booking(booking_data)
    
    # Return JSON Invoice
    json_data = json.dumps(booking_data)
    return f":::BOOKING_DATA:::{json_data}:::END_DATA:::"