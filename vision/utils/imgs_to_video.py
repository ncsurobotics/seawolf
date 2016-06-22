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
import argparse

path = ''

def setup_parser():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("path",
                        type=str, help="location of the directory containing img files")

    parser.add_argument("-s", "--slice",
                        help="Specify the beggining, and (optionally) end img",
                        type=int, dest="slice", default=[], nargs='+', action="append",
                        metavar="idx")

    return parser

def get_imgs(dir, slices=None):
    # collect slices
    if len(slices)==2:
        start = slices[0]
        end = slices[1]
    elif len(slices)==1:
        start = slices[0]
        end = -1
    elif slices is None:
        start = 0
        end = -1
    else:
        raise InputError("maximum length of slices argument is 2.")

    # other variables
    exti = 1
    namei = 0

    # get a list of all image files in the directory
    imgs = []
    for file in os.listdir(dir):
        [name,ext] = os.path.splitext(file)

        

        if (ext in ['.png', '.jpg', '.bmp']):
            imgs.append(file)

    # sort the list in numerical order
    
    getNamefromIMG = lambda x: eval( os.path.splitext(x)[namei] )
    imgs.sort(key=getNamefromIMG) # performs the sort
    

    # remove frames outside specified slice
    i = 0
    done = False
    while(not done):
        imgnum = eval( os.path.splitext(imgs[i])[namei] )
        if imgnum >= start:
            imgs = imgs[i:] # slice off the first portion
            done = True
        else:
            i += 1

    # now slice off the second portion
    i = len(imgs)-1
    done = False
    
    # if no end position is specified, we're done
    if end < 0:
        return imgs

    while(not done):
        imgnum = eval( os.path.splitext(imgs[i])[namei] )
        if imgnum <= end:
            imgs = imgs[:i]
            done = True
        else:
            i -= 1

        if i < 0:
            break


    # return
    return imgs


    
    

def main():
    parser = setup_parser()
    args = parser.parse_args()

    # assign args
    path = args.path
    slice_points = args.slice[0] 

    # get full directory path
    base_dir = os.getcwd()
    directory = os.path.join(base_dir, path)
    if not os.path.exists(directory):
        print "Invalid Path - Directory does not exist"
        exit()

    img_dirs = get_imgs(directory, slice_points)
    
    
    
    # print how many frames are going to be processed
    if slice_points==2:
            (a,b) = slice_points
            print("Writing frames %d through %d to file" % (a,b))
    else:
        print("Writing %d frames to the file" % len(img_dirs))

    # generate video writer
    out = cv2.VideoWriter(os.path.basename(os.path.normpath(directory)) + '.avi',
                          cv2.cv.FOURCC('M', 'J', 'P', 'G'), 30.0, (640, 480))

    for (n,image) in enumerate(img_dirs):
        if ((n%100)==0):
        	print("%2.f percent" % (n/len(img_dirs)*100))
        frame = cv2.imread(os.path.join(directory, image))
        out.write(frame)

    out.release()


if __name__ == '__main__':
    main()
