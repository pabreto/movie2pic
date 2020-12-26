#!/home/bscuser/moviecolor/venv/bin/python

import cv2
from PIL import Image
from configparser import ConfigParser
import os
import sys
from collections import Counter
from pathlib import Path
# import webcolors
import numpy as np

movie_name = "nemo.mp4"
movie_name = "movies/test_movie-uni2.mp4"
number_of_rows = 2
height_frame = 200
x_frame = 20
cam = cv2.VideoCapture(movie_name)
number_of_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
print('number_of_frames',number_of_frames)
final_pic = Image.new('RGB', (int(number_of_frames*x_frame), height_frame), "black")
for currentframe in range(number_of_frames):
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #    cv2.imshow("original", frame)
#    cv2.waitKey(0)
    tmp = movie_name+str(currentframe)
#    for h in range(0,2):
    for h in range(0, number_of_rows):
        print("shape", (frame.shape[1], frame.shape[0]))
        print("frame",type(frame))
        print("tmp",type(tmp))
        print("inter",cv2.INTER_AREA)
        print("shape2",frame[int(frame.shape[0] / number_of_rows)
                                                    * h:int(frame.shape[0] / number_of_rows) * (h + 1), :, :].shape)
        cv2.imshow("original", frame[int(frame.shape[0] / number_of_rows)
                                                    * h:int(frame.shape[0] / number_of_rows) * (h + 1), :, :])
        cv2.waitKey(0)
        subframe = frame[int(frame.shape[0] / number_of_rows)
                                                    * h:int(frame.shape[0] / number_of_rows) * (h + 1), :, :]
#        tmpImage2 = Image.new('RGB', (x_frame, height_frame), tuple(frame[int(frame.shape[0] / number_of_rows)
#                                                    * h:int(frame.shape[0] / number_of_rows) * (h + 1), :, :]))
#        tmpImage2.show()
#        interp = cv2.resize(frame[int(frame.shape[0]/number_of_rows)*h:int(frame.shape[0]/number_of_rows)*(h+1),:,:],
#                            (1, 2), cv2.INTER_AREA)
#        interp = cv2.resize(frame[:,frame.shape[1]*h:frame.shape[1]*(h+1),:], (2, 1), cv2.INTER_AREA)
        interp = cv2.resize(subframe,
                            (1, 1), cv2.INTER_AREA)
#        interp = cv2.resize(frame[:,frame.shape[1]*h:frame.shape[1]*(h+1),:], (2, 1), cv2.INTER_AREA)

        print(interp.shape)
#        tmpImage = Image.new('RGB', (x_frame, height_frame), tuple(interp[h,0,:]))
        tmpImage = Image.new('RGB', (x_frame, height_frame), tuple(interp[0, 0, :]))
#    tmpImage = Image.new('RGB', (20, 200), tuple(cv2.resize(frame, (1,2), cv2.INTER_AREA)[0][0]))
        final_pic.paste(tmpImage, (currentframe*x_frame, int(h*height_frame/number_of_rows)))
    final_pic.show()
#cv2.imshow("Resized image", final_pic)
#cv2.waitKey(0)
cv2.destroyAllWindows()