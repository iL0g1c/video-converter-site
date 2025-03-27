from fastapi import FastAPI, File, UploadFile, WebSocket
from fastapi.responses import FileResponse
import shutil
import os
from app.utils import convert_video
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
CONVERTED_DIR = "converted"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CONVERTED_DIR, exist_ok=True)


@app.post("/upload/")
async def upload_video(file: UploadFile, format: str):
    file_id = str(uuid.uuid4())
    input_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    output_path = f"{CONVERTED_DIR}/{file_id}_converted.{format}"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Start video conversion
    convert_video(input_path, output_path, format)
    return {"file_id": file_id, "output_path": output_path}


@app.get("/download/{file_id}")
async def download_video(file_id: str, format: str):
    output_path = f"{CONVERTED_DIR}/{file_id}_converted.{format}"
    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="application/octet-stream", filename=f"{file_id}_converted.{format}")
    return {"error": "File not found"}
