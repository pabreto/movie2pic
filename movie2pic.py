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
interpolation_method = config_file.get("DEFAULT", "interpolation_method")
number_of_rows = int(config_file.get('DEFAULT', "number_of_rows"))
height_frame = int(config_file.get("DEFAULT", "height_frame"))
x_frame = config_file.get("DEFAULT", "x_frame")
x_final_pic = config_file.get("DEFAULT", "x_final_pic")


if pic_name == "":
    pic_name = str(Path(movie_name).stem + "-" + interpolation_method + "-" + str(number_of_rows))
    print("Picname not defined, will use movie name (", pic_name, ").")
else:
    print("Pic saved to", pic_name)

cam = cv2.VideoCapture(movie_name)
number_of_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

if x_frame == "":
    if x_final_pic == "":
        print("x_frame and x_final_pic can't be undefined at the same time, select at least one")
        sys.exit(0)
    x_final_pic = int(x_final_pic)
    x_frame = max(int(x_final_pic / number_of_frames), 1)
    x_final_pic = min (x_frame * number_of_frames, 1200)
else:
    x_frame = int(x_frame)
    if x_final_pic == "":
        print('x_frame0', x_frame)
        print('Number of frames0: ', number_of_frames)
        x_final_pic = int(x_frame) * int(number_of_frames)
        #Min taken for performance, 1200 can be adjusted.
    else:
        x_final_pic = int(x_final_pic)

if int(number_of_frames) <= x_final_pic:
    increment = 1
else:
    x_final_pic = max(x_final_pic, 1200)
    increment = max(int(number_of_frames / x_final_pic), 1)

# Read the video from specified path
currentframe = 0

fps_orig = round(cam.get(cv2.CAP_PROP_FPS))

if not os.path.isfile(movie_name):
    print("Movie " + movie_name + " doesn't exist")
else:
    print('Reading ', movie_name)
    print('Number of frames: ', number_of_frames)
    print('Increment: ', increment)
    print('height_frame', height_frame)
    print('x_frame', x_frame)
    print('x_final_pic', x_final_pic)

if not os.path.exists(outdir):
    os.makedirs(outdir)
print("Before Img creation")
final_pic = Image.new('RGB', (x_final_pic, height_frame), "black")
print("Img created")
for currentframe in progressbar(range(number_of_frames), "Creating image: ", 40):
    ret, frame = cam.read()
    if ret:
        if currentframe % increment == 0:
            #            cv2.imshow('frame' + str(currentframe), frame)
            #            cv2.waitKey()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#            print("preframe",frame.shape)
            if currentframe == 0:
                height_orig, x_orig = frame[:, :, 0].shape
                height_slice_orig = int(height_orig / number_of_rows)
                size_slice = int(x_orig * height_slice_orig)
                new_height = int(height_frame / number_of_rows)

                # find black columns from left and stop when not -> left_border
                left_border = 0
                top_border = 0
                while left_border < x_orig - 1:
                    if not np.array_equal(np.mean(frame[:, left_border, :], 0, int), [0, 0, 0]):
                        break
                    left_border += 1

                # find black columns from right and stop when not -> right_border
                right_border = x_orig - 1
                while right_border > left_border:
                    if not np.array_equal(np.mean(frame[:, right_border, :], 0, int), [0, 0, 0]):
                        break
                    right_border -= 1

                top_border = 0
                while top_border < height_orig - 1:
                    if not np.array_equal(np.mean(frame[top_border, :, :], 0, int), [0, 0, 0]):
                        break
                    top_border += 1

                bottom_border = height_orig - 1
                while bottom_border > top_border:
                    if not np.array_equal(np.mean(frame[bottom_border, :, :], 0, int), [0, 0, 0]):
                        break
                    bottom_border -= 1
            # redefine frame after cropping
                print("top_border,bottom_border,left_border,right_border",top_border,bottom_border,left_border,right_border)
            frame = frame[top_border:bottom_border, left_border:right_border, :]
            height_orig, x_orig = frame[:, :, 0].shape
            height_slice_orig = int(height_orig / number_of_rows)
            size_slice = int(x_orig * height_slice_orig)
            new_height = int(height_frame / number_of_rows)
            x1 = currentframe * x_frame
#            print("x1", x1)
#            print("current_frame",currentframe)
#            print("x_frame",x_frame)
#            print("new_height",new_height)
#            print("height_slice_orig",height_slice_orig)
            for h in range(0, number_of_rows):
#                print("shape", frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig), :, :].shape)
                subframe = frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig), :, :].reshape(size_slice,
                                                                                                            3)
                if interpolation_method == "max":
                    mostfrequent_color = Counter(map(tuple, subframe)).most_common()[0][0]
                elif interpolation_method == "average":
                    mostfrequent_color = tuple(np.mean(subframe, 0, int))
                tmpImage = Image.new('RGB', (x_frame, new_height), mostfrequent_color)
                y1 = h * new_height
                final_pic.paste(tmpImage, (x1, y1))
    currentframe += increment
print("Final pic created: " + pic_name + ".jpg")
final_pic.show()
final_pic.save(pic_name + ".jpg")

# Release all space and windows once done 
cam.release()
cv2.destroyAllWindows()
