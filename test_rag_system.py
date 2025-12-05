import os
import sys
sys.path.append('.')

print("🔧 Testing RAG QC Document System...")

try:
    from services.rag_agent import build_or_load_qc_index
    print("✅ RAG agent imported successfully")
    
    # Check if QC docs exist
    qc_dir = "./qc_docs"
    if os.path.exists(qc_dir):
        files = os.listdir(qc_dir)
        print(f"📁 QC documents found: {files}")
    else:
        print("❌ QC docs directory not found")
        exit(1)
    
    # Try to build index
    print("🔨 Building QC document index...")
    vectordb = build_or_load_qc_index()
    print("✅ QC document index built successfully!")
    
    # Test retrieval
    print("🔍 Testing document retrieval...")
    results = vectordb.similarity_search("solder joint defects", k=3)
    print(f"📄 Retrieved {len(results)} relevant documents")
    
    for i, doc in enumerate(results):
        print(f"  {i+1}. {doc.page_content[:100]}...")
        
except Exception as e:
    print(f"❌ RAG system error: {e}")
    import traceback
    traceback.print_exc()
