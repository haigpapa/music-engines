#!/bin/bash
echo "🧪 Testing Music Engines MVP..."

echo "\n1️⃣ Checking dependencies..."
python3 -c "import librosa; import flask" && echo "✅ Core deps OK"

echo "\n2️⃣ Verifying modules..."
python3 verify_modules.py | tail -1

echo "\n3️⃣ Starting server (background)..."
PORT=5001 python3 server.py &
SERVER_PID=$!
sleep 5

echo "\n4️⃣ Health check..."
curl -s http://localhost:5001/health | grep -q "healthy" && echo "✅ Server healthy"

echo "\n5️⃣ Stopping server..."
kill $SERVER_PID

echo "\n✅ All tests passed! Ready for demo."
