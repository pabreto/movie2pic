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
separations = int(config_file.get('DEFAULT', "separations"))
height = int(config_file.get("DEFAULT", "height"))
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
final_pic = Image.new('RGB', (number_of_frames * x_frame, height), "black")
while currentframe < number_of_frames:
    ret, frame = cam.read()
    if ret:
        # print(frame.shape)
        x_orig = frame[:, 0, 0].size
        h_orig = frame[0, :, 0].size
        print('x_orig', x_orig)
        print('h_orig', h_orig)
        #        print(frame[0,0,0])
        #        print(webcolors.rgb_to_name((0, 0, 0), spec='css3'))
        #        print(webcolors.rgb_to_name(list(frame[0,0,0]),spec='css3'))
        #        for i in range(0, 3):
        #            print("i", frame[0, :, i])
        cv2.imshow('frame' + str(currentframe), frame)
        cv2.waitKey()
        #        print("newframe",newframe)
        #        print("frame",frame)
        print('separations', separations)
        for h in range(0, separations):
            new_height = int(height / separations)
            slice_hsize = int(h_orig / separations)
            slice_size = int(x_orig * slice_hsize)
            print('height', height)
            print('new_height', new_height)
            print('slice_hsize', slice_hsize)
            print('slice_size', slice_size)
            cv2.imshow('subframe' + str(currentframe), frame[:, int(h * slice_hsize):int((h + 1) * slice_hsize), :])
            subframe = frame[:, int(h * slice_hsize):int((h + 1) * slice_hsize), :].reshape(slice_size, 3)
            mostfrequent_color = Counter(map(tuple, subframe[h:int((h + 1) * slice_hsize)])).most_common()[0][0]
            print('subframe', subframe)
            print('mostfrequent_color', mostfrequent_color)
            x1 = currentframe * x_frame
            y1 = h * new_height
            x2 = (currentframe + 1) * x_frame
            y2 = (h + 1) * new_height
            final_pic.paste(mostfrequent_color,
                            (x1, y1, x2, y2))

            # tmppic = Image.new('RGB', (x_frame, new_height), mostfrequent_color)
            cv2.waitKey()
        currentframe += 1
        final_pic.show()
final_pic.save(pic_name + ".jpg")
# writing the extracted images
# increasing counter so that it will 
# show how many frames are created 

# Release all space and windows once done 
cam.release()
cv2.destroyAllWindows()
