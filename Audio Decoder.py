import pyaudio
import numpy as np
import wave
import time

def create_frequency_lookup():
    return {
        1000: '0000', 1100: '0001', 1200: '0010', 1300: '0011',
        1400: '0100', 1500: '0101', 1600: '0110', 1700: '0111',
        1800: '1000', 1900: '1001', 2000: '1010', 2100: '1011',
        2200: '1100', 2300: '1101', 2400: '1110', 2500: '1111',
    }

def audio_to_binary(audio_data, sample_rate=44100, duration=0.1, chunk_size=1024):
    frequencies = create_frequency_lookup()

    binary_data = ""
    num_samples = len(audio_data)
    num_chunks = -(-num_samples // chunk_size)  # Equivalent to math.ceil(num_samples / chunk_size)

    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, num_samples)
        chunk = audio_data[start_idx:end_idx]

        # Perform Fourier Transform to get frequency components
        frequencies_chunk = np.fft.fft(chunk)
        frequencies_chunk = np.fft.fftfreq(len(chunk), d=1/sample_rate)

        # Find dominant frequency
        dominant_frequency = int(np.abs(frequencies_chunk[np.argmax(np.abs(frequencies_chunk))]))

        # Map frequency to 4-bit binary
        binary_data += create_frequency_lookup().get(dominant_frequency, '0000')

    return binary_data

def decode_binary_to_text(binary_data):
    text = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        text += chr(int(byte, 2))
    return text

def listen_and_decode():
    chunk_size = 1024
    sample_rate = 44100
    audio_format = pyaudio.paInt16
    channels = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=audio_format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Listening... Press Ctrl+C to stop.")

    try:
        while True:
            audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
            binary_data = audio_to_binary(audio_data)
            decoded_text = decode_binary_to_text(binary_data)
            print(f"Decoded Text: {decoded_text}")
            time.sleep(0.1)  # Adjust sleep duration based on your needs

    except KeyboardInterrupt:
        print("\nStopped listening.")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    listen_and_decode()
