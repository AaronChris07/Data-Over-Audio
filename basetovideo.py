import pybase64

def decode_base64_to_video(base64_encoded_video, output_video_path):
    try:
        # Decode the Base64-encoded string to bytes
        decoded_video = pybase64.b64decode(base64_encoded_video.encode("utf-8"))
        
        # Write the decoded bytes to the output video file
        with open(output_video_path, "wb") as output_video_file:
            output_video_file.write(decoded_video)
        
        print(f"Video decoded from Base64 and saved to '{output_video_path}' successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the path to the text file containing the Base64-encoded video
input_file_path = '1234.txt'

# Specify the path for the output video file
output_video_path = 'decoded_video.mp4'

# Read the Base64-encoded video from the text file
with open(input_file_path, 'r') as input_file:
    base64_encoded_video = input_file.read()

# Decode the Base64-encoded video and save it to the output video file
decode_base64_to_video(base64_encoded_video, output_video_path)
