
import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from services.dococr_extraction_services import GoogleDocOcr
from services.signature_detecore_service import SignatureDetectorService
from services.llama import generate_response

import cv2
import io
from dotenv import load_dotenv
import json
load_dotenv()

router = APIRouter()
detector = SignatureDetectorService()
extractore= GoogleDocOcr(
    project_id=os.getenv("PROJECT_ID"),
    processor_id=os.getenv("PROCESSOR_ID")
)

@router.post("/detect-signature")
async def detect_signature(file: UploadFile = File(...)):
    image_bytes = await file.read()
    annotated_image, _ = detector.detect_signature(image_bytes)

    _, encoded_image = cv2.imencode(".jpg", annotated_image)
    image_stream = io.BytesIO(encoded_image.tobytes())

    return StreamingResponse(image_stream, media_type="image/jpeg")



@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    extention=file.filename.split(".")[1]
    extention_={
        "pdf":"application/pdf",
        "png":"image/png",
        "jpg":"image/jpeg",
        "jpeg":"image/jpeg"
    }
    mime=extention_[extention]
    pdf_bytes = await file.read()

    response = extractore.documentai_(pdf_bytes,mime)
    json_string= generate_response(response['data'])
    # x = json_string.replace("```json\n", "").replace("\n```", "") 
    data = json.loads(json_string)
    return data