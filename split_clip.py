import opentimelineio as otio
import argparse
import ffmpeg
import os

def get_video_duration(input_file):
    try:
        probe = ffmpeg.probe(input_file)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        return float(video_info['duration'])
    except ffmpeg.Error as e:
        print(f"Error probing video file: {e.stderr.decode('utf-8')}")
        raise

def create_split_clips(input_file, output_file):
    # Get the absolute path of the input file
    input_file_path = os.path.abspath(input_file)

    # Create an empty timeline
    timeline = otio.schema.Timeline(name="SplitClips")
    
    # Create the input media reference with full path
    media_ref = otio.schema.ExternalReference(target_url=input_file_path)
    
    # Get the actual duration of the video
    try:
        video_duration = get_video_duration(input_file_path)
    except Exception as e:
        print(f"Failed to get video duration: {e}")
        return
    
    # Calculate the half duration
    half_duration = video_duration / 2
    frame_rate = 24  # Assuming 24 fps
    gap_duration = 10  # 10 seconds gap
    
    # Create the first half clip for video
    first_half_video_clip = otio.schema.Clip(
        name="First Half Video",
        media_reference=media_ref,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, frame_rate),
            duration=otio.opentime.RationalTime(half_duration * frame_rate, frame_rate)
        )
    )
    
    # Create the second half clip for video
    second_half_video_clip = otio.schema.Clip(
        name="Second Half Video",
        media_reference=media_ref,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(half_duration * frame_rate, frame_rate),
            duration=otio.opentime.RationalTime(half_duration * frame_rate, frame_rate)
        )
    )
    
    # Create the first half clip for audio
    first_half_audio_clip = otio.schema.Clip(
        name="First Half Audio",
        media_reference=media_ref,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, frame_rate),
            duration=otio.opentime.RationalTime(half_duration * frame_rate, frame_rate)
        )
    )
    
    # Create the second half clip for audio
    second_half_audio_clip = otio.schema.Clip(
        name="Second Half Audio",
        media_reference=media_ref,
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(half_duration * frame_rate, frame_rate),
            duration=otio.opentime.RationalTime(half_duration * frame_rate, frame_rate)
        )
    )
    
    # Create gaps for video and audio
    video_gap = otio.schema.Gap(
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, frame_rate),
            duration=otio.opentime.RationalTime(gap_duration * frame_rate, frame_rate)
        )
    )

    audio_gap = otio.schema.Gap(
        source_range=otio.opentime.TimeRange(
            start_time=otio.opentime.RationalTime(0, frame_rate),
            duration=otio.opentime.RationalTime(gap_duration * frame_rate, frame_rate)
        )
    )
    
    # Add video clips and gap to video track
    video_track = otio.schema.Track(name="Video")
    video_track.append(first_half_video_clip)
    video_track.append(video_gap)
    video_track.append(second_half_video_clip)
    
    # Add audio clips and gap to audio track
    audio_track = otio.schema.Track(name="Audio", kind=otio.schema.TrackKind.Audio)
    audio_track.append(first_half_audio_clip)
    audio_track.append(audio_gap)
    audio_track.append(second_half_audio_clip)
    
    # Add tracks to timeline
    timeline.tracks.append(video_track)
    timeline.tracks.append(audio_track)
    
    # Write the timeline to an OTIO file
    otio.adapters.write_to_file(timeline, output_file)

def main():
    parser = argparse.ArgumentParser(description="Split a video file into two halves with a gap between the clips")
    parser.add_argument("input_file", help="Path to the input video file (.mov, .mp4, etc.)")
    parser.add_argument("output_file", help="Path to the output OTIO file")
    
    args = parser.parse_args()
    
    create_split_clips(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
