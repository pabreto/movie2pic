#!/bin/python

import os
import sys
from configparser import ConfigParser
import cv2 
from PIL import Image

config_file = ConfigParser()

config_file.read(str(sys.argv[1]))

movie_name = config_file.get("DEFAULT", "movie_name")
outdir = config_file.get("DEFAULT", "outdir")
pic_name = config_file.get("DEFAULT", "picname")
separation = config_file.get("DEFAULT", "separation")
height = config_file.get("DEFAULT", "height")
x_frame = config_file.get("DEFAULT", "x_frame")


# Read the video from specified path
cam = cv2.VideoCapture(movie_name)
currentframe = 0
number_of_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

final_pic = Image.new('RGB',(number_of_frames*x_frame,height),"black")
#create empty final black pic with 4 horizontal pixels per frame, height defined in config file
while(True): 
    ret,frame = cam.read()
    if ret: 
# frame 
        # if video is still left continue creating images 
#        tmppicname = os.path.join(outdir,picname+"_"+str(currentframe) + '.jpg')
#        print ('Creating...' + tmppicname) 
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        frame =
        color = # array ( (RGB), separation)
        for i in range(0,separation):
            final_pic.paste(color[i],(currentframe*x_frame,i*height,(currentframe+1)*x_frame,(i+1)*height))
            final_pic.show()
        # writing the extracted images 
        # increasing counter so that it will 
        # show how many frames are created 
        currentframe += 1
    else: 
        break
  
# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 

