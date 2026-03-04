"""
Test script to demonstrate the Query Rewriting Engine impact.
This shows how short vague queries get improved before retrieval.
"""

from backend.api.query import ask_question

# Test queries that would normally be too vague
test_queries = [
    "college name",
    "project details",
    "my work"
]

print("\n" + "="*70)
print("🔍 QUERY REWRITING ENGINE DEMONSTRATION")
print("="*70)

for i, query in enumerate(test_queries, 1):
    print(f"\n\n{'='*70}")
    print(f"TEST {i}: Testing with vague query")
    print(f"{'='*70}")
    
    try:
        response = ask_question(query)
        print("\n")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*70)
print("✅ QUERY REWRITING ENGINE DEMO COMPLETE")
print("="*70)
