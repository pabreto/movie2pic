#!/home/bscuser/moviecolor/venv/bin/python

import glob
from configparser import ConfigParser

import cv2
import numpy as np
from PIL import Image

config_file = ConfigParser()
# config_file.read(str(sys.argv[1]))
config_file.read('options-generator.conf')

number_of_frames = int(config_file.get("DEFAULT", "number_of_frames"))
height = int(config_file.get("DEFAULT", "height"))
x_frame = int(config_file.get("DEFAULT", "x_frame"))
separation_vert = int(config_file.get("DEFAULT", "separation_vert"))
separation_horiz = int(config_file.get("DEFAULT", "separation_horiz"))
video_name = config_file.get("DEFAULT", "video_name")
c1p1 = config_file.get("DEFAULT", "c1p1")
c2p1 = config_file.get("DEFAULT", "c2p1")
c1p2 = config_file.get("DEFAULT", "c1p2")
c2p2 = config_file.get("DEFAULT", "c2p2")

final_pic = Image.new('RGB', (number_of_frames * x_frame, height), "pink")

red = [255, 0, 0]
white = [255, 255, 255]
blue = [51, 51, 255]
black = [51, 0, 0]
yellow = [255, 255, 0]
green = [0, 255, 0]
purple = [153, 0, 153]
orange = [255, 128, 0]
color2rgb = {
    "red": [255, 0, 0, 100, 100],
    "white": [255, 255, 255],
    "blue": [51, 51, 255],
    "black": [51, 0, 0],
    "yellow": [255, 255, 0],
    "green": [0, 255, 0],
    "purple": [153, 0, 153],
    "orange": [255, 128, 0]
}

# print(color2rgb["red"])
# print( np.array(c1p1))
# print(color2rgb(np.array(c1p1)))
# color=np.array([ [ color2rgb(np.array(c1p1)),\
#        np.array(c2p1)],\
#        [ np.array(c1p2),\
#        np.array(c2p2)]])
# color=np.array([ [ np.array(c1p1),\
#        np.array(c2p1)],\
#        [ np.array(c1p2),\
#        np.array(c2p2)]])
# print("shape",color.shape)
color = np.array([[[red, red, blue, black],
                   [red, green, black, blue]],
                  [[yellow, green, purple, orange],
                   [red, white, blue, black]]])
color = np.array([[[red, red, red, red],
                   [red, red, red, red]],
                  [[green, green, green, green],
                   [green, green, green, blue]]])

for currentframe in range(0, number_of_frames):
    final_pic = Image.new('RGB', (number_of_frames * x_frame, height), "red")
    for horiz in range(0, separation_horiz):
        for vertic in range(0, separation_vert):
            x1 = horiz * x_frame
            y1 = vertic * int((height / separation_vert))
            x2 = (horiz + 1) * x_frame
            y2 = (vertic + 1) * int((height / separation_vert))
            #print(y2-y1+1)
            final_pic.paste(tuple(color[currentframe, horiz, vertic, :]), (x1, y1, x2, y2))
    final_pic.show()
    print(final_pic.mode)
    currentframe += 1
    final_pic.save("image_h" + str(currentframe) + ".jpg")

img_array = []
for filename in glob.glob('*.jpg'):
    img = cv2.imread(filename)
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
