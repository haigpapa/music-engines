import requests
import time
import os
import sys

# Configuration
BASE_URL = "http://localhost:5001"
AUDIO_FILE = "ai_test_sine.wav"

def verify_async_flow():
    print(f"--- Verifying Async Analysis Flow ---")
    
    # 1. Upload File
    params = {"lyrics": "I am so happy!", "artist_id": "test_user"}
    print(f"Uploading {AUDIO_FILE}...")
    
    with open(AUDIO_FILE, 'rb') as f:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/analyze", files={"file": f}, data=params)
        duration = time.time() - start_time
    
    # Assertion: Request should be FAST (< 1 second), not blocking
    print(f"Request duration: {duration:.2f}s")
    if duration > 2.0:
        print("❌ FAILURE: /analyze took too long! It seems blocking.")
        sys.exit(1)
        
    if response.status_code != 202:
        print(f"❌ FAILURE: Expected 202, got {response.status_code}")
        print(response.text)
        sys.exit(1)
        
    data = response.json()
    job_id = data.get("job_id")
    print(f"✅ Upload accepted. Job ID: {job_id}")
    
    # 2. Poll for Completion
    print("Polling for results...")
    max_retries = 30
    for i in range(max_retries):
        res = requests.get(f"{BASE_URL}/jobs/{job_id}")
        status_data = res.json()
        status = status_data.get("status")
        print(f"Poll {i+1}: {status}")
        
        if status == "completed":
            print("✅ Analysis Complete!")
            # Basic validation of result structure
            result = status_data.get("result", {})
            if "resonance" in result:
                print(f"   Vibe: {result['resonance'].get('vibe')}")
            else:
                print("⚠️ Warning: Result structure missing 'resonance'")
            break
            
        if status == "failed":
            print(f"❌ Analysis Failed: {status_data.get('error')}")
            sys.exit(1)
            
        time.sleep(2)
    else:
        print("❌ Timeout waiting for job completion.")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(AUDIO_FILE):
        print("Generating test file...")
        # Simple sine wave generator if missing
        import wave, struct, math
        sample_rate = 44100
        duration = 1.0 # seconds
        frequency = 440.0
        obj = wave.open(AUDIO_FILE,'w')
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(sample_rate)
        for i in range(int(duration * sample_rate)):
            value = int(32767.0*math.sin(frequency*math.pi*2*i/sample_rate))
            data = struct.pack('<h', value)
            obj.writeframesraw( data )
        obj.close()
        
    verify_async_flow()
