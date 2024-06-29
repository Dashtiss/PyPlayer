from moviepy.editor import AudioFileClip
import os
async def webm_to_mp3(webm_file, mp3_file):
    try:
        # Load the webm file
        audio_clip = AudioFileClip(webm_file)
        # Write the audio content to an mp3 file
        audio_clip.write_audiofile(mp3_file, codec='mp3')
        # Close the AudioFileClip
        audio_clip.close()
        print(f"Successfully converted {webm_file} to {mp3_file}")
        os.remove(webm_file)
    except Exception as e:
        print(f"An error occurred: {e}")