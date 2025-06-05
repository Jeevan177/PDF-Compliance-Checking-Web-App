from pydantic import BaseModel
from typing import Dict, Any

class ComplianceResponse(BaseModel):
    status: str
    results: Dict[str, Any]
    pdf_filename: str
    rules_filename: str
    
class HealthResponse(BaseModel):
    status: str