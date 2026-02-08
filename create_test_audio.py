import wave
import struct

# Create a 1-second silent WAV file
sample_rate = 44100
duration = 1.0
num_frames = int(duration * sample_rate)

with wave.open('test_audio.wav', 'w') as wav_file:
    wav_file.setnchannels(1) # Mono
    wav_file.setsampwidth(2) # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    
    data = struct.pack('<' + 'h'*num_frames, *([0]*num_frames))
    wav_file.writeframes(data)

print("Created test_audio.wav")
