from fastapi import FastAPI
from routers import document

app = FastAPI()

app.include_router(document.router, prefix="/api", tags=["Document"])


@app.get("/")
def read_root():
    return {"message": "DocuMind backend is running"}

