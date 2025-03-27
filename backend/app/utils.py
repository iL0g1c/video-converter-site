import subprocess

def convert_video(input_path: str, output_path: str, format: str):
    # Define encoding options based on format
    codec_map = {
        "mp4": ["libx264", "aac"],
        "avi": ["mpeg4", "mp3"],
        "mkv": ["libx264", "aac"]
    }

    if format not in codec_map:
        raise ValueError(f"Unsupported format: {format}")

    video_codec, audio_codec = codec_map[format]

    command = [
        "ffmpeg", "-i", input_path,
        "-c:v", video_codec, "-preset", "fast",
        "-c:a", audio_codec, output_path
    ]
    subprocess.run(command, check=True)
