import numpy as np
import wave
import struct

sample_rate = 16000
duration = 5.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
frequency = 440.0 # A4 note
# Create sine wave
audio = 0.5 * np.sin(2 * np.pi * frequency * t)
# Convert to 16-bit PCM
audio_int16 = (audio * 32767).astype(np.int16)

with wave.open('ai_test_sine.wav', 'w') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_int16.tobytes())
