import os
import sys
sys.path.append('.')

from app import create_app

print("🔧 Testing RAG QC Document System with Flask context...")

app = create_app()

with app.app_context():
    try:
        from services.rag_agent import build_or_load_qc_index, analyze_defects_with_standards
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
        
        # Test the actual RCA function
        print("🤖 Testing RCA analysis with standards...")
        product_ctx = {
            "line": "Line 2",
            "product": "PCB-X120", 
            "lot": "L24-0093",
            "ipc_class": "Class 2"
        }
        
        mock_detections = [
            {"type": "bottle", "confidence": 0.85},
            {"type": "chair", "confidence": 0.72}
        ]
        
        rca_result = analyze_defects_with_standards(product_ctx, mock_detections)
        print("✅ RCA analysis completed!")
        print("📊 RCA Result:")
        print(f"   Defect Type: {rca_result.get('defect_type', 'N/A')}")
        print(f"   Risk Level: {rca_result.get('risk_level', 'N/A')}")
        print(f"   Root Causes: {rca_result.get('root_causes', [])}")
        
    except Exception as e:
        print(f"❌ RAG system error: {e}")
        import traceback
        traceback.print_exc()
