"""
ELKA Enterprise Knowledge Assistant API
Production-grade FastAPI backend for RAG system
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import subprocess
from pathlib import Path

from backend.api.query import ask_question


# Configuration
UPLOAD_DIR = "data/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="ELKA Enterprise Knowledge Assistant",
    description="Production RAG system with Query Rewriting, Hybrid Retrieval, and LLM Generation",
    version="1.0.0"
)

# Add CORS middleware for frontend compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== DATA MODELS ====================

class QueryRequest(BaseModel):
    """Query request model"""
    question: str


class QueryResponse(BaseModel):
    """Query response model"""
    question: str
    answer: str


# ==================== HEALTH CHECK ====================

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "message": "ELKA API running",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "ELKA Enterprise Knowledge Assistant",
        "version": "1.0.0"
    }


# ==================== QUERY ENDPOINT ====================

@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    """
    Query the RAG system with natural language question.
    
    Pipeline:
    1. Query Rewriting (expand vague queries)
    2. Hybrid Search (FAISS + BM25)
    3. Reranking (cross-encoder)
    4. LLM Generation (Gemini)
    
    Args:
        request: QueryRequest with question field
    
    Returns:
        QueryResponse with question and answer
    """
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer = ask_question(request.question)
        
        return {
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


# ==================== DOCUMENT UPLOAD ====================

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and automatically reindex the vector database.
    
    Supported formats:
    - PDF (.pdf)
    - Plain text (.txt)
    - HTML (.html)
    
    Process:
    1. Save file to data/documents/
    2. Run ingestion pipeline
    3. Update FAISS index
    
    Args:
        file: UploadFile object
    
    Returns:
        Success message with filename
    """
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    allowed_extensions = {'.pdf', '.txt', '.html', '.md'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Reindex the vector database
        print(f"Running ingestion pipeline for {file.filename}...")
        result = subprocess.run(
            ["python", "run_ingestion.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise Exception(f"Ingestion failed: {result.stderr}")
        
        return {
            "message": f"{file.filename} uploaded and indexed successfully",
            "filename": file.filename,
            "status": "success"
        }
    
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500, 
            detail="Ingestion timeout - try uploading smaller documents"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Upload failed: {str(e)}"
        )


# ==================== DOCUMENT MANAGEMENT ====================

@app.get("/documents")
def list_documents():
    """
    List all uploaded documents.
    
    Returns:
        List of filenames in data/documents/
    """
    try:
        if not os.path.exists(UPLOAD_DIR):
            return {"documents": [], "count": 0}
        
        documents = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]
        
        return {
            "documents": documents,
            "count": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """
    Delete a document.
    
    Args:
        filename: Name of file to delete
    
    Returns:
        Success message
    """
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Security: prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        os.remove(file_path)
        
        # Reindex after deletion
        print(f"Running ingestion pipeline after deleting {filename}...")
        subprocess.run(
            ["python", "run_ingestion.py"],
            capture_output=True,
            timeout=300
        )
        
        return {"message": f"{filename} deleted and index updated"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")


# ==================== BATCH QUERY ====================

class BatchQueryRequest(BaseModel):
    """Batch query request model"""
    questions: list[str]


@app.post("/batch-query")
def batch_query(request: BatchQueryRequest):
    """
    Process multiple questions at once.
    
    Args:
        request: BatchQueryRequest with list of questions
    
    Returns:
        List of answers corresponding to questions
    """
    
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
                answer = ask_question(question)
                results.append({"question": question, "answer": answer, "error": None})
            except Exception as e:
                results.append({"question": question, "answer": None, "error": str(e)})
        
        return {"results": results, "total": len(results), "successful": sum(1 for r in results if r["error"] is None)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch query error: {str(e)}")


# ==================== INFO ENDPOINTS ====================

@app.get("/info/config")
def get_config():
    """Get system configuration"""
    return {
        "upload_directory": UPLOAD_DIR,
        "max_batch_size": 50,
        "supported_formats": ['.pdf', '.txt', '.html', '.md'],
        "model": "google/gemini-2.5-flash"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("""
    🚀 ELKA Enterprise Knowledge Assistant
    Starting FastAPI server...
    
    API Documentation: http://127.0.0.1:8000/docs
    ReDoc: http://127.0.0.1:8000/redoc
    """)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
