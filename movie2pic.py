#!/home/bscuser/moviecolor/venv/bin/python
import time
import cv2
from PIL import Image
from configparser import ConfigParser
import os
import sys
from collections import Counter
from pathlib import Path
import webcolors
import numpy as np


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count))
        file.flush()

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()


config_file: ConfigParser = ConfigParser()

# config_file.read(str(sys.argv[1]))
config_file.read("options-m2p.conf")

movie_name = config_file.get("DEFAULT", "movie_name")
outdir = config_file.get("DEFAULT", "outdir")
pic_name = config_file.get("DEFAULT", "picname")
number_of_rows = int(config_file.get('DEFAULT', "number_of_rows"))
height_frame = int(config_file.get("DEFAULT", "height_frame"))
x_frame = int(config_file.get("DEFAULT", "x_frame"))

# print("picname",pic_name)
if pic_name == "":
    pic_name = Path(movie_name).stem
    print("Picname not defined, will use movie name (", pic_name, ").")
else:
    print("picname defined", pic_name)


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

final_pic = Image.new('RGB', (number_of_frames * x_frame, height_frame), "black")
for currentframe in progressbar(range(number_of_frames), "Creating image: ", 40):
    ret, frame = cam.read()
    if ret:
        #        cv2.imshow('frame' + str(currentframe), frame)
        #        cv2.waitKey()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if currentframe == 0:
            height_orig, x_orig = frame[:, :, 0].shape
            height_slice_orig = int(height_orig / number_of_rows)
            size_slice = int(x_orig * height_slice_orig)
            new_height = int(height_frame / number_of_rows)
            #print("shape", frame[:, :, :].shape)
            #print("shape2", np.zeros((height_orig, 3)).shape)

            # find black columns from left and stop when not -> left_border
            left_border = 0
            top_border = 0
            while left_border < x_orig:
                if not np.array_equal(np.mean(frame[:, left_border, :], 0, int), [0, 0, 0]):
                    break
                left_border += 1
            #print("left_border", left_border)

            # find black columns from right and stop when not -> right_border
            right_border = x_orig - 1
            #print("x_orig", x_orig)
            while right_border > left_border:
                if not np.array_equal(np.mean(frame[:, right_border, :], 0, int), [0, 0, 0]):
                    break
                right_border -= 1
            #print("right_border", right_border)

            top_border = 0
            while top_border < height_orig:
                if not np.array_equal(np.mean(frame[top_border, :, :], 0, int), [0, 0, 0]):
                    break
                top_border += 1
            #print("top_border", top_border)

            bottom_border = height_orig - 1
            while bottom_border > top_border:
                if not np.array_equal(np.mean(frame[bottom_border, :, :], 0, int), [0, 0, 0]):
                    break
                bottom_border -= 1
            #print("bottom_border", bottom_border)
        # redefine frame after cropping
        frame = frame[top_border:bottom_border, left_border:right_border, :]
        height_orig, x_orig = frame[:, :, 0].shape
        height_slice_orig = int(height_orig / number_of_rows)
        size_slice = int(x_orig * height_slice_orig)
        new_height = int(height_frame / number_of_rows)
        #        cv2.imshow('crop' + str(currentframe), frame)
        #        cv2.waitKey()
        x1 = currentframe * x_frame
        #        print('x_orig', x_orig)
        #        print('height_orig', height_orig)
        #        print(frame[0,0,0])
        #        print(webcolors.rgb_to_name((0, 0, 0)))
        #        print("newframe",newframe)
        #        print("frame",frame)
        #        print('number_of_rows', number_of_rows)
        for h in range(0, number_of_rows):
            subframe = frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig), :, :].reshape(size_slice, 3)
            mostfrequent_color = Counter(map(tuple, subframe)).most_common()[0][0]
            tmpImage = Image.new('RGB', (x_frame, new_height), mostfrequent_color)
            y1 = h * new_height
            final_pic.paste(tmpImage, (x1, y1))
            currentframe += 1
            #            print('height_slice_orig', height_slice_orig)
            #            print('size_slice', size_slice)
            #            print('shape.frame', frame.shape)
            #            print('shape.subframe', subframe.shape)
            #            print(size_slice*3)
            #            subframe = frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig), :, :]
            #          print('shape.subframe',subframe.shape)
            #           cv2.imshow('subframe' + str(currentframe) + "_h" +str(h), subframe)
            #           mostfrequent_color = Counter(subframe).most_common()[0][0]
            #            print('Counter',Counter(map(tuple, subframe_reshaped)).most_common()[0])
            #           print('Counter',len(Counter(map(tuple, subframe_reshaped)).most_common()))
            # mostfrequent_color = Counter(map(tuple, subframe_reshaped[h:int((h + 1) * height_slice_orig)])).most_common()[0][0]
            #            print('mostfrequent_color',tuple(mostfrequent_color))
            #            print('new_height', new_height)
            #           tmpImage.show()
            #            cv2.imshow('mostfrequent_color', tmpImage)
            #            cv2.waitKey()
            #            print('subframe', subframe)
            #            print('mostfrequent_color', tuple(mostfrequent_color))
            #            x2 = (currentframe + 1) * x_frame
            #            y2 = (h + 1) * new_height
        #            cv2.waitKey()
#    cv2.imshow("final",final_pic)    #
#    final_pic.show()
#    cv2.waitKey()
print("Final pic created: " + pic_name + ".jpg")
final_pic.show()
final_pic.save(pic_name + ".jpg")

# writing the extracted images
# increasing counter so that it will 
# show how many frames are created 

# Release all space and windows once done 
cam.release()
cv2.destroyAllWindows()
