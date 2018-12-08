#!/usr/bin/python
#
#   clamp the width (and height preserving aspect ratio) of all the JPG files in the specified directory(s)
#   who's width is greater than the width specified on the command line.
#
#   python resizeimg.py --width 800 image-dir1 image-dir2 image-dir3...
#
#   resized images will be overwritten
#
#resizeimg.py
import cv2,sys,time
import fnmatch, os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='resize images in specified folders such that if thier width is > --width it will reduced to width preserving aspect ratio')
    parser.add_argument('--width', dest='width', required=True, type=int, help='width in pixels to clamp image size to')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='list of one or more directories to resize files')
    args = parser.parse_args()
    return args

def fixsize(filename, width):
    img = cv2.imread(filename)
    (h, w) = img.shape[:2]
                
    # Rationalize the image sizes
    if w > width:
        r = width / float(w)
        dim = (width, int(h * r))
        img = cv2.resize(img, dim)
        print ("resized:", filename, "from", (w, h), "to", dim)
        if not cv2.imwrite (filename, img):
            print ("failed writing:", filename)
            return None
    else:
        print ("No change", filename, (w,h))
        dim = (w, h)

    return dim
      
args = parse_args()
if args.width > 2000: 
    print ("--width should be less than 2000")
    sys.exit()
if len(args.args) < 1:
    print ("no directories to process")
    sys.exit()

for dir in args.args:
    files = [ os.path.join(dir, x) for x in fnmatch.filter(os.listdir(dir),'*.jpg')]
    if len(files) < 1:
        print ("skipping: no jpg files in", dir)
        continue
    for f in files:
        fixsize (f, args.width)
