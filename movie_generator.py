#!/bin/python

import os
import sys
from configparser import ConfigParser
import cv2 
from PIL import Image

number_of_frames = 2
x_frame = 5
height = 16
separation_vert = 4
separation_horiz = 2

video_name = 
final_pic = Image.new('RGB',(number_of_frames*x_frame,height),"black")
color=np.array([[[256,256,0],[256,0,0],[0,256,256],[256,0,256]],\
               [[256,0,256],[0,256,256],[256,0,0],[256,256,0]]],\
               [[[0,0,0],[256,256,256],[0,0,0],[256,256,256]],\
               [[256,256,256],[0,0,0],[256,256,256],[0,0,0]]])


for currentframe in range(0,number_of_frames):
    for horiz in range(0,separation_horiz):
        for i in range(0,separation_vert):
            final_pic.paste(color[i,horiz],(currentframe*x_frame,i*height,(currentframe+1)*x_frame,(i+1)*height))
            final_pic.show()
            currentframe += 1
    final_pic.save("image_h"+str(currentframe)+".jpg")


