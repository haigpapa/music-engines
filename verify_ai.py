import os
import sys
import logging
import numpy as np

# Ensure project root is in path
sys.path.append(os.getcwd())

from totality_engine.engines.creative.deep_listening import DeepListeningEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_ai_engine():
    print("🤖 Verifying Deep Listening Engine...")
    
    # Check if test file exists
    test_file = "ai_test.wav"
    if not os.path.exists(test_file):
        print(f"❌ Test file {test_file} not found. Please create it first.")
        sys.exit(1)
        
    try:
        # Instantiate Engine (this downloads/loads model)
        engine = DeepListeningEngine()
        
        if not engine.model:
            print("⚠️ Transformers/Model not loaded. Verification likely to fail (fallback mode).")
        
        # Run Analysis
        print(f"Analyzing {test_file}...")
        result = engine.analyze(test_file)
        
        # Check Result
        if result.get("status") == "success":
            embedding = result.get("embedding")
            dims = len(embedding)
            print(f"✅ Success! Generated embedding with {dims} dimensions.")
            
            if dims == 768: # AST default
                print("✅ Dimensions match expected AST model output (768).")
            else:
                 print(f"⚠️ Unexpected dimensions: {dims} (expected 768).")
                 
            # Check for non-zero values (real inference)
            if np.sum(np.abs(embedding)) > 0:
                print("✅ Embedding contains non-zero values (inference working).")
            else:
                print("⚠️ Embedding is all zeros (fallback or error).")
                
        else:
            print(f"❌ Analysis failed: {result.get('error')}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Verification crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify_ai_engine()
