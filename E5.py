import numpy as np
import os
import subprocess
import collections
import E3

Bformats = ["DVB", "ATSC", "ISBD-T", "DTMB"]
formats_dict = collections.OrderedDict.fromkeys(Bformats, 0)
for i in Bformats:
    formats_dict[i] = {"v": ["h264", "mpeg2video"], "a": ""}
else:
    formats_dict["DVB"]["a"] = ["aac", "mp3", "ac3"]
    formats_dict["ATSC"]["a"] = "ac3"
    formats_dict["ISBD-T"]["a"] = "aac"
    formats_dict["DTMB"]["a"] = ["dra", "aac", "ac3", "mp2", "mp3"]
    formats_dict["DTMB"]["v"].append("avs")
    formats_dict["DTMB"]["v"].append("avs+")


class Containers:
    def __init__(self, formats):
        self.formats_dict = formats

    def CompatibleBroadcast(self, filename):
        """
        Tells you the compatibility with the broadcast standards
        filename:name of the fil you want to check
        """
        # extract audio and video codecs
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "csv=s=x:p=0",
            filename,
        ]
        Video_codec = (
            subprocess.Popen(cmd, stdout=(subprocess.PIPE))
            .communicate()[0]
            .decode("utf-8")
        )
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "csv=s=x:p=0",
            filename,
        ]
        Audio_codec = (
            subprocess.Popen(cmd, stdout=(subprocess.PIPE))
            .communicate()[0]
            .decode("utf-8")
        )
        compF = []
        for i in Bformats:
            # check if codec of audio and video compatible with any format
            if (
                Audio_codec.strip() in self.formats_dict[i]["a"]
                and Video_codec.strip() in self.formats_dict[i]["v"]
            ):
                # if yes save format in list
                compF.append(i)
        else:
            if not compF:
                print("There are no compatibles broadcast standards.")
                print("Please remember the broadcast standard and the codec accepted")
                for i in Bformats:
                    print("Format ", i, self.formats_dict[i])
                else:
                    print("The format of the file is \n", Audio_codec, Video_codec)

            else:
                separator = " "
                x = separator.join(compF)
                print("The compatibles broadcast standards are:{}".format(x))

    def MP4(self, video, audio, subtitles, output):
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

    def createFiles(self):
        # create different files to check formats
        os.system("ffmpeg -i BBB_10.avi -c:v mpeg2video BBB1.mpg")
        os.system("ffmpeg -i BBB_10.avi -c:v h264 -c:a aac BBB2.mp4")
        os.system("ffmpeg -i BBB_10.avi -c:v h264 -c:a ac3 BBB3.mp4")
        os.system("ffmpeg -i BBB_10.avi -c:v mpeg2video -c:a mp3 BBB4.mpg")

    def testFiles(self):
        # check broadcast standard compatibility
        E3.CompatibleBroadcast("BBB1.mpg")
        E3.CompatibleBroadcast("BBB2.mp4")
        E3.CompatibleBroadcast("BBB3.mp4")
        E3.CompatibleBroadcast("BBB4.mpg")


# test
#cont = Containers(formats_dict)
#cont.createFiles()
#cont.testFiles()
