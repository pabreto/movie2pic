#!/home/bscuser/moviecolor/venv/bin/python

import glob
from configparser import ConfigParser

import cv2
import numpy as np
import os
import webcolors
from PIL import Image


config_file = ConfigParser()
# config_file.read(str(sys.argv[1]))
config_file.read('options-generator.conf')

number_of_frames = int(config_file.get("DEFAULT", "number_of_frames"))
height_frame = int(config_file.get("DEFAULT", "height_frame"))
x_frame = int(config_file.get("DEFAULT", "x_frame"))
number_of_rows = int(config_file.get("DEFAULT", "number_of_rows"))
number_of_columns = int(config_file.get("DEFAULT", "number_of_columns"))
video_name = config_file.get("DEFAULT", "video_name")
c1p1 = config_file.get("DEFAULT", "c1p1")
c2p1 = config_file.get("DEFAULT", "c2p1")
c1p2 = config_file.get("DEFAULT", "c1p2")
c2p2 = config_file.get("DEFAULT", "c2p2")


red = [255, 0, 0]
white = [255, 255, 255]
blue = [51, 51, 255]
black = [51, 0, 0]
yellow = [255, 255, 0]
green = [0, 255, 0]
purple = [153, 0, 153]
orange = [255, 128, 0]

color = np.array([[[red, purple],
                   [blue, black],
                   [red, green],
                   [black, blue]],
                  [[yellow, green],
                   [purple, orange],
                   [red, green],
                   [blue, black]]])
color = np.array([[[red, red],
                   [red, black],
                   [red, red],
                   [black, red]],
                  [[purple, purple],
                   [purple, green],
                   [green, green],
                   [blue, green]]])


for currentframe in range(0, number_of_frames):
    final_pic = Image.new('RGB', (x_frame,height_frame), tuple(white))
    for row in range(0, number_of_rows):
        for column in range(0, number_of_columns):
            y1 = row * int((height_frame / number_of_rows))
            x1 = column * int(x_frame/number_of_columns)
#            y2 = (row + 1) * int((x_frame / number_of_columns))
#            x2 = (column + 1) * int(height_frame/number_of_rows)
#            print(y2-y1+1)
#            final_pic.paste(tuple(color[currentframe, horiz, vertic, :]), (x1, y1, x2, y2))
            tmpImage = Image.new('RGB', (int(x_frame / number_of_columns),int(height_frame/number_of_rows)),  tuple(color[currentframe, row, column, :]))
            final_pic.paste(tmpImage, (x1, y1))

    final_pic.show()
    print(final_pic.mode)
    currentframe += 1
    final_pic.save("image_h" + str(currentframe) + ".jpg")

img_array = []
for filename in sorted(glob.glob('image_h*.jpg')):
#for filename in sorted(glob.glob('*.jpg')):
#for filename in os.listdir('*.jpg'):
    img = cv2.imread(filename)
    print(filename)
    print(img.shape)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = 0x7634706d
print(video_name)
out = cv2.VideoWriter(video_name, fourcc, 1, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
