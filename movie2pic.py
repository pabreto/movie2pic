#!/home/bscuser/moviecolor/venv/bin/python
import time
import cv2
from PIL import Image
from configparser import ConfigParser
import os
import numpy as np

config_file: ConfigParser = ConfigParser()

# config_file.read(str(sys.argv[1]))
config_file.read("options-m2p.conf")

movie_name = config_file.get("DEFAULT", "movie_name")
outdir = config_file.get("DEFAULT", "outdir")
pic_name = config_file.get("DEFAULT", "picname")
separations = int(config_file.get('DEFAULT', "separations"))
height = int(config_file.get("DEFAULT", "height"))
x_frame = int(config_file.get("DEFAULT", "x_frame"))

# Read the video from specified path
currentframe = 0

# create empty final black pic with 4 horizontal pixels per frame, height defined in config file
cam = cv2.VideoCapture(movie_name)
number_of_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
print(number_of_frames)
print(movie_name)
if os.path.isfile(movie_name):
    print('ok')
else:
    print('no')
if not os.path.exists(outdir):
    os.makedirs(outdir)

final_pic = Image.new('RGB', (number_of_frames * x_frame, height), "black")
while currentframe < number_of_frames:
    ret, frame = cam.read()
    if ret:
        print(frame.shape)
        for i in range(0, 4):
            print("i", frame[i, 0, 0])
        cv2.imshow('frame', frame)
        cv2.waitKey(0)


        tmppicname = os.path.join(outdir, pic_name + "_" + str(currentframe) + '.jpg')
        print('Creating...' + tmppicname)
        #        frame =
        #        color = # array ( (RGB), separations)
        #        for i in range(0,separations):
        #            final_pic.paste(color[i],(currentframe*x_frame,i*height,(currentframe+1)*x_frame,(i+1)*height))
        #            final_pic.show()
        currentframe += 1

# writing the extracted images
# increasing counter so that it will 
# show how many frames are created 

# Release all space and windows once done 
cam.release()
cv2.destroyAllWindows()
