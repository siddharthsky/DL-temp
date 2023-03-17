import cv2
import os
import pandas as pd

# Define input parameters
video_links = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2",
    "https://www.youtube.com/watch?v=video3"
]
output_path = "c:/hyna/god/GGT/DL/"

# Initialize dataframe to store video information
video_df = pd.DataFrame(columns=["video_id", "video_url", "video_parts", "frame_rate"])

# Loop through each video link and extract information
for i, video_link in enumerate(video_links):
    # Extract video ID and URL from video link
    video_id = f"video{i+1}"
    video_url = video_link
    
    # Download video from YouTube using youtube-dl
    os.system(f"youtube-dl -f mp4 {video_url} -o {video_id}.mp4")

    # Open video using OpenCV
    cap = cv2.VideoCapture(f"{video_id}.mp4")
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_duration = num_frames / frame_rate

    # Split video into 10-second chunks
    chunk_length = 10
    chunk_start = 0
    chunk_end = chunk_start + chunk_length
    part_num = 1
    video_parts = []
    while chunk_start < video_duration:
        # Set output path for chunk
        output_chunk_path = os.path.join(output_path, f"{video_id}-p{part_num}.mp4")

        # Use OpenCV to extract chunk from video
        cap.set(cv2.CAP_PROP_POS_FRAMES, chunk_start * frame_rate)
        out = cv2.VideoWriter(output_chunk_path, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (int(cap.get(3)), int(cap.get(4))))
        while cap.get(cv2.CAP_PROP_POS_FRAMES) < chunk_end * frame_rate:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
        out.release()

        # Add chunk information to video_parts list
        video_parts.append(f"{video_id}-p{part_num}.mp4")
        part_num += 1

        # Update chunk start and end times
        chunk_start = chunk_end
        chunk_end = chunk_start + chunk_length

    # Convert bitrate to 2 frames per second
    bitrate = int(num_frames / video_duration * 2)

    # Add video information to dataframe
    video_df = video_df.append({
        "video_id": video_id,
        "video_url": video_url,
        "video_parts": ", ".join(video_parts),
        "frame_rate": frame_rate,
        "bitrate": bitrate
    }, ignore_index=True)

    # Release video capture object
    cap.release()

# Print final dataframe
print(video_df)
