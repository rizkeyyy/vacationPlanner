# SOLUTION DOCUMENT: VOYAGER AI

**Project Name:** Voyager AI – Autonomous Vacation Planner  
**Student Name:** Rizki Ramadhan Lestariono  
**Submission Date:** March 2, 2026  

---

# 🌍 Voyager AI - Autonomous Vacation Planner

**Student Name:** Rizki Ramadhan Lestariono  
**Project Role:** Autonomous AI Agent (Proof of Concept)  
**Submission Date:** March 2, 2026

---

## 🚀 1. Overview & Key Features

**Voyager AI** adalah sistem agen perjalanan otonom yang dibangun menggunakan arsitektur **Agentic Tool-Use**. Berbeda dari chatbot biasa, Voyager memiliki kemampuan untuk mengambil keputusan dan bertindak (Action-Oriented) berdasarkan ketersediaan jadwal dan data riil.

### ✨ Fitur Unggulan:
- **Autonomous Calendar Sync:** Agent secara otomatis memvalidasi jadwal pengguna melalui `calendar_tool` sebelum merencanakan perjalanan.
- **Precise Tool Execution:** Melakukan pencarian hotel dan pesawat secara deterministik melalui Mock Database (menghindari halusinasi AI).
- **Persistence Layer:** Menggunakan database JSON (`bookings_db.json`) untuk menyimpan transaksi. Data tetap tersimpan meskipun aplikasi dimatikan.
- **Visual Document Generation:** Menghasilkan invoice digital yang dapat diunduh langsung sebagai bukti reservasi.

---

## 🛠️ 2. Installation & How to Run

Ikuti langkah berikut untuk menjalankan proyek dari hasil *Clone Repository*:

### Step 1: Clone Repository
```bash
git clone <URL_REPOS_ANDA>
cd Voyager_ai
```
### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
```
# Aktivasi Environment (Windows)
```bash
.\venv\Scripts\activate
```
# Aktivasi Environment (Mac/Linux)
```bash
source venv/bin/activate
```

# Install Dependencies (Versi Diet/Ringan)
```bash
pip install -r requirements.txt
```

### Step 3: API Configuration
Buat file .env di dalam folder backend/ dan masukkan API Key Groq Anda:
```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

### Step 4: Run Application
Jalankan Backend:
```bash
uvicorn main:app --reload
```

Buka Frontend:
Buka file frontend/dashboard.html di browser (Chrome/Edge direkomendasikan).

## 3. Installation & How to Run
Project Structure
```bash
Voyager_ai/
├── backend/
│   ├── app/
│   │   ├── core/       # State management (state.py)
│   │   ├── graph/      # Agent reasoning (agent.py)
│   │   ├── tools/      # Functional tools (Flight, Hotel, Calendar)
│   │   └── data/       # Mock DB (bookings_db.json, hotels.json)
│   ├── main.py         # Entry Point FastAPI
│   └── requirements.txt
├── frontend/
│   └── dashboard.html  # Interactive Dashboard
└── README.md           # Documentation (File ini)
```

