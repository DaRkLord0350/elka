"""
ELKA Enterprise Knowledge Assistant API
Production-grade FastAPI backend for RAG system
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os
import subprocess
from pathlib import Path

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
