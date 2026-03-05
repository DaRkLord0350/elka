# ELKA — Enterprise Knowledge Assistant

A production-grade **Retrieval-Augmented Generation (RAG)** system that intelligently searches through enterprise documents and generates accurate, context-aware answers using LLMs. ELKA combines vector search, keyword search, query rewriting, and intelligent reranking to deliver superior retrieval and generation capabilities.

---

## 🎯 Project Overview

ELKA is an enterprise-grade knowledge assistant designed to help organizations extract insights from their document repositories. It enables intelligent querying across multiple document sources (PDFs, Google Drive, Slack, Notion) and provides accurate answers backed by source citations.

### Core Concept
The system implements a complete RAG pipeline:
1. **Ingest** documents from various sources
2. **Embed** documents into a vector database
3. **Retrieve** relevant context using hybrid search
4. **Rewrite** user queries for better retrieval
5. **Rerank** results for highest relevance
6. **Generate** accurate answers using LLMs

---

## ✨ Key Features

### 🔍 Intelligent Retrieval
- **Hybrid Search**: Combined vector (semantic) and keyword (BM25) search for comprehensive coverage
- **Query Rewriting**: Automatically improves user queries using LLM before retrieval
- **Smart Reranking**: Re-scores search results to prioritize most relevant documents
- **Multi-Source Support**: Indexes documents from multiple connectors

### 📄 Document Processing
- **Multiple Format Support**: PDF, TXT, HTML, Markdown
- **Smart Chunking**: 500-token chunks with 100-token overlap for context preservation
- **Text Preprocessing**: Automatic cleaning and normalization
- **Embedding Generation**: Uses state-of-the-art sentence transformers

### 🔗 External Data Connectors
- **Google Drive**: Automatic sync of Google Drive documents
- **Slack**: Index Slack channel messages and conversations
- **Notion**: Import Notion databases and pages
- **Direct Upload**: Manual document upload via API

### 🤖 LLM Integration
- **Modern LLM Support**: Uses Google Gemini 2.5 Flash via Bytez API
- **Intelligent Generation**: Context-aware answer generation
- **Streaming Ready**: Optimized for fast response times

### 🌐 Professional API
- **FastAPI Backend**: Production-ready REST API
- **CORS Support**: Cross-origin requests for frontend integration
- **Batch Processing**: Process multiple queries efficiently
- **Comprehensive Logging**: Detailed pipeline visibility

### 🎨 Modern Frontend
- **Dark Modern UI**: Professional dark theme with glassmorphism
- **Real-time Search**: Interactive query interface
- **Source Attribution**: Shows document sources for answers
- **Responsive Design**: Works on desktop and tablet

### ⏰ Background Scheduling
- **Automated Sync**: APScheduler for periodic data synchronization
- **Configurable Intervals**: Set sync frequency based on needs

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Frontend                         │
│            (Modern Web Interface)                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                   FastAPI Server                     │
├─────────────────────────────────────────────────────┤
│  • /query → Answer questions                         │
│  • /upload → Upload documents                        │
│  • /sync → Trigger external synchronization          │
│  • /health → Health check                            │
└──────────┬──────────────────────────┬────────────────┘
           │                          │
           ▼                          ▼
      ┌─────────────┐          ┌──────────────┐
      │   Query     │          │  Ingestion   │
      │  Pipeline   │          │  Pipeline    │
      └──────┬──────┘          └──────┬───────┘
             │                        │
      ┌──────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────┐
│              Retrieval Pipeline                      │
├─────────────────────────────────────────────────────┤
│  1. Query Rewriting (LLM)                            │
│  2. Hybrid Search:                                   │
│     - Vector Search (FAISS)                          │
│     - Keyword Search (BM25)                          │
│  3. Reranking (Relevance Scoring)                    │
│  4. Answer Generation (LLM)                          │
└──────────┬───────────────────────────────────────────┘
           │
      ┌────┴────┐
      ▼         ▼
  ┌────────┐ ┌────────────────┐
  │ FAISS  │ │  Chunks Meta   │
  │Vector  │ │   (Pickle)     │
  │Store   │ │                │
  └────────┘ └────────────────┘
```

### Module Structure

```
backend/
├── api/                    # FastAPI endpoints
│   ├── server.py          # Main application & routes
│   └── query.py           # Query pipeline orchestration
├── ingestion/             # Document processing pipeline
│   ├── loader.py          # Load PDFs and documents
│   ├── preprocessing.py   # Text cleaning
│   ├── chunking.py        # Text splitting
│   └── embeddings.py      # Generate embeddings
├── retrieval/             # Search & retrieval logic
│   ├── vector_search.py   # FAISS semantic search
│   ├── bm25_search.py     # Keyword search
│   ├── hybrid_search.py   # Combine & deduplicate results
│   ├── reranker.py        # Re-score results
│   └── query_rewriter.py  # LLM query improvement
├── llm/                   # LLM integration
│   ├── generator.py       # Answer generation
│   └── prompt.py          # Prompt templates
├── connectors/            # External data integrations
│   ├── sync_manager.py    # Orchestrate syncs
│   ├── google_drive.py    # Google Drive sync
│   ├── slack.py           # Slack message sync
│   └── notion.py          # Notion database sync
├── automation/            # Background jobs
│   └── scheduler.py       # APScheduler setup
└── config/                # Configuration
    └── settings.py        # Environment & settings

data/
└── documents/             # Downloaded documents

vector_store/
├── faiss_index           # FAISS vector database
└── chunks.pkl            # Chunk metadata

frontend/
└── index.html            # Web interface

run_ingestion.py          # Standalone ingestion entry point
test_query.py             # Interactive CLI for testing
test_api.py               # API testing utility
requirements.txt          # Python dependencies
```

---

## 🛠️ Tech Stack

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Framework** | FastAPI | High-performance REST API |
| **Server** | Uvicorn | ASGI server |
| **Vector DB** | FAISS | Fast semantic search |
| **Keyword Search** | Rank-BM25 | TF-IDF based retrieval |
| **Embeddings** | Sentence Transformers | Text encoding (all-MiniLM-L6-v2) |
| **LLM** | Bytez API (Gemini 2.5 Flash) | Answer generation & query rewriting |
| **Document Parsing** | PyPDF, BeautifulSoup | PDF & HTML extraction |
| **Scheduling** | APScheduler | Automated sync jobs |

### Connectors
- **Google Drive**: google-api-python-client, google-auth-oauthlib
- **Slack**: slack-sdk
- **Notion**: notion-client

### Frontend
- **HTML5** with custom CSS
- **Modern design**: Dark theme, glassmorphism, responsive layout
- **JavaScript**: Fetch API for backend communication

---

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- BYTEZ_API_KEY (for LLM functionality)
- Optional: Google Drive, Slack, or Notion API credentials

---

## 📦 Installation

### 1. Clone or Navigate to Project
```bash
cd d:\Ai\ELka
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
source .venv/bin/activate   # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
BYTEZ_API_KEY=your_bytez_api_key_here
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=100
DOCUMENT_PATH=data/documents
VECTOR_DB_PATH=vector_store/faiss_index
```

### 5. Create Required Directories
```bash
mkdir -p data/documents
mkdir -p vector_store
```

---

## 🚀 Quick Start

### Option 1: Web Interface + API Server
```bash
# Terminal 1: Start the API server
uvicorn backend.api.server:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Open frontend
# Open your browser to: http://localhost:8000
```

### Option 2: Interactive CLI Testing
```bash
python test_query.py
# Enter your question when prompted
```

### Option 3: Programmatic Usage
```python
from backend.api.query import ask_question

response = ask_question("What is the main topic?")
print(response["answer"])
print("Sources:", response["sources"])
```

---

## 📥 Ingestion Pipeline

### Process Documents Locally
```bash
python run_ingestion.py
```

**Pipeline Steps:**
1. ✅ Loads documents from `data/documents/` (currently supports PDFs)
2. ✅ Cleans and preprocesses text
3. ✅ Splits into chunks (500 tokens, 100 overlap)
4. ✅ Generates embeddings using Sentence Transformers
5. ✅ Creates FAISS vector index
6. ✅ Saves chunk metadata to `vector_store/chunks.pkl`

**Expected Output:**
```
============================================================
STARTING INGESTION PIPELINE
============================================================

 Looking for documents in: data/documents
 Loaded 5 documents
 Chunking documents...
   Document 1: 12 chunks from file1.pdf
   ...
 Total chunks created: 87
 Generating embeddings...
 Generated 87 embeddings
  Embedding dimension: 384
 Building FAISS index...
 FAISS index created
 Saving chunks metadata...
 Saved 87 chunks metadata

============================================================
 INGESTION COMPLETED SUCCESSFULLY
============================================================
```

---

## 🔄 Sync External Sources

### Automated Sync
```bash
python backend/connectors/sync_manager.py
```

**Supported Sources:**
- 📁 **Google Drive**: Downloads documents from specified folder
- 💬 **Slack**: Indexes channel messages and threads
- 📓 **Notion**: Imports Notion database pages

**Requirements for Each Source:**

**Google Drive:**
- Create service account JSON from Google Cloud Console
- Share Google Drive folder with service account email
- Set `GOOGLE_FOLDER_ID` environment variable

**Slack:**
- Create bot with message read permissions
- Set `SLACK_BOT_TOKEN` and `CHANNEL_ID`

**Notion:**
- Create integration and share pages
- Set `NOTION_TOKEN` and `DATABASE_ID`

---

## 🌐 API Endpoints

### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "ELKA Enterprise Knowledge Assistant",
  "version": "1.0.0"
}
```

### Query Documents (Main Endpoint)
```http
POST /query
Content-Type: application/json

{
  "question": "What is the main topic of the documents?"
}
```

**Response:**
```json
{
  "question": "What is the main topic of the documents?",
  "answer": "The documents primarily discuss advanced AI techniques...",
  "sources": ["file1.pdf", "file2.pdf"]
}
```

**Status Codes:**
- `200`: Successful query
- `400`: Empty or invalid question
- `500`: Processing error

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

file: <binary file data>
```

**Supported Formats:** `.pdf`, `.txt`, `.html`, `.md`

**Response:**
```json
{
  "filename": "document.pdf",
  "size": 1024000,
  "status": "uploaded"
}
```

### Batch Query (Process Multiple Questions)
```http
POST /batch-query
Content-Type: application/json

{
  "questions": [
    "Question 1?",
    "Question 2?",
    "Question 3?"
  ]
}
```

**Response:**
```json
[
  {
    "question": "Question 1?",
    "answer": "Answer 1...",
    "sources": ["file1.pdf"]
  },
  ...
]
```

### Trigger Sync
```http
POST /sync
```

Manually trigger synchronization of external sources (Google Drive, Slack, Notion).

---

## 🔍 Query Pipeline Explained

When you ask a question, ELKA processes it through multiple stages:

### Stage 1: Query Rewriting
```
User Query: "What about the projects?"
        ↓
    [LLM Processing]
        ↓
Improved Query: "What specific projects are mentioned and what are their details?"
```
The LLM makes the query more specific and detailed for better document retrieval.

### Stage 2: Hybrid Retrieval
```
Improved Query: "What specific projects are mentioned..."
        ↓
    ┌───┴────┐
    ▼        ▼
Vector    BM25
Search    Search
(10)      (10)
    │        │
    └───┬────┘
        ▼
  Combine & Deduplicate
        ↓
    ~15-20 Results
```
- **Vector Search**: Finds semantically similar content
- **BM25 Search**: Finds keyword matches
- Results are merged and deduplicated

### Stage 3: Reranking
```
~15-20 Results → [Reranker] → Top 7 Results
Sort by relevance score
```

### Stage 4: Answer Generation
```
User's Original Question + Top 7 Chunks
        ↓
    [LLM with Context]
        ↓
    Final Answer + Sources
```

---

## 🧪 Testing

### Test Interactive Query
```bash
python test_query.py
```
Prompts for input and shows the full pipeline execution.

### Test API
```bash
python test_api.py
```
Runs automated API tests with sample queries.

### Test Query Rewriting
```bash
python test_query_rewriting.py
```
Tests the query rewriting mechanism in isolation.

---

## ⚙️ Configuration Details

### Chunking Strategy
```python
CHUNK_SIZE = 500        # Tokens per chunk
CHUNK_OVERLAP = 100     # Tokens of overlap between chunks
```
This ensures:
- Chunks are substantive (500 tokens ≈ 200-300 words)
- Context isn't lost between chunks (100-token overlap)
- Reduces redundancy while preserving continuity

### Embedding Model
```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```
- Lightweight (22M parameters)
- Fast inference
- Output dimension: 384
- Excellent for semantic search
- Multi-lingual support

### Retrieval Settings
```python
Vector Search: top_k=10
BM25 Search: top_k=10
Final Results: top_k=7
```

### LLM Model
```
Provider: Bytez API
Model: google/gemini-2.5-flash
Capabilities:
  - Fast response times
  - Advanced reasoning
  - Long context windows
```

---

## 📊 Performance Metrics

| Operation | Time | Details |
|-----------|------|---------|
| **Embedding** | ~5ms per chunk | Using sentence-transformers |
| **Vector Search** | ~10ms | FAISS on CPU |
| **BM25 Search** | ~1-2ms | Pre-built index |
| **Reranking** | ~20-50ms | 15-20 results |
| **LLM Generation** | ~2-5s | API latency + processing |
| **Total Query** | ~3-7s | End-to-end |

---

## 🐛 Debugging & Troubleshooting

### Issue: "Documents not found"
```
ERROR: DOCUMENT_PATH not found
```
**Solution:**
```bash
mkdir data/documents
# Place your PDF files in the data/documents folder
```

### Issue: "No chunks created"
```
WARNING: No chunks created
```
**Solution:**
- Verify PDFs are valid and contain extractable text
- Check that documents are in `data/documents/`
- Test PDF extraction: `from backend.ingestion.loader import load_documents`

### Issue: "Embedding model not found"
**Solution:**
```bash
# Model will auto-download on first use
# Ensure internet connection and ~500MB disk space
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### Issue: BYTEZ_API_KEY not working
**Solution:**
1. Verify key is correct in `.env`
2. Check Bytez API status
3. Verify model availability: `google/gemini-2.5-flash`
4. Check API quota/rate limits

### Enable Debug Logging
```python
# In any module
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🔐 Security Considerations

- [ ] Environment variables stored in `.env` (not in repo)
- [ ] API credentials should never be committed
- [ ] CORS configured for production (currently allow all)
- [ ] Input validation on all endpoints
- [ ] Document upload restricted to safe file types

**For Production:**
```python
# In server.py, update CORS:
CORSMiddleware(
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 🚢 Deployment

### Environment Variables for Production
```env
BYTEZ_API_KEY=***
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=100
DOCUMENT_PATH=data/documents
VECTOR_DB_PATH=vector_store/faiss_index
DEBUG=False
```

### Run Production Server
```bash
uvicorn backend.api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence Transformers](https://www.sbert.net/)
- [Bytez API Docs](https://docs.bytez.ai/)
- [Rank-BM25](https://github.com/dorianbrown/rank_bm25)

---

## 📝 Project Statistics

- **Total Modules**: 15+ Python modules
- **Frontend**: 1 HTML file with embedded CSS/JS
- **Test Files**: 4 test/demo scripts
- **Vector DB**: FAISS-based (configurable size)
- **Supported Formats**: PDF, TXT, HTML, Markdown
- **Embedding Dimensions**: 384
- **Concurrent Requests**: Supports FastAPI async

---

## 🤝 Contributing

To extend ELKA:

1. **Add new document format**: Extend `backend/ingestion/loader.py`
2. **Add new connector**: Create file in `backend/connectors/`
3. **Customize prompts**: Edit `backend/llm/prompt.py`
4. **Improve reranking**: Modify `backend/retrieval/reranker.py`
5. **Add new API endpoints**: Extend `backend/api/server.py`

---

## 📄 License

This project is part of the ELka Enterprise Knowledge Assistant suite.

---

## 🎓 How It Works (Visual Guide)

```
[User Query]
    │
    ▼
┌─────────────────────────────┐
│ Query Rewriting with LLM     │
│ Makes query more specific    │
└─────────────────────────────┘
    │
    ▼
┌──────────────┬──────────────┐
│ Vector Search│ Keyword Search│ Hybrid Approach
│ (Semantic)   │ (BM25)       │ for completeness
└──────┬───────┴──────┬───────┘
       │              │
       └──────┬───────┘
              ▼
    ┌─────────────────────┐
    │ Deduplicate Results │
    │ ~15-20 chunks      │
    └─────────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │ Rerank by Relevance │
    │ Top 7 results       │
    └─────────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │ Generate Answer     │
    │ with LLM + Context  │
    └─────────────────────┘
              │
              ▼
    [Answer + Source Citations]
```

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Status**: Production Ready
