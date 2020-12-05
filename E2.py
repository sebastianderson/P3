import numpy as np
import numpy as np
import os
import subprocess
import collections


def MP4(video, audio, subtitles, output):
    """
    Creates an mp4 container
    video:filename of the video
    audio:filename of the audio
    subtitles:filename of the subtitles
    output:name of the output you want
    """
    cmd = [
        "ffmpeg",
        "-i",
        video,
        "-i",
        audio,
        "-shortest",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "256k",
        "-ac",
        "1",
        output,
    ]
    # to convert a list to string we use join
    separator = " "
    com = separator.join(cmd)
    # use the command
    os.system(com)
    cmd = [
        "ffmpeg",
        "-i",
        video,
        "-i",
        subtitles,
        "-c copy",
        "-c:s",
        "mov_text",
        output,
    ]
    # to convert a list to string we use join
    separator = " "
    com = separator.join(cmd)
    # use the command
    os.system(com)


# test
MP4("BBB_10.avi", "BBB_mono.wav", "BBB.srt", "probamp4.mp4")
