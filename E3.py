import numpy as np
import numpy as np
import os
import subprocess
import collections

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

    def CompatibleBroadcast(filename):
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
                Audio_codec.strip() in formats_dict[i]["a"]
                and Video_codec.strip() in formats_dict[i]["v"]
            ):
                # if yes save format in list
                compF.append(i)
        else:
            if not compF:
                print("There are no compatibles broadcast standards.")
                print("Please remember the broadcast standard and the codec accepted")
                for i in Bformats:
                    print("Format ", i, formats_dict[i])
                else:
                    print("The format of the file is \n", Audio_codec, Video_codec)

            else:
                separator = " "
                x = separator.join(compF)
                print("The compatibles broadcast standards are:{}".format(x))


CompatibleBroadcast("BBB_10.avi")
