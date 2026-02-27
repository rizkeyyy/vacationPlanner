from fastapi import FastAPI

app = FastAPI(title="Voyager AI Backend")

@app.get("/")
def health_check():
    return {"status": "backend running"}