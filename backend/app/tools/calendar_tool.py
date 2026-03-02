from langchain_core.tools import tool
import json

@tool
def check_user_calendar(date_range: str = "this weekend"):
    """
    Mengecek ketersediaan jadwal user di kalender.
    Gunakan tool ini SEBELUM mencari hotel untuk memastikan user bisa pergi.
    """
    print(f"📅 [CALENDAR] Checking schedule for: {date_range}")
    
    # Simulasi logika pengecekan
    mock_response = {
        "status": "AVAILABLE",
        "date": "2026-03-07 to 2026-03-08",
        "notes": "Tidak ada meeting. Jadwal kosong untuk liburan."
    }
    
    # Return data JSON (sesuai arsitektur kita yang baru)
    return f":::CALENDAR_DATA:::{json.dumps(mock_response)}:::END_DATA:::"