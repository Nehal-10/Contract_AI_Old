from pathlib import Path

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from src.pipeline.analyze_uploaded_contract import (
    analyze_contract
)

app = FastAPI(
    title="Contract AI API"
)

UPLOAD_DIR = Path(
    "data/uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@app.get("/")
def home():

    return {
        "message":
        "Contract AI Running"
    }


@app.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):

    file_path = (
        UPLOAD_DIR /
        file.filename
    )

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(contents)

    result = analyze_contract(
        file_path
    )

    return result
