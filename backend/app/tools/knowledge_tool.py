from langchain_core.tools import tool

@tool
def consult_travel_guide(query: str):
    """
    Memberikan informasi umum/singkat tentang destinasi wisata.
    Hanya gunakan tool ini jika user bertanya spesifik tentang 'Apa yang menarik di X?'.
    JANGAN gunakan tool ini untuk mengecek harga atau ketersediaan tiket.
    """
    # Kita return response generik agar aman dan tidak error
    return f"""
    [INFO WISATA]
    Destinasi '{query}' merupakan pilihan populer. 
    Saran: Sebaiknya langsung cek ketersediaan Hotel dan Pesawat untuk mendapatkan harga terkini.
    """