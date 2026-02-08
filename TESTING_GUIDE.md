# Music Engines MVP - Testing Guide

## Quick Test Checklist

Run these tests on your local machine to verify everything works:

---

## Test 1: Dependencies Check

```bash
cd music-engines

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Verify critical imports
python3 -c "import librosa; import flask; import flask_cors; print('✅ Core dependencies installed')"
```

**Expected:** No errors, confirmation message printed

---

## Test 2: Module Verification

```bash
python3 verify_modules.py
```

**Expected Output:**
```
Scanning totality_engine/engines...
...
Summary: 23/23 modules passed.
```

**If you see failures:**
- Check which module failed
- Look for missing dependencies
- Install missing packages

---

## Test 3: Server Startup

```bash
python3 server.py
```

**Expected Output:**
```
Initializing Music Engines Pipeline...
Pipeline initialized successfully.
 * Running on http://0.0.0.0:5000
```

**If server doesn't start:**
- Check port 5000 isn't already in use
- Check all dependencies installed
- Look at error messages

---

## Test 4: Health Check

**Keep server running, open new terminal:**

```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "pipeline_ready": true
}
```

---

## Test 5: Frontend Loading

**With server running, open browser:**

1. Go to: `http://localhost:5000`
2. You should see:
   - "TOTALITY ENGINE" header
   - "SYSTEM READY" indicator
   - Upload drop zone
   - "Upload Track" section

**Visual checklist:**
- [ ] Page loads without errors
- [ ] Dark theme displays correctly
- [ ] Drop zone is visible
- [ ] "INITIALIZE ANALYSIS" button is disabled (no file uploaded yet)

---

## Test 6: File Upload (UI Test)

**Find a test MP3 file (any music file will work):**

1. Drag MP3 onto the drop zone
2. **Expected:**
   - Drop zone updates with filename
   - Shows file size
   - "INITIALIZE ANALYSIS" button becomes enabled
   - File name appears in results header

---

## Test 7: Full Analysis (End-to-End)

**With file uploaded:**

1. Click "INITIALIZE ANALYSIS"
2. **Expected:**
   - Button text changes to "ANALYZING..."
   - Loading bar appears
   - Analysis runs (may take 10-30 seconds)
   - Results appear below

**Results should show cards for:**
- [ ] Creative Metrics (tempo, spectral flux, explicitness)
- [ ] Platform Performance (viral elasticity)
- [ ] Market Risk
- [ ] Audience Impact
- [ ] Industry Connectivity

3. Click "Raw Data Payload" dropdown
4. **Expected:** JSON output displays

---

## Test 8: API Test (cURL)

**With server running and a test MP3 file:**

```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@/path/to/your/test.mp3" \
  -F "artist_id=test_artist" \
  -F "target_markets=US,UK"
```

**Expected:** JSON response with analysis results

**If it fails:**
- Check file path is correct
- Verify file is a supported format (.mp3, .wav, .flac, .ogg, .aiff)
- Check server logs for error messages

---

## Test 9: Error Handling

**Test 1: Wrong file type**
```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@/path/to/some/document.txt"
```

**Expected:** 400 error with message "File type not allowed"

**Test 2: No file**
```bash
curl -X POST http://localhost:5000/analyze
```

**Expected:** 400 error with message "No file part"

---

## Test 10: Multiple Files

**Upload and analyze 3 different songs:**

1. Upload first song → Analyze
2. Check results clear
3. Upload second song → Analyze
4. Upload third song → Analyze

**Expected:** Each analysis completes successfully, no errors accumulate

---

## Common Issues & Fixes

### Issue: `ModuleNotFoundError: No module named 'librosa'`
**Fix:**
```bash
pip install librosa --break-system-packages
```

### Issue: `ModuleNotFoundError: No module named 'flask'`
**Fix:**
```bash
pip install flask flask-cors --break-system-packages
```

### Issue: Server won't start - "Address already in use"
**Fix:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or run server on different port
PORT=5001 python3 server.py
```

### Issue: Frontend shows "Network error. Is the server running?"
**Check:**
1. Is server actually running? (check terminal)
2. Is it on port 5000? (check server output)
3. Try accessing `http://localhost:5000/health` directly in browser

### Issue: Analysis takes forever / hangs
**Possible causes:**
- Very large audio file (try with smaller file)
- Missing audio processing libraries (check librosa/ffmpeg installed)
- Check server logs for errors

### Issue: Results show "N/A" for everything
**Possible causes:**
- Audio analysis failed silently
- Check server logs for warnings
- Try different audio file

---

## Performance Benchmarks

**Expected analysis times:**
- 30-second song: ~5-15 seconds
- 3-minute song: ~15-30 seconds
- 10-minute song: ~30-60 seconds

*Times vary based on CPU speed and file format*

---

## What Success Looks Like

After running all tests, you should have:

✅ All 23 modules verified
✅ Server starts without errors
✅ Frontend loads correctly
✅ Can upload files via drag-drop
✅ Analysis completes and shows results
✅ Results display in organized cards
✅ Raw JSON available
✅ Can analyze multiple files in sequence
✅ Error handling works

---

## Recording Your Demo

**Once everything works:**

1. **Screen Recording Setup:**
   - Use Loom, OBS, or QuickTime
   - Set resolution to 1920x1080
   - Include your face in corner (optional but good)

2. **Demo Script (5 minutes):**
   ```
   0:00-0:30 - The Problem
   "Music analysis is fragmented. I built a system
   that analyzes across all dimensions simultaneously."

   0:30-1:00 - Show the UI
   Open http://localhost:5000
   Highlight the clean interface

   1:00-2:00 - Upload & Analyze
   Drag a song onto the drop zone
   Click analyze
   Show the loading state

   2:00-4:00 - Results Walkthrough
   Show each category of results
   Highlight one interesting metric
   Open the raw JSON

   4:00-5:00 - The Vision
   "This is the foundation of the Resonance Atlas"
   "What we can build next: knowledge graph,
   AI latent space analysis, cross-domain connections"
   ```

3. **Technical Notes:**
   - Use a recognizable song (but blur the name if needed)
   - Keep the demo moving (don't let long waits kill momentum)
   - Show confidence (this is YOUR system)

---

## Deployment Test (Optional)

**If you want to deploy publicly:**

### Quick Deploy to Render.com (Free Tier):

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: music-engines
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python server.py"
```

2. Push to GitHub
3. Connect to Render
4. Wait for deploy (~5-10 minutes)
5. Get public URL

**Expected:** System accessible at `https://your-app.onrender.com`

---

## Pre-Submission Checklist

Before using this in applications:

- [ ] All tests pass
- [ ] Demo video recorded (5 minutes)
- [ ] Screenshots captured
- [ ] GitHub repo is public (or ready to share)
- [ ] README.md written
- [ ] ARCHITECTURE.md written
- [ ] requirements.txt is complete
- [ ] .gitignore excludes temp files

---

## Quick Test Command (All in One)

```bash
#!/bin/bash
echo "🧪 Testing Music Engines MVP..."

echo "\n1️⃣ Checking dependencies..."
python3 -c "import librosa; import flask" && echo "✅ Core deps OK"

echo "\n2️⃣ Verifying modules..."
python3 verify_modules.py | tail -1

echo "\n3️⃣ Starting server (background)..."
python3 server.py &
SERVER_PID=$!
sleep 5

echo "\n4️⃣ Health check..."
curl -s http://localhost:5000/health | grep -q "healthy" && echo "✅ Server healthy"

echo "\n5️⃣ Stopping server..."
kill $SERVER_PID

echo "\n✅ All tests passed! Ready for demo."
```

Save this as `test.sh`, run `chmod +x test.sh`, then `./test.sh`

---

## Support

**If tests fail:**
1. Check error messages carefully
2. Look at server logs (terminal where server is running)
3. Check browser console (F12) for frontend errors
4. Verify all dependencies installed

**The system is well-built. If tests fail, it's likely:**
- Missing dependency
- Wrong file path
- Port conflict
- File format issue

**All fixable in minutes.**

---

**Now go test it. You've built something real. Verify it works. Then ship.**
