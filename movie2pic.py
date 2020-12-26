#!/home/bscuser/moviecolor/venv/bin/python
# import time
import cv2
from PIL import Image
from configparser import ConfigParser
import os
import sys
from collections import Counter
from pathlib import Path
# import webcolors
import numpy as np


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        percent = int(int(j*100/count))
#        file.write("%s[%s%s] %i/%i (%f '%')\r" % (prefix, "o" * x, "." * (size - x), j, count, percent))
        file.write("%s[%s%s] %i/%i (%i)\r" % (prefix, "o" * x, "." * (size - x), j, count, percent))
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
# Flag to remove all black frames at beginning of movie

#for x_frame in ["30"]:
for x_frame in ["1", "5"]:
    for number_of_rows in [1, 2, 3]:
        for interpolation_method in ["average", "max", "interpolation"]:
            for movie_name in ["movies/Shrek.2001.720p.BluRay.x264.YIFY.mp4",
                   "movies/Finding.Nemo.2003.720p.BluRay.x264.YIFY.mp4",
                   "movies/Sin.City.EXTENDED.UNRATED.2005.1080p.BrRip.x264.YIFY+HI.mp4",
                   "movies/Avatar.ECE.2009.720p.BrRip.x264.bitloks.YIFY.mp4",
                   "movies/The.Darjeeling.Limited.2007.Criterion.1080p.BluRay.x264.DTS-SARTRE.mkv",
                   "movies/Minions.Yellow is the New Black.2019.1080p.Bluray.X264-EVO.mkv",
                   "movies/Minions20151080p10bitBlurayx265HEVCOrgBD5.1HindiDD5.1EnglishMSubsTombDoc.mkv",
                   "movies/[www.Cpasbien.me] Kirikou.et.Les.Hommes.et.Les.Femmes.2012.FRENCH.BDRip.XviD-Ulysse.avi",
                   "movies/Up.2009.720p.BluRay.x264.YIFY.mp4"]:
#            for movie_name in ['nemo.mp4', 'avatar.mp4', 'shrek.mp4']:
                all_black = True
                pic_name = ""
                if pic_name == "":
                    pic_name = str(Path(movie_name).stem + "-" + interpolation_method + "-" + str(number_of_rows) +
                                   "rows-" + str(x_frame) + "xframe")
                    print("Picname not defined, will use movie name")
                    print("Creating picture", pic_name)
                else:
                    print("Creating picture:", pic_name)
                if os.path.isfile(pic_name+".jpg"):
                    print("already there, skipping")
                else:
                    cam = cv2.VideoCapture(movie_name)
                    number_of_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
                    currentframe = 0

                    if not os.path.isfile(movie_name):
                        print("Movie " + movie_name + " doesn't exist")
                        sys.exit(0)
                    else:
                        print('Reading ', movie_name)
                        print('Number of frames: ', number_of_frames)
                        print('height_frame', height_frame)

                    if not os.path.exists(outdir):
                        os.makedirs(outdir)

                    for currentframe in progressbar(range(number_of_frames), "Creating image... ", 40):
                        ret, frame = cam.read()
                        if ret:
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            if float(cv2.countNonZero(gray)) < float((frame[:, :, 0]).size/100) and all_black:
    #                            print("Image" + str(currentframe) + " is black")
                                currentframe += 1
                                number_of_frames -= 1
                            else:
                                if all_black:
                                    print("First colored image ", str(currentframe))
                                    if x_frame == "":
                                        if x_final_pic == "":
                                            print("x_frame and x_final_pic can't be undefined at the same time, select at least one")
                                            sys.exit(0)
                                        x_final_pic = int(x_final_pic)
                                        x_frame = max(int(x_final_pic / number_of_frames), 1)
                                        x_final_pic = min(x_frame * number_of_frames, 1200)
#                                        print("defining xfinal_pic", x_final_pic)
                                    else:
                                        x_frame = int(x_frame)
                                        if x_final_pic == "":
     #                                       print('x_frame0', x_frame)
     #                                       print('Number of frames0: ', number_of_frames)
                                            x_final_pic = min(int(x_frame) * int(number_of_frames), 1200)
     #                                       print("defining xfinal_pic2", x_final_pic)
                                            # Min taken for performance, 1200 can be adjusted.
                                        else:
                                            x_final_pic = int(x_final_pic)
      #                                      print("defining xfinal_pic3", x_final_pic)

                                    if int(number_of_frames) <= x_final_pic:
                                        increment = 1
                                    else:
                                        x_final_pic = min(x_final_pic, 1200)
       #                                 print("defining xfinal_pic4", x_final_pic)
                                        increment = max(int(number_of_frames / x_final_pic), 1)
                                    print("Starting creation of final pic", pic_name)
         #                           print('Number of frames: ', number_of_frames)
                                    print('Increment: ', increment)
                                    print('height_frame', height_frame)
                                    print('x_frame', x_frame)
                                    print('x_final_pic', x_final_pic)
                                    final_pic = Image.new('RGB', (x_final_pic, height_frame), "black")
                                    #                print("Img created")
                    #                cv2.imshow('frame-' + str(currentframe), frame)
                    #                cv2.waitKey()
                                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                    #            print("preframe",frame.shape)
                                    #                if not all_black:
                                    height_orig, x_orig = frame[:, :, 0].shape
                                    height_slice_orig = int(height_orig / number_of_rows)
                                    size_slice = int(x_orig * height_slice_orig)
                                    new_height = int(height_frame / number_of_rows)

                                    # find black columns from left and stop when not -> left_border
                                    left_border = 0
                                    top_border = 0
                                    while left_border < x_orig - 1:
                    #                    if not np.array_equal(np.mean(frame[:, left_border, :], 0, int), [0, 0, 0]):
                                        if cv2.countNonZero(cv2.cvtColor(frame[:, left_border:left_border+1, :], cv2.COLOR_BGR2GRAY)) != 0:
                                            break
                                        left_border += 1
                                        # find black columns from right and stop when not -> right_border
                                    right_border = x_orig - 1
                                    while right_border > left_border:
                                        #if not np.array_equal(np.mean(frame[:, right_border, :], 0, int), [0, 0, 0]):
                                        if cv2.countNonZero(cv2.cvtColor(frame[:, right_border:right_border+1, :], cv2.COLOR_BGR2GRAY)) != 0:
                                            break
                                        right_border -= 1

                                    top_border = 0
                                    while top_border < height_orig - 1:
                                       # if not np.array_equal(np.mean(frame[top_border, :, :], 0, int), [0, 0, 0]):
                                       if cv2.countNonZero(cv2.cvtColor(frame[top_border:top_border+1, :, :], cv2.COLOR_BGR2GRAY)) != 0:
                                            break
                                       top_border += 1

                                    bottom_border = height_orig - 1
                                    while bottom_border > top_border:
                                        #if not np.array_equal(np.mean(frame[bottom_border, :, :], 0, int), [0, 0, 0]):
                                        if cv2.countNonZero(cv2.cvtColor(frame[bottom_border:bottom_border+1, :, :], cv2.COLOR_BGR2GRAY)) != 0:
                                            break
                                        bottom_border -= 1
                                        # redefine frame after cropping
                                    print("top_border,bottom_border,left_border,right_border", top_border, bottom_border, left_border,
                                          right_border)
                                    all_black = False
                                if currentframe % increment == 0:
                    #                cv2.imshow('frame-' + str(currentframe), frame)
                    #                cv2.waitKey()
                                    frame = frame[top_border:bottom_border, left_border:right_border, :]
                                    height_orig, x_orig = frame[:, :, 0].shape
                                    height_slice_orig = int(height_orig / number_of_rows)
                                    size_slice = int(x_orig * height_slice_orig)
                                    new_height = int(height_frame / number_of_rows)
                                    x1 = int(currentframe/increment) * x_frame
                    #                print("x1", x1)
                    #                print("current_frame", currentframe)
                    #                print("x_frame", x_frame)
                    #                print("new_height", new_height)
                    #                print("height_slice_orig", height_slice_orig)
                                    for h in range(0, number_of_rows):
                                        #                print("shape", frame[int(h * height_slice_orig):int((h + 1) * height_slice_orig), :, :].shape)

                                        subframe = frame[
                                                   int(h * height_slice_orig):int((h + 1) * height_slice_orig), :,
                                                   :]
                                        if interpolation_method == "interpolation":
                                            interp = cv2.resize(subframe,
                                                                (1, 1), cv2.INTER_AREA)
                                            tmpImage = Image.new('RGB', (x_frame, height_frame), tuple(interp[0, 0, :]))
                                            final_pic.paste(tmpImage, (
                                                currentframe * x_frame, int(h * height_frame / number_of_rows)))
                                        else:
                                            subframe = frame[
                                                       int(h * height_slice_orig):int((h + 1) * height_slice_orig), :,
                                                       :].reshape(
                                                size_slice,
                                                3)
                                            if interpolation_method == "max":
                                                mostfrequent_color = Counter(map(tuple, subframe.reshape(
                                                    size_slice, 3))).most_common()[0][0]
                                            elif interpolation_method == "average":
                                                mostfrequent_color = tuple(np.mean(subframe.reshape(
                                                    size_slice, 3), 0, int))
                                            tmpImage = Image.new('RGB', (x_frame, new_height), mostfrequent_color)
                                            y1 = h * new_height
                                            final_pic.paste(tmpImage, (x1, y1))
                                currentframe += increment
                    print("Final pic created: " + pic_name + ".jpg")
#                    final_pic.show()
                    final_pic.save(pic_name + ".jpg")

                    # Release all space and windows once done
                    cam.release()
                    cv2.destroyAllWindows()
