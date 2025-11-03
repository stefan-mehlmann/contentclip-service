from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
import csv
import io

# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="ContentClip Service",
    description="Microservice zum Upload und Verarbeitung von zwei CSV-Dateien",
    version="1.0.0"
)

# ============================================================================
# Helper Functions
# ============================================================================

def parse_csv(file_content: bytes) -> List[Dict[str, Any]]:
    """Parse CSV und gib alle Zeilen zurück"""
    csv_text = file_content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_text), delimiter=';')
    return list(csv_reader)

# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health Check"""
    return {
        "service": "ContentClip Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/upload/csv")
async def upload_csv_return_csv(
    file1: UploadFile = File(..., description="Erste CSV-Datei"),
    file2: UploadFile = File(..., description="Zweite CSV-Datei")
):
    """
    Upload zwei CSV-Dateien und erhalte alle Einträge aus der ersten Datei als CSV
    
    Returns:
        CSV-Datei mit allen Zeilen aus file1
    """
    # Validierung
    if not file1.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file1 must be a CSV file")
    
    if not file2.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file2 must be a CSV file")
    
    # Dateien lesen
    file1_content = await file1.read()
    file2_content = await file2.read()
    
    # file1 parsen (alle Zeilen)
    try:
        data = parse_csv(file1_content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV: {str(e)}")
    
    # CSV erstellen
    output = io.StringIO()
    if data:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(data)
    
    # CSV Response
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=contentclip_result.csv"
        }
    )

# ============================================================================
# Startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)