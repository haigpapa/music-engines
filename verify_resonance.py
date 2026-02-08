import os
import sys
import logging
import numpy as np

# Ensure project root is in path
sys.path.append(os.getcwd())

from totality_engine.engines.creative.resonance import ResonanceEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_resonance():
    print("🔮 Verifying Resonance Engine (Cross-Modal)...")
    
    try:
        engine = ResonanceEngine()
        
        if not engine.sentiment_analyzer:
            print("⚠️ Sentiment model not loaded. Verification will fail or skip.")
            
        # Test Case 1: High Dissonance (Happy Audio, Sad Text)
        print("\n--- Test Case 1: Dissonance (Happy Music / Sad Lyrics) ---")
        lyrics = "I am so lonely and the darkness surrounds me. Only pain remains."
        # Mock "Happy/High Energy" embedding (large norm)
        embedding_happy = [10.0] * 768 
        audio_features = {"embedding": embedding_happy}
        
        result = engine.analyze(lyrics, audio_features)
        print(f"Lyrics: '{lyrics}'")
        print(f"Result: {result}")
        
        if result['status'] == 'success':
            print(f"✅ Vibe: {result['vibe']}")
            print(f"✅ Dissonance: {result['dissonance_score']:.2f}")
            if result['lyrical_sentiment'] == 'NEGATIVE':
                print("✅ Correctly identified NEGATIVE lyrics.")
            else:
                 print(f"❌ Failed sentiment analysis. Got {result['lyrical_sentiment']}")
        else:
            print(f"❌ Analysis failed: {result.get('error')}")

        # Test Case 2: Alignment (Happy Music / Happy Text)
        print("\n--- Test Case 2: Alignment (Happy Music / Happy Lyrics) ---")
        lyrics_happy = "The sun is shining and I feel alive! Everything is wonderful!"
        
        result_aligned = engine.analyze(lyrics_happy, audio_features)
        print(f"Lyrics: '{lyrics_happy}'")
        print(f"Result: {result_aligned}")

        if result_aligned['status'] == 'success':
            print(f"✅ Vibe: {result_aligned['vibe']}")
            print(f"✅ Dissonance: {result_aligned['dissonance_score']:.2f}")
            if result_aligned['lyrical_sentiment'] == 'POSITIVE':
                print("✅ Correctly identified POSITIVE lyrics.")
                
            if result_aligned['dissonance_score'] < result['dissonance_score']:
                 print("✅ Logic Check: Aligned Dissonance < Clashing Dissonance")
            else:
                 print("⚠️ Dissonance calculation logic might be off.")

    except Exception as e:
        print(f"❌ Verification crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    verify_resonance()
