import numpy as np
import os
import subprocess
import E3

# create different files to check formats
os.system("ffmpeg -i BBB_10.avi -c:v mpeg2video BBB1.mpg")
os.system("ffmpeg -i BBB_10.avi -c:v h264 -c:a aac BBB2.mp4")
os.system("ffmpeg -i BBB_10.avi -c:v h264 -c:a ac3 BBB3.mp4")
os.system("ffmpeg -i BBB_10.avi -c:v mpeg2video -c:a mp3 BBB4.mpg")
# check broadcast standard compatibility
E3.CompatibleBroadcast("BBB1.mpg")
E3.CompatibleBroadcast("BBB2.mp4")
E3.CompatibleBroadcast("BBB3.mp4")
E3.CompatibleBroadcast("BBB4.mpg")
