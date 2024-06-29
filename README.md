# PyPlayer

This is a Discord bot built with `discord.py` that can play audio from YouTube and files uploaded by users.

## Features

- Play audio from YouTube URLs
- Play audio from files uploaded by users

## Requirements

- Python 3.7 or higher
- `discord.py` library
- `yt_dlp` library
- `ffmpeg` installed and added to your system PATH

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/Dashtiss/PyPlayer.git
    cd PyPlayer
    ```

2. **Install the required libraries**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your Discord bot token**

    - Create a `.env` file in the root directory of your project.
    - Add your Discord bot token to the `.env` file:

    ```env
    TOKEN=your-bot-token
    ```

4. **(OPTIONAL) Set up your VirusTotal API key**

    - Add your VirusTotal API key to the `.env` file:

    ```env
    VirusTotalAPIKEY=your-virustotal-apikey
    ```

5. **Install FFmpeg**

    - Follow the instructions on the [FFmpeg website](https://ffmpeg.org/download.html) to download and install FFmpeg.
    - Make sure FFmpeg is added to your system PATH.

## Usage

1. **Run the bot**

    ```bash
    python Run.py
    ```

2. **Bot Commands**

    - **Join Voice Channel**
    
      Command: `!join`
      
      Makes the bot join the voice channel you are currently in.

    - **Play Audio from YouTube**
    
      Command: `!play <YouTube URL or FILE>`
      
      Plays the audio from the provided YouTube URL.

    - **Stop Audio**
    
      Command: `!stop`
      
      Stops the audio and makes the bot leave the voice channel.
    - **unpause**
      Command: `!unpause`

      Unpauses the audio

## Example Commands

- `!join`
- `!play https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- `!play` (upload an audio file after sending the command)
- `!stop`
- `!unpause`

## Contributing

Feel free to submit issues and pull requests to the repository. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
