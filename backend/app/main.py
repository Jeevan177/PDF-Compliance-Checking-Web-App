from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from .services.compliance_service import ComplianceService
from .models import ComplianceResponse
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Compliance Check API",
    description="API for checking document compliance against rules",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize compliance service
compliance_service = ComplianceService()

@app.get("/")
async def root():
    return {"message": "Compliance Check API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/compliance-check", response_model=ComplianceResponse)
async def check_compliance(
    pdf_file: UploadFile = File(..., description="PDF document to check"),
    rules_file: UploadFile = File(..., description="Text file containing compliance rules")
):
    try:
        # Validate file types
        if not pdf_file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="PDF file must have .pdf extension")
        
        if not rules_file.filename.lower().endswith('.txt'):
            raise HTTPException(status_code=400, detail="Rules file must have .txt extension")
        
        logger.info(f"Processing compliance check for {pdf_file.filename}")
        
        # Process the compliance check
        results = await compliance_service.run_compliance_check(pdf_file, rules_file)
        
        return ComplianceResponse(
            status="success",
            results=results,
            pdf_filename=pdf_file.filename,
            rules_filename=rules_file.filename
        )
        
    except Exception as e:
        logger.error(f"Error processing compliance check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )