"""
ELKA Enterprise Knowledge Assistant API
Production-grade FastAPI backend for RAG system
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

from backend.api.query import ask_question

UPLOAD_DIR = "data/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="ELKA Enterprise Knowledge Assistant",
    description="Production RAG system with Query Rewriting, Hybrid Retrieval, and LLM Generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]

class BatchQueryRequest(BaseModel):
    questions: list[str]


# Credentials Models for External Sync
class GoogleDriveCredentials(BaseModel):
    folder_id: Optional[str] = None
    service_account_json: Optional[Dict[str, Any]] = None

class SlackCredentials(BaseModel):
    token: str
    channel_id: str

class NotionCredentials(BaseModel):
    token: str
    database_id: str


@app.get("/")
def root():
    return {"message": "ELKA API running", "version": "1.0.0", "status": "operational"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ELKA Enterprise Knowledge Assistant", "version": "1.0.0"}


@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        result = ask_question(request.question)
        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    allowed_extensions = {'.pdf', '.txt', '.html', '.md'}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}")

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = subprocess.run(
            ["python", "run_ingestion.py"],
            capture_output=True, text=True, timeout=300
        )

        if result.returncode != 0:
            raise Exception(f"Ingestion failed: {result.stderr}")

        return {"message": f"{file.filename} uploaded and indexed successfully", "filename": file.filename, "status": "success"}

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Ingestion timeout - try uploading smaller documents")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/documents")
def list_documents():
    try:
        if not os.path.exists(UPLOAD_DIR):
            return {"documents": [], "count": 0}
        documents = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
            raise HTTPException(status_code=400, detail="Invalid filename")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        os.remove(file_path)
        subprocess.run(["python", "run_ingestion.py"], capture_output=True, timeout=300)
        return {"message": f"{filename} deleted and index updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")


@app.post("/batch-query")
def batch_query(request: BatchQueryRequest):
    if not request.questions:
        raise HTTPException(status_code=400, detail="Questions list cannot be empty")
    if len(request.questions) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 questions per batch")
    try:
        results = []
        for question in request.questions:
            if not question.strip():
                results.append({"question": question, "answer": None, "error": "Empty question"})
                continue
            try:
                result = ask_question(question)
                results.append({"question": question, "answer": result["answer"], "sources": result["sources"], "error": None})
            except Exception as e:
                results.append({"question": question, "answer": None, "sources": [], "error": str(e)})
        return {"results": results, "total": len(results), "successful": sum(1 for r in results if r["error"] is None)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch query error: {str(e)}")


@app.get("/info/config")
def get_config():
    return {
        "upload_directory": UPLOAD_DIR,
        "max_batch_size": 50,
        "supported_formats": ['.pdf', '.txt', '.html', '.md'],
        "model": "google/gemini-2.5-flash"
    }


@app.post("/sync/{source}")
def sync_external_source(source: str, credentials: dict = Body(...)):
    """
    Sync external knowledge sources (Google Drive, Slack, Notion)
    Accepts credentials in request body as JSON
    """
    if not credentials:
        raise HTTPException(status_code=400, detail="Credentials required in request body")
    try:
        from backend.connectors.google_drive import download_drive_files
        from backend.connectors.slack import fetch_slack_messages
        from backend.connectors.notion import fetch_notion_pages
        import json as json_lib
        import tempfile
        
        print(f"Starting sync for {source}...")
        
        if source == "gdrive":
            if not credentials:
                raise HTTPException(status_code=400, detail="Google Drive credentials required")
            
            folder_id = credentials.get("folder_id")
            service_account_json = credentials.get("service_account_json")
            
            if not folder_id:
                raise HTTPException(status_code=400, detail="folder_id is required")
            
            # Handle service account JSON
            if service_account_json:
                # Write JSON to temp file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    json_lib.dump(service_account_json, f)
                    f.flush()  # Ensure data is written to disk
                    service_account_file = f.name
            else:
                service_account_file = "service_account.json"
            
            try:
                download_drive_files(service_account_file, folder_id)
            finally:
                if service_account_json and os.path.exists(service_account_file):
                    os.unlink(service_account_file)
            
            source_name = "Google Drive"
            
        elif source == "slack":
            if not credentials:
                raise HTTPException(status_code=400, detail="Slack credentials required")
            
            token = credentials.get("token")
            channel_id = credentials.get("channel_id")
            
            if not token or not channel_id:
                raise HTTPException(status_code=400, detail="token and channel_id are required")
            
            fetch_slack_messages(token, channel_id)
            source_name = "Slack"
            
        elif source == "notion":
            if not credentials:
                raise HTTPException(status_code=400, detail="Notion credentials required")
            
            token = credentials.get("token")
            database_id = credentials.get("database_id")
            
            if not token or not database_id:
                raise HTTPException(status_code=400, detail="token and database_id are required")
            
            fetch_notion_pages(token, database_id)
            source_name = "Notion"
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown source: {source}. Allowed: gdrive, slack, notion")
        
        # Run ingestion pipeline after syncing
        print(f"Running ingestion pipeline for {source_name} sync...")
        result = subprocess.run(
            ["python", "run_ingestion.py"],
            capture_output=True, text=True, timeout=600
        )
        
        if result.returncode != 0:
            raise Exception(f"Ingestion failed: {result.stderr}")
        
        return {
            "status": "synced",
            "source": source,
            "message": f"{source_name} documents imported and indexed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_msg = f"Sync failed: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_msg)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
