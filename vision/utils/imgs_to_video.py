#!/usr/bin/env python
"""
Convert a directory of images into a video file

Usage:

    ./imgs_to_video.py [path to media directory]
"""
from __future__ import division
import cv2
import sys
import os

path = ''


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]

    base_dir = os.getcwd()
    directory = os.path.join(base_dir, path)

    if not os.path.exists(directory):
        print "Invalid Path - Directory does not exist"
        exit()

    img_dirs = [
        image for image in os.listdir(directory) if os.path.splitext(image)[1][1:] in ['png', 'jpg', 'bmp']
    ]
    getNamefromIMG = lambda x: eval(x[0:-4])
    img_dirs.sort(key=getNamefromIMG)

    out = cv2.VideoWriter(os.path.basename(os.path.normpath(directory)) + '.avi',
                          cv2.cv.FOURCC('M', 'J', 'P', 'G'), 20.0, (640, 480))

    i = 0
    for image in img_dirs:
        if ((i%100)==0):
        	print("%2.f percent" % (i/len(img_dirs)*100))
        frame = cv2.imread(os.path.join(directory, image))
        out.write(frame)
        i+=1

    out.release()


if __name__ == '__main__':
    main()
