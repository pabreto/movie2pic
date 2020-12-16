#!/bin/python

import os
import sys
from configparser import ConfigParser
import cv2 
from PIL import Image
import numpy as np
import glob

number_of_frames = 2
x_frame = 50
height = 160
separation_vert = 4
separation_horiz = 2

video_name = "movies/test_movie.mp4" 
final_pic = Image.new('RGB',(number_of_frames*x_frame,height),"pink")
#color=np.array([ [ [255,0,0],[255,255,255],[51,51,255],[51,0,0] ],\
#        [ [255,255,0],[0,153,256],[153,0,153],[255,128,0] ],\
#        [ [255,255,0],[0,153,256],[153,0,153],[255,128,0] ],\
#        [ [255,0,0],[255,255,255],[51,51,255],[51,0,0] ]])
#color=np.array([ [ [ [255,0,0],[255,255,255],[51,51,255],[51,0,0] ],\
#        [ [255,255,0],[0,255,0],[153,0,153],[255,128,0] ],\
#        [ [255,255,0],[0,255,0],[153,0,153],[255,128,0] ],\
#        [ [255,0,0],[255,255,255],[51,51,255],[51,0,0] ]], \
#
#        [ [ [255,255,0],[0,255,0],[153,0,153],[255,128,0] ],\
#        [ [255,0,0],[255,255,255],[51,51,255],[51,0,0] ],\
#        [ [255,0,0],[255,255,255],[51,51,255],[51,0,0] ],\
#        [ [255,255,0],[0,255,0],[153,0,153],[255,128,0] ]]])
red = [255,0,0]
white = [255,255,255]
blue = [51,51,255]
black = [51,0,0]
yellow = [255,255,0]
green = [0,255,0]
purple = [153,0,153]
orange = [255,128,0]
color=np.array([ [ [ red, white, blue, black ],\
        [ yellow, green, purple, orange ],\
        [ yellow, green, purple, orange ],\
        [ red, white, blue, black ]], \

        [ [ yellow, green, purple, orange ],\
        [ red, white, blue, black ],\
        [ red, white, blue, black ],\
        [ yellow, green, purple, orange ]]])
#First pic
# red white blue black 1-1
# yellow green purple orange 1-2
# yellow green purple orange 2-1
# red white blue black 2-2

#Second pic
# yellow green purple orange 1-1
# red white blue black 1-2
# red white blue black 2-1
# yellow green purple orange 2-2

for currentframe in range(0,number_of_frames):
    final_pic = Image.new('RGB',(number_of_frames*x_frame,height),"pink")
    print("currentframe",currentframe)
    for horiz in range(0,separation_horiz):
        print("horiz",horiz)
        for vertic in range(0,separation_vert):
            x1=horiz*x_frame
            y1=vertic*int((height/separation_vert))
            x2=(horiz+1)*x_frame-1
            y2=(vertic+1)*int((height/separation_vert))-1
            print("vertic",vertic)
            print("color",tuple(color[currentframe,horiz,vertic,:]))
            print("x1",x1)
            print("y1",y1)
            print("x2",x2)
            print("y2",y2)
            final_pic.paste(tuple(color[currentframe,horiz,vertic,:]),(x1,y1,x2,y2))
    final_pic.show()
    currentframe += 1
    final_pic.save("image_h"+str(currentframe)+".jpg")


img_array = []
for filename in glob.glob('*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = 0x7634706d
out = cv2.VideoWriter(video_name,fourcc, 1, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
