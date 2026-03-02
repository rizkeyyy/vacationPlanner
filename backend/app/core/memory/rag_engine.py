import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# --- KONFIGURASI PATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Mundur 3 langkah untuk ke folder data (backend/data/knowledge_base)
DATA_PATH = os.path.join(CURRENT_DIR, "../../../../backend/data/knowledge_base/travel_guide.txt")
# Lokasi penyimpana database vector (backend/data/vector_db)
DB_PATH = os.path.join(CURRENT_DIR, "../../../../backend/data/vector_db")

def build_knowledge_base():
    """
    Fungsi ini dibaca CUMA SEKALI untuk mengubah teks jadi angka (vector)
    dan menyimpannya di ChromaDB.
    """
    print(f"🔄 Membaca data dari: {DATA_PATH}")
    
    # 1. Load File Teks
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File tidak ditemukan di: {DATA_PATH}")
        
    loader = TextLoader(DATA_PATH)
    docs = loader.load()
    
    # 2. Pecah Teks (Chunking)
    # Kita pecah per 500 karakter biar AI fokus
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    print(f"✅ Berhasil memecah dokumen menjadi {len(splits)} potongan.")

    # 3. Embed & Simpan ke ChromaDB
    # Model ini GRATIS dan jalan offline di laptopmu (gak pake API key)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("🧠 Sedang menanamkan memori ke otak AI (Embedding)...")
    vector_db = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=DB_PATH
    )
    print("🎉 Database pengetahuan berhasil disimpan!")
    return vector_db

def get_retriever():
    """
    Fungsi ini dipanggil nanti sama Agent buat nyari info.
    """
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
    return vector_db.as_retriever(search_kwargs={"k": 2}) # Ambil 2 info paling relevan

# --- TEST AREA (Biar bisa langsung dicoba) ---
if __name__ == "__main__":
    # 1. Bangun Database dulu
    db = build_knowledge_base()
    
    # 2. Coba Tanya
    pertanyaan = "Tempat yang bagus buat honeymoon romantis dimana?"
    print(f"\n❓ Test Query: {pertanyaan}")
    
    docs = db.similarity_search(pertanyaan)
    print("\n💡 Jawaban dari Database RAG:")
    for i, doc in enumerate(docs):
        print(f"[{i+1}] {doc.page_content}\n")