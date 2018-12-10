#!/usr/bin/python
'''clamp the width (and height preserving aspect ratio) of all the JPG
   files in the specified directory(s) who's width is greater than the
   width specified on the command line.

   python resizeimg.py --width 800 image-dir1 image-dir2 image-dir3...

   resized images will be overwritten'''
import sys
import fnmatch
import os
import argparse
import cv2

def parse_args():
    '''Process command line'''
    description = '''resize images in specified folders such that if thier width
is > --width it will reduced to width preserving aspect ratio'''
    parser = argparse.ArgumentParser(description, usage="resizeimg.py --width 250 dir1 dir2...")
    parser.add_argument('--width', dest='width', required=True, type=int,
                        help='width in pixels to clamp image size to')
    parser.add_argument('args', nargs=argparse.REMAINDER,
                        help='list of one or more directories to resize files')
    return parser.parse_args()

def fixsize(filename, width):
    '''Clamp the width of the image to that specified preserving the aspect ratio'''
    img = cv2.imread(filename)
    (h, w) = img.shape[:2]

    # Rationalize the image sizes
    if w > width:
        r = width / float(w)
        dim = (width, int(h * r))
        img = cv2.resize(img, dim)
        print("resized:", filename, "from", (w, h), "to", dim, file=sys.stderr)
        if not cv2.imwrite(filename, img):
            print("failed writing:", filename, file=sys.stderr)
            return None
    else:
        print("No change", filename, (w, h), file=sys.stderr)
        dim = (w, h)

    return dim

ARGS = parse_args()
if not ARGS.args:
    print(sys.argv[0] + ": no directory specified", file=sys.stderr)
    sys.exit()

if ARGS.width > 2000:
    print("--width should be less than 2000", file=sys.stderr)
    sys.exit()

for fdir in ARGS.args:
    try:
        files = [os.path.join(fdir, x) for x in fnmatch.filter(os.listdir(fdir), '*.jpg')]
    except:
        print (sys.argv[0]+": can't access ", fdir, file=sys.stderr)
        continue
    if not files:
        print("skipping: no jpg files in", fdir, file=sys.stderr)
        continue
    for f in files:
        fixsize(f, ARGS.width)
