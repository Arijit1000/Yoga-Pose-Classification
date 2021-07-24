import sys
import os
from urllib.parse import parse_qs, urlparse

file = open(sys.argv[1], "r")

current_pose = ""
current_link = ""
counter = 0
for line in  file.readlines():
  line = line.strip()
  #print(line)
  if line == "":
    continue
  elif line.startswith("http"):
    current_link = line.replace(" ","")
    vid_tag = parse_qs(urlparse(current_link).query)['v']
    current_link = "http://www.youtube.com/watch?v={}".format(vid_tag[0])
  elif line[0].isdigit():
    start_min, start_sec, end_min, end_sec = line.replace(" ","").replace(":","-").split("-")
    start_seconds = int(start_min) * 60 + int(start_sec)
    end_seconds = int(end_min) * 60 + int(end_sec)

    #Print out youtube-dl command (next lines shows an example)
    #youtube-dl https://www.youtube.com/watch?v=1oumWGKg2mE&t=35s
    #cvlc "./John Schumacher Teaches Virabhadrasana I-1oumWGKg2mE.webm" --video-filter=scene --vout=dummy --start-time=156 --stop-time=158 --scene-ratio=1 --scene-prefix=B --scene-path="." vlc://quit

    print("mkdir -p {}".format(current_pose))
    print("cd {}".format(current_pose))
    #vid_tag = parse_qs(urlparse(current_link).query)['v']
    counter = counter +1
    vid_tag = str(counter) + ".vid"
    print("youtube-dl {} -o {}".format(current_link, vid_tag))
    #print("cvlc \"{}\" --video-filter=scene --vout=dummy --start-time={} --stop-time={} --scene-ratio=1 --rate=10 --scene-prefix={} --scene-path=\".\" vlc://quit".format(vid_tag, start_seconds, end_seconds, counter))
    print("ffmpeg -i {} -ss {} -to {} -vf fps=10 {}_%d.png".format(vid_tag, start_seconds, end_seconds, counter))
    print("cd ..")
    print("echo done processing {}".format(vid_tag))
    print()
  else:
    current_pose = line.replace(" ","_").capitalize()
    #os.mkdir(current_pose)
