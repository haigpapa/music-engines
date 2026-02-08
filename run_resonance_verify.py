import os
import time
import subprocess
import requests

def run_tests():
    print("🚀 Starting Resonance Engine Verification...")
    
    # 1. Cleanup
    subprocess.run(["pkill", "-f", "server.py"])
    if os.path.exists("totality.db"):
        os.remove("totality.db")
    
    # 2. Start Server
    print("Starting server on port 5001...")
    server_process = subprocess.Popen(
        ["python3", "server.py"],
        env={**os.environ, "PORT": "5001"}
    )
    
    # Wait for server and models to load (takes time due to 2 AI models)
    print("Waiting 20s for server/models...")
    time.sleep(20)
    
    try:
        # 3. Run Analysis
        print("Running Analysis...")
        files = {'file': open('ai_test_sine.wav', 'rb')}
        data = {
            'artist_id': 'resonance_verified',
            'target_markets': 'RES_VERIFY',
            'lyrics': 'I am so happy and joyful today!'
        }
        res = requests.post('http://localhost:5001/analyze', files=files, data=data)
        print(f"Analysis Status: {res.status_code}")
        
        if res.status_code == 200:
            result_json = res.json()
            resonance = result_json['results'].get('resonance', {})
            print(f"Resonance Result: {resonance}")
            
            if 'dissonance_score' in resonance:
                print("✅ Resonance metrics found in response.")
            else:
                print("❌ Missing resonance metrics.")
        else:
            print(f"❌ Analysis failed: {res.text}")

        # 4. Check History
        print("Checking History...")
        hist_res = requests.get('http://localhost:5001/history')
        if hist_res.status_code == 200:
            history = hist_res.json()
            print(f"History: {history}")
            if len(history) > 0 and history[0]['artist_id'] == 'resonance_verified':
                print("✅ Result persisted correctly.")
            else:
                print("❌ Result not found in history.")
        else:
             print(f"❌ History check failed: {hist_res.text}")
             
    except Exception as e:
        print(f"❌ Verification crashed: {e}")
    finally:
        print("Stopping server...")
        server_process.terminate()

if __name__ == "__main__":
    run_tests()
