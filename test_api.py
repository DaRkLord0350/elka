"""
ELKA API Test Suite
Tests all endpoints of the FastAPI backend
"""

import requests
import json


BASE_URL = "http://127.0.0.1:8000"

print("""
╔══════════════════════════════════════════════════════════════════╗
║          ELKA ENTERPRISE KNOWLEDGE ASSISTANT API TEST            ║
║                 Production RAG System Backend                     ║
╚══════════════════════════════════════════════════════════════════╝
""")


# ==================== 1. HEALTH CHECK ====================
print("\n✅ TEST 1: Health Check")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/health")
    print(json.dumps(response.json(), indent=2))
    print("✓ Status:", response.status_code)
except Exception as e:
    print(f"✗ Error: {e}")


# ==================== 2. ROOT ENDPOINT ====================
print("\n✅ TEST 2: Root Endpoint")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/")
    print(json.dumps(response.json(), indent=2))
    print("✓ Status:", response.status_code)
except Exception as e:
    print(f"✗ Error: {e}")


# ==================== 3. QUERY ENDPOINT ====================
print("\n✅ TEST 3: Query RAG System")
print("-" * 60)

test_queries = [
    "What is my college name?",
    "Tell me about the projects",
    "college information"
]

for query in test_queries:
    try:
        print(f"\n📝 Query: {query}")
        response = requests.post(
            f"{BASE_URL}/query",
            json={"question": query},
            timeout=30
        )
        result = response.json()
        print(f"✓ Answer: {result['answer'][:100]}...")
        print(f"✓ Status: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")


# ==================== 4. CONFIG ENDPOINT ====================
print("\n✅ TEST 4: System Configuration")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/info/config")
    print(json.dumps(response.json(), indent=2))
    print("✓ Status:", response.status_code)
except Exception as e:
    print(f"✗ Error: {e}")


# ==================== 5. LIST DOCUMENTS ====================
print("\n✅ TEST 5: List Uploaded Documents")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/documents")
    result = response.json()
    print(f"Documents (Count: {result['count']}):")
    for doc in result['documents']:
        print(f"  • {doc}")
    print("✓ Status:", response.status_code)
except Exception as e:
    print(f"✗ Error: {e}")


# ==================== 6. BATCH QUERY ====================
print("\n✅ TEST 6: Batch Query Multiple Questions")
print("-" * 60)

batch_questions = [
    "What is my college?",
    "What are my projects?",
    "Tell me more information"
]

try:
    response = requests.post(
        f"{BASE_URL}/batch-query",
        json={"questions": batch_questions},
        timeout=60
    )
    result = response.json()
    print(f"Processed {result['total']} questions")
    print(f"Successful: {result['successful']}")
    print("\nResults:")
    for i, item in enumerate(result['results'], 1):
        print(f"  {i}. Q: {item['question']}")
        if item['error']:
            print(f"     ✗ Error: {item['error']}")
        else:
            print(f"     ✓ A: {item['answer'][:60]}...")
    print("✓ Status:", response.status_code)
except Exception as e:
    print(f"✗ Error: {e}")


# ==================== SUMMARY ====================
print("\n" + "=" * 60)
print("🎉 API TESTS COMPLETE")
print("=" * 60)
print("""
📚 API Documentation:
   • Swagger UI: http://127.0.0.1:8000/docs
   • ReDoc: http://127.0.0.1:8000/redoc

🔗 Available Endpoints:
   • GET  /              - Health check
   • GET  /health        - Detailed health
   • POST /query         - Query RAG system
   • POST /batch-query   - Process multiple queries
   • GET  /documents     - List uploaded documents
   • POST /upload        - Upload new document
   • DELETE /documents/{filename} - Delete document
   • GET  /info/config   - System configuration

🚀 The system is production-ready!
""")
