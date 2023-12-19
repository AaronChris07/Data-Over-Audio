import sounddevice as sd
import numpy as np
from scipy.signal import find_peaks
from queue import Queue
import threading

# Constants for modulation
duration = 0.1
sample_rate = 44100

# Frequency pairs for decoding
decode_frequencies = {'00': 1000, '01': 1500, '10': 2000, '11': 2500}

# Threshold for peak detection
threshold = 0.5

# Buffer to store received audio samples
audio_buffer = Queue()

def callback(indata, frames, time, status):
    if status:
        print("Error:", status)
    audio_buffer.put(indata.copy())

def decode_signal(signal):
    peaks, _ = find_peaks(signal, height=threshold)
    bit_pairs = []

    for i in range(0, len(peaks), int(sample_rate * duration)):
        start = peaks[i]
        end = peaks[i + 1] if i + 1 < len(peaks) else len(signal)
        frequency = int(np.mean(signal[start:end]))

        # Find the closest frequency pair
        bit_pair = min(decode_frequencies, key=lambda x: abs(decode_frequencies[x] - frequency))
        bit_pairs.append(bit_pair)

    return bit_pairs

def decode_audio():
    while True:
        if not audio_buffer.empty():
            audio_data = audio_buffer.get()
            audio_signal = np.mean(audio_data, axis=1)
            bit_pairs = decode_signal(audio_signal)
            decoded_text = ''.join(bit_pair for bit_pair in bit_pairs)
            print("Decoded Text:", decoded_text)

def main():
    # Start the live decoder in a separate thread
    decoder_thread = threading.Thread(target=decode_audio, daemon=True)
    decoder_thread.start()

    # Start capturing audio
    with sd.InputStream(callback=callback):
        print("Live decoder is running. Press Ctrl+C to exit.")
        sd.sleep(2**31)  # Sleep for a very long time, decoder will run in a separate thread

if __name__ == "__main__":
    main()
