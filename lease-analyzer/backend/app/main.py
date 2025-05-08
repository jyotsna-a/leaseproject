from fastapi import FastAPI, UploadFile, File
import os, shutil
import pdfplumber
import openai  # you'll later set your API key
from app.utils.lease_summary import generate_summary  # you’ll create this

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Lease Analyzer Backend Running!"}

@app.get("/ping")
async def ping():
    return {"message": "pong"}


# Lease Uploads
UPLOAD_DIR = "temp_uploads"  # temp folder for uploads

@app.post("/upload")
async def upload_lease(file: UploadFile = File(...)):
    # Save temp file
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    with pdfplumber.open(temp_path) as pdf:
        full_text = "\n".join([page.extract_text() or "" for page in pdf.pages])

    # Generate summary
    summary = generate_summary(full_text)

    # Clean up
    os.remove(temp_path)

    return {"summary": summary}
