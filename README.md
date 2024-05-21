# Split Clip

## Description
This Python script, `split_clip.py`, allows you to split a video clip into two halves with a 10 second gap in between. It takes two inputs: the path to the video file you want to split and the path to the output directory where the split clips will be saved.

## Prerequisites
- Python 3.x
- FFmpeg (installed and added to the system's PATH)

## Installation
1. Clone this repository: `git clone https://github.com/lizhagearty/split-clip.git`
2. Navigate to the project directory: `cd split-clip`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage
1. Open a terminal and navigate to the project directory.
2. Run the script with the following command:
    ```
    python split_clip.py /path/to/video/file /path/to/output/directory
    ```
    Replace `/path/to/video/file` with the actual path to your video file and `/path/to/output/directory` with the desired output directory.
3. The script will split the video clip into two segments, with a 10 second gap in between the clips 

## Import 
Import the generated OTIO file into DaVinci Resolve:

Open DaVinci Resolve.
Go to `File > Import > Timeline.`
Select the `output.otio` file.

## Script Details
The script performs the following steps:

Splits the input video into two halves.
Inserts a 10-second gap between the two clips.
Handles both video and audio tracks.
Outputs the result as an OTIO file.