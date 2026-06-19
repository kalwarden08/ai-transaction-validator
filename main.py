"""
FastAPI application for AI Transaction Validator.
"""
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from validation import TransactionValidator
from splitter import CSVSplitter

# Setup directories
BASE_DIR = Path(__file__).parent
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

UPLOADS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

# FastAPI app setup
app = FastAPI(title="AI Transaction Validator")

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Configuration
CHUNK_SIZE = 1000
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB


@app.get("/")
async def index(request: Request):
    """Render main page."""
    return templates.TemplateResponse(name="index.html", context={"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handle CSV file upload and validation.
    
    Args:
        file: Uploaded CSV file
        
    Returns:
        JSON response with validation results
    """
    try:
        # Validate file
        if not file.filename.endswith('.csv'):
            return JSONResponse(
                status_code=400,
                content={"error": "Only CSV files are allowed"}
            )

        # Read file
        contents = await file.read()
        if len(contents) == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "File is empty"}
            )

        # Save uploaded file
        upload_path = UPLOADS_DIR / file.filename
        with open(upload_path, 'wb') as f:
            f.write(contents)

        # Read CSV
        try:
            df = pd.read_csv(upload_path)
        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={"error": f"Failed to parse CSV: {str(e)}"}
            )

        # Check for required columns
        required_columns = ['order_id', 'customer_name', 'country_code', 'phone',
                           'date', 'time', 'product_id', 'product_name', 'amount', 'payment_mode']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return JSONResponse(
                status_code=400,
                content={"error": f"Missing required columns: {', '.join(missing_columns)}"}
            )

        # Validate records
        validator = TransactionValidator(country_rules_path="country_rules.json")
        valid_df, invalid_df, validation_errors = validator.validate_dataset(df)

        # Generate timestamp for this session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = OUTPUTS_DIR / timestamp
        session_dir.mkdir(exist_ok=True)

        # Save results
        valid_csv = session_dir / "valid_records.csv"
        invalid_csv = session_dir / "invalid_records.csv"
        report_csv = session_dir / "validation_report.csv"

        if not valid_df.empty:
            valid_df.to_csv(valid_csv, index=False)

        if not invalid_df.empty:
            invalid_df.to_csv(invalid_csv, index=False)

        # Generate validation report
        validation_report = validator.generate_validation_report()
        if not validation_report.empty:
            validation_report.to_csv(report_csv, index=False)

        # Split valid records if needed
        split_info = CSVSplitter.get_split_info(valid_df, CHUNK_SIZE)
        chunk_files = []
        
        if split_info['will_split'] and not valid_df.empty:
            chunk_files = CSVSplitter.split_csv(
                valid_df,
                output_dir=str(session_dir),
                chunk_size=CHUNK_SIZE,
                prefix="chunk"
            )

        # Calculate statistics
        total_records = len(df)
        valid_records = len(valid_df)
        invalid_records = len(invalid_df)
        success_rate = (valid_records / total_records * 100) if total_records > 0 else 0

        # Prepare response
        response = {
            "status": "success",
            "session_id": timestamp,
            "statistics": {
                "total_records": total_records,
                "valid_records": valid_records,
                "invalid_records": invalid_records,
                "success_rate": round(success_rate, 2)
            },
            "files": {
                "valid_csv": "valid_records.csv" if not valid_df.empty else None,
                "invalid_csv": "invalid_records.csv" if not invalid_df.empty else None,
                "validation_report": "validation_report.csv" if not validation_report.empty else None,
                "chunks": chunk_files,
                "will_split": split_info['will_split']
            },
            "validation_summary": {
                "total_errors": len(validation_errors),
                "errors": validation_errors[:100]  # Return first 100 errors
            }
        }

        return response

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Server error: {str(e)}"}
        )


@app.get("/download/{session_id}/{filename}")
async def download_file(session_id: str, filename: str):
    """
    Download a processed file.
    
    Args:
        session_id: Session timestamp
        filename: Name of file to download
        
    Returns:
        File download response
    """
    try:
        # Security: validate filename to prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        file_path = OUTPUTS_DIR / session_id / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="text/csv"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download-zip/{session_id}")
async def download_zip(session_id: str):
    """
    Download all chunk files as ZIP.
    
    Args:
        session_id: Session timestamp
        
    Returns:
        ZIP file download response
    """
    try:
        session_dir = OUTPUTS_DIR / session_id

        if not session_dir.exists():
            raise HTTPException(status_code=404, detail="Session not found")

        # Find all chunk files
        chunk_files = sorted(session_dir.glob("chunk_*.csv"))

        if not chunk_files:
            raise HTTPException(status_code=400, detail="No chunk files found")

        # Create ZIP
        zip_filename = f"chunks_{session_id}.zip"
        zip_path = session_dir / zip_filename

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for chunk_file in chunk_files:
                zipf.write(chunk_file, arcname=chunk_file.name)

        return FileResponse(
            path=zip_path,
            filename=zip_filename,
            media_type="application/zip"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
