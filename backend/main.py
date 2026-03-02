import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Tambah path root biar module 'app' kebaca
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Kita import fungsi 'process_chat' yang baru kita buat di agent.py
# Fungsi ini sudah membungkus logika inject profile & invoke graph
from app.graph.agent import process_chat 

app = FastAPI(title="Voyager AI Backend")

# Setup CORS (Wajib biar HTML bisa akses)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODEL DATA BARU (DINAMIS) ---
class ChatRequest(BaseModel):
    message: str
    user_profile: dict = {} # Default kosong kalau frontend lupa kirim

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        print(f"📩 Pesan Masuk: {req.message}")
        print(f"👤 Profil User: {req.user_profile.get('name', 'Anonim')}")
        
        # Panggil fungsi pintar di agent.py
        # Fungsi ini akan:
        # 1. Bikin System Prompt baru sesuai Profil User
        # 2. Jalanin Agent
        # 3. Balikin respons terakhir (Text atau JSON Marker)
        reply = process_chat(req.message, req.user_profile)
        
        return {"reply": reply}

    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "Server Voyager Aman Terkendali 🚀"}