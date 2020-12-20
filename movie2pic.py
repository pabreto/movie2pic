#!/home/bscuser/moviecolor/venv/bin/python
import time
import cv2
from PIL import Image
from configparser import ConfigParser
import os
from collections import Counter
import webcolors
import numpy as np

config_file: ConfigParser = ConfigParser()

# config_file.read(str(sys.argv[1]))
config_file.read("options-m2p.conf")

movie_name = config_file.get("DEFAULT", "movie_name")
outdir = config_file.get("DEFAULT", "outdir")
pic_name = config_file.get("DEFAULT", "picname")
number_of_rows = int(config_file.get('DEFAULT', "number_of_rows"))
height_frame = int(config_file.get("DEFAULT", "height_frame"))
x_frame = int(config_file.get("DEFAULT", "x_frame"))

# Read the video from specified path
currentframe = 0

# create empty final black pic with 4 horizontal pixels per frame, height defined in config file
cam = cv2.VideoCapture(movie_name)
number_of_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

if not os.path.isfile(movie_name):
    print("Movie " + movie_name + " doesn't exist")
else:
    print('Reading ', movie_name)
    print('Number of frames: ', number_of_frames)

if not os.path.exists(outdir):
    os.makedirs(outdir)

# A = np.array(
#  [[ 2.,  1.],
#   [ 1.,  1.]]
# )

# c = Counter(map(tuple, A)).most_common()[0][0]
# print("c",c)
final_pic = Image.new('RGB', (number_of_frames * x_frame,height_frame), "black")
while currentframe < number_of_frames:
    print("-------")
    ret, frame = cam.read()
    if ret:
        # print(frame.shape)
        cv2.imshow('frame' + str(currentframe), frame)
        cv2.waitKey()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        x_orig = frame[0, :, 0].size
        height_orig = frame[:, 0, 0].size
        print('x_orig', x_orig)
        print('height_orig', height_orig)
        #        print(frame[0,0,0])
#        print(webcolors.rgb_to_name((0, 0, 0)))
        #        print("newframe",newframe)
        #        print("frame",frame)
        print('number_of_rows', number_of_rows)
        for h in range(0, number_of_rows):
            height_slice_orig = int(height_orig / number_of_rows)
            size_slice = int(x_orig * height_slice_orig)
            print('height_slice_orig', height_slice_orig)
            print('size_slice', size_slice)
            subframe = frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig),:, :]
            print('shape.frame', frame.shape)
            print('shape.subframe', subframe.shape)
#            print(size_slice*3)
#            subframe = frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig), :, :]
  #          print('shape.subframe',subframe.shape)
 #           cv2.imshow('subframe' + str(currentframe) + "_h" +str(h), subframe)
            subframe_reshaped = subframe.reshape(size_slice, 3)
 #           mostfrequent_color = Counter(subframe).most_common()[0][0]
            print('Counter',Counter(map(tuple, subframe_reshaped)).most_common()[0])
            print('Counter',len(Counter(map(tuple, subframe_reshaped)).most_common()))
            mostfrequent_color = Counter(map(tuple, subframe_reshaped)).most_common()[0][0]
            #mostfrequent_color = Counter(map(tuple, subframe_reshaped[h:int((h + 1) * height_slice_orig)])).most_common()[0][0]
            print('mostfrequent_color',tuple(mostfrequent_color))
            new_height = int(height_frame / number_of_rows)
            print('new_height', new_height)
            tmpImage = Image.new('RGB', (x_frame,new_height), mostfrequent_color)
 #           tmpImage.show()
#            cv2.imshow('mostfrequent_color', tmpImage)
#            cv2.waitKey()
#            print('subframe', subframe)
#            print('mostfrequent_color', tuple(mostfrequent_color))
            x1 = currentframe * x_frame
            y1 = h * new_height
#            x2 = (currentframe + 1) * x_frame
#            y2 = (h + 1) * new_height
            final_pic.paste(tmpImage, (x1, y1))
#            cv2.waitKey()
        currentframe += 1
#    cv2.imshow("final",final_pic)    #
    final_pic.show()
    cv2.waitKey()
final_pic.save(pic_name + ".jpg")
# writing the extracted images
# increasing counter so that it will 
# show how many frames are created 

# Release all space and windows once done 
cam.release()
cv2.destroyAllWindows()
