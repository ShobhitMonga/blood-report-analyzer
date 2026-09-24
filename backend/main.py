from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from datetime import datetime
import json
import logging
from pydantic import BaseModel
from typing import List, Optional
from database import reports_collection

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Blood Report Analyzer API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY environment variable is missing!")
    
model = genai.GenerativeModel('gemini-3.8-flash')

# Define Pydantic Models for Output Validation
class Marker(BaseModel):
    name: str
    value: str
    unit: str
    normal_range: str
    status: str

class BloodReportResult(BaseModel):
    summary_english: str
    summary_hindi: str
    summary_punjabi: str
    markers: List[Marker]

PROMPT = """
You are a medical expert. Read this blood report. 
Extract the key biomarkers, the normal reference ranges, and the patient's values.
Also provide an explanation of any abnormalities in simple, plain English that a non-medical person can understand.
Translate this exact summary into fluent Hindi (summary_hindi) and Punjabi (summary_punjabi).
Return the result strictly as a JSON object matching this EXACT format:
{
  "summary_english": "...",
  "summary_hindi": "...",
  "summary_punjabi": "...",
  "markers": [
    {
      "name": "Hemoglobin",
      "value": "12.00",
      "unit": "g/dL",
      "normal_range": "13.00 - 17.00",
      "status": "Low"
    }
  ]
}
"""

def fix_object_id(report):
    report["_id"] = str(report["_id"])
    return report

@app.post("/analyze")
async def analyze_report(file: UploadFile = File(...)):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API Key not set.")
        
    try:
        logger.info(f"Received file: {file.filename} (Type: {file.content_type})")
        contents = await file.read()
        mime_type = file.content_type or "image/jpeg"
        
        # Call Gemini with Structured Output configuration
        logger.info("Sending request to Gemini AI...")
        response = model.generate_content(
            [PROMPT, {"mime_type": mime_type, "data": contents}],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        logger.info("Received response from Gemini AI.")
            
        parsed_data = json.loads(response.text)
        
        # Add metadata before saving to DB
        parsed_data["filename"] = file.filename
        parsed_data["upload_date"] = datetime.utcnow().isoformat()
        
        # Save to DB
        result = await reports_collection.insert_one(parsed_data.copy())
        logger.info(f"Saved analysis to database with ID: {result.inserted_id}")
        
        parsed_data["_id"] = str(result.inserted_id)
        
        return parsed_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response into JSON.")
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis.")

@app.get("/history")
async def get_history():
    logger.info("Fetching report history from database...")
    reports = []
    cursor = reports_collection.find().sort("upload_date", -1)
    async for document in cursor:
        reports.append(fix_object_id(document))
    return {"reports": reports}
