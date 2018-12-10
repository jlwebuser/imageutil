#!/usr/bin/python
'''
This script scans the specified directory for JPG/TXT files using the "YOLO" markup
The yolo markup is a txt file by the same name containing the labels for that image.
The yolo markup has the ClassID  Xcenter yCenter  xExtent y Extent
It produces to standard out a LST file that is suitable for the im2rec.py script

Notes
If a JPG file is missing its associated Txt file, an empty label list will be returned,
and a well formed line with a fake label of -1. -1. -1. -1. -1  will be emitted - if its
just left with no label it seems like recordio rejects it -
https://github.com/zhreshold/mxnet-ssd/issues/163

If the txt file has multiple labels, they will all be read, converted, and emitted in a
line in the lst file (its possible that they should be sorted by classid in the future)

The order of the output is determined by the directory listing - if you want to
randomize the order, then use something like the unix shuf command.

if you have alot of lables (10+ make sure to set the label_width really
large (like 500 in the hyperparameters))
'''
import sys
import os
import fnmatch
import argparse
import cv2

def parse_args():
    '''Load args...'''
    description = '''Generate an LST format to standard out from JPG files and
    label files in the yolo format for processing by im2rec.py\n'''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--imagedir', dest='imagedir', required=True,
                        help='process jpg/txt files in imagedir')
    args = parser.parse_args()
    return args

def processfile(srcjpg):
    '''
    Read the jpg file specified
    Read its associated label (.txt) file from the same directory/basename
    ending with .txt (if it exists) If the txt file does not exist, or has
    no labels then a single label of [-1,-1,-1,-1,-1] will be emitted.
    Produce the w, h, and a list containing the 0..n class id, and convert the
    center/extents of the label to a bounding rectangle
    Return None if it can't read the jpg file'''
    img = cv2.imread(srcjpg)
    if img is None:
        print(sys.argv[0], "Skipping image: failed reading", srcjpg, file=sys.stderr)
        return None

    height, width, _ = img.shape
    txtfile = srcjpg[:-4] + ".txt"
    try:
        # if it exists, process the label box dimensions
        labels = []
        with open(txtfile, "r") as f:
            lines = f.readlines()
            for l in lines:
                s = l.split()
                if len(s) != 5:
                    continue
                xmin = round(float(s[1]) - float(s[3])/2, 5)
                ymin = round(float(s[2]) - float(s[4])/2, 5)
                xmax = round(float(s[1]) + float(s[3])/2, 5)
                ymax = round(float(s[2]) + float(s[4])/2, 5)
                labels.append([str(float(s[0])), str(xmin), str(ymin), str(xmax), str(ymax)])
    except IOError:
        pass
    if not labels:
        # No labels for this image, but im2rec expects at least one, so pass this
        labels.append(["-1.", "-1.", "-1.", "-1.", "-1."])
    return True, width, height, labels

#
#  Main section that plucks and validates the args, and processes the file list
#
ARGS = parse_args()
COUNT = 0
# validate the dir path and scan for jpg files
try:
    DIRLIST = fnmatch.filter(os.listdir(ARGS.imagedir), "*.jpg")
except os.error:
    print(sys.argv[0], ": exception accessing", ARGS.imagedir, file=sys.stderr)
    sys.exit()

# process eash file in the dirlist
for file in DIRLIST:
    # form the full path to the source jpg file, read it and get the dimensions
    src_jpg = os.path.join(ARGS.imagedir, file)
    success, _, _, labels = processfile(src_jpg)
    label_s = [item for sublist in labels for item in sublist]

    # this line format is documented https://mxnet.incubator.apache.org/api/python/
    # image/image.html#image-iterator-for-object-detection
    # Index, A  B  [extra header]  [(object0), (object1), ... (objectN)] file
    # Where A is the width (number of fields including itself) of header (2 which
    # are A(this number), and B (the number of fields in a single label)),
    # B is the number of fields in a label. for this program a label has 5 fields
    # classid, xmin, ymin, xmax, ymax
    # if you wanted the image width and height in the header, just bump the
    # A (str(2)) value up to str(4), and put str(width), str(height) before B(str(5))
    # i've not found anything that required width/height so leaving it out.
    lstline = [str(COUNT), str(2), str(5)] + label_s + [file]
    print('\t'.join(lstline))
    if success:
        COUNT += 1
