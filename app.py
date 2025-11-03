from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Dict, Any
import csv
import io
import pandas as pd

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

def parse_csv(file_content: bytes, max_rows: int = 20) -> List[Dict[str, Any]]:
    """Parse CSV und gib erste N Zeilen zurück"""
    csv_text = file_content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    rows = []
    for i, row in enumerate(csv_reader):
        if i >= max_rows:
            break
        rows.append(row)
    
    return rows

def create_xlsx(data: List[Dict]) -> bytes:
    """Erstelle XLSX mit einem Sheet"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df = pd.DataFrame(data)
        df.to_excel(writer, sheet_name='Data', index=False)
    
    output.seek(0)
    return output.getvalue()

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

@app.post("/upload/json")
async def upload_csv_return_json(
    file1: UploadFile = File(..., description="Erste CSV-Datei"),
    file2: UploadFile = File(..., description="Zweite CSV-Datei")
):
    """
    Upload zwei CSV-Dateien und erhalte die ersten 20 Einträge aus der ersten Datei als JSON
    
    Returns:
        JSON mit ersten 20 Zeilen aus file1
    """
    # Validierung
    if not file1.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file1 must be a CSV file")
    
    if not file2.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file2 must be a CSV file")
    
    # Dateien lesen
    file1_content = await file1.read()
    file2_content = await file2.read()
    
    # Nur file1 parsen (erste 20 Zeilen)
    try:
        data = parse_csv(file1_content, max_rows=20)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV: {str(e)}")
    
    # JSON Response
    return {
        "filename": file1.filename,
        "rows_returned": len(data),
        "data": data
    }

@app.post("/upload/xlsx")
async def upload_csv_return_xlsx(
    file1: UploadFile = File(..., description="Erste CSV-Datei"),
    file2: UploadFile = File(..., description="Zweite CSV-Datei")
):
    """
    Upload zwei CSV-Dateien und erhalte die ersten 20 Einträge aus der ersten Datei als XLSX
    
    Returns:
        XLSX-Datei mit ersten 20 Zeilen aus file1
    """
    # Validierung
    if not file1.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file1 must be a CSV file")
    
    if not file2.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file2 must be a CSV file")
    
    # Dateien lesen
    file1_content = await file1.read()
    file2_content = await file2.read()
    
    # Nur file1 parsen (erste 20 Zeilen)
    try:
        data = parse_csv(file1_content, max_rows=20)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV: {str(e)}")
    
    # XLSX erstellen
    try:
        xlsx_bytes = create_xlsx(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating XLSX: {str(e)}")
    
    # XLSX Response
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=contentclip_result.xlsx"
        }
    )

@app.post("/upload/csv")
async def upload_csv_return_csv(
    file1: UploadFile = File(..., description="Erste CSV-Datei"),
    file2: UploadFile = File(..., description="Zweite CSV-Datei")
):
    """
    Upload zwei CSV-Dateien und erhalte die ersten 20 Einträge aus der ersten Datei als CSV
    
    Returns:
        CSV-Datei mit ersten 20 Zeilen aus file1
    """
    # Validierung
    if not file1.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file1 must be a CSV file")
    
    if not file2.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="file2 must be a CSV file")
    
    # Dateien lesen
    file1_content = await file1.read()
    file2_content = await file2.read()
    
    # Nur file1 parsen (erste 20 Zeilen)
    try:
        data = parse_csv(file1_content, max_rows=20)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV: {str(e)}")
    
    # CSV erstellen
    output = io.StringIO()
    if data:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
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