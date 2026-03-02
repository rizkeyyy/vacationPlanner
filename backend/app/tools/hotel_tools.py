import json
import os
import random
from langchain_core.tools import tool

# --- SETUP PATH DATABASE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOTELS_DB = os.path.join(BASE_DIR, "../../data/mock_db/hotels.json")
BOOKING_DB = os.path.join(BASE_DIR, "../../data/mock_db/bookings_db.json")

# --- HELPER FUNCTIONS (Bukan Tool) ---
def load_hotels():
    if not os.path.exists(HOTELS_DB): return []
    try:
        with open(HOTELS_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return []

def save_booking_to_db(data):
    # Pastikan folder ada
    os.makedirs(os.path.dirname(BOOKING_DB), exist_ok=True)
    
    # Buat file jika belum ada
    if not os.path.exists(BOOKING_DB):
        with open(BOOKING_DB, "w") as f: json.dump([], f)
    
    # Baca, Append, Simpan
    try:
        with open(BOOKING_DB, "r+") as f:
            try:
                bookings = json.load(f)
            except json.JSONDecodeError:
                bookings = []
            
            bookings.append(data)
            f.seek(0)
            json.dump(bookings, f, indent=4)
    except Exception as e:
        print(f"Error saving booking: {e}")

# --- TOOLS UTAMA (Dipanggil Agent) ---

@tool
def check_hotel_availability(location: str, max_price: int = 0):
    """
    Mencari hotel berdasarkan lokasi. 
    Mengembalikan data JSON untuk dirender menjadi Card UI.
    """
    print(f"🔎 [TOOL] Search Hotel: {location}")
    hotels = load_hotels()
    found_hotels = []
    
    loc_query = location.lower()
    
    for h in hotels:
        # Logika pencarian sederhana
        h_loc = h["location"].lower()
        if (loc_query in h_loc) or (h_loc in loc_query) or ("bali" in loc_query and "bali" in h_loc):
            if max_price > 0 and h["price"] > max_price: continue
            
            # Format data untuk Frontend
            found_hotels.append({
                "name": h["name"],
                "location": h["location"],
                "price": h["price"],
                "rating": h["rating"],
                "image": h["image"],
                "amenities": h["amenities"][:3]
            })
            
    if not found_hotels:
        return "Maaf, tidak ada data hotel yang cocok."

    # Return JSON dengan Marker
    json_data = json.dumps(found_hotels[:3]) # Batasi 3 hasil
    return f":::HOTEL_DATA:::{json_data}:::END_DATA:::"

@tool
def book_hotel(hotel_name: str, guest_name: str = "Tamu"):
    """
    Melakukan booking (Hotel/Pesawat) dan menyimpannya ke database.
    Mengembalikan Invoice JSON.
    """
    print(f"💳 [TOOL] Booking Process: {hotel_name}")
    
    # Generate ID Unik
    booking_id = f"VOY-{random.randint(10000, 99999)}"
    
    booking_data = {
        "id": booking_id,
        "hotel_name": hotel_name, # Bisa berisi nama hotel atau "Tiket Pesawat X"
        "guest_name": guest_name,
        "status": "LUNAS",
        "payment_method": "VISA PLATINUM",
        "timestamp": "2026-03-02" 
    }
    
    # Simpan ke File JSON (Persistence)
    save_booking_to_db(booking_data)
    
    # Return JSON Invoice
    json_data = json.dumps(booking_data)
    return f":::BOOKING_DATA:::{json_data}:::END_DATA:::"

@tool
def retrieve_booking_status(booking_id: str):
    """
    Mengecek status booking berdasarkan Booking ID (contoh: VOY-12345).
    """
    print(f"📂 [TOOL] Retrieve Booking: {booking_id}")
    
    if not os.path.exists(BOOKING_DB):
        return "Database booking kosong/belum ada transaksi."

    try:
        with open(BOOKING_DB, "r") as f:
            bookings = json.load(f)
            
        # Cari ID (Case insensitive)
        result = next((b for b in bookings if b["id"].upper() == booking_id.upper()), None)
        
        if result:
            # Kembalikan format BOOKING_DATA agar Frontend merender Invoice lagi
            return f":::BOOKING_DATA:::{json.dumps(result)}:::END_DATA:::"
        else:
            return f"Maaf, Booking ID **{booking_id}** tidak ditemukan di database kami."
            
    except Exception as e:
        return f"Terjadi kesalahan saat membaca database: {str(e)}"