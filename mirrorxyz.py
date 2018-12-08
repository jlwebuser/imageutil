#!/usr/bin/python
# usage: mirrorxy directory x|y|z
#
# read each jpg file, and make a mirror image of it flipped on the specified axis/axes
#  x  -> flip upside down
#  y  -> flip left/right 
#  z -> flip bottom left to top right (and x and y flip combined)
#
# the files created will have the following string added to the basename of the source jpg file (-xX, -yY, -zZ) 
#
# examples:
# Flip all jpg/txt files in data/myfiles vertical around the x-axis (mirror image top/bottom)
#       python mirrorxyz.py data/myfiles x            
#
# Flip all jpg/txt files in data/myfiles horizontally around the y-axis (mirror image left/right)
#       python mirrorxyz.py data/myfiles y            
#
# Flip all jpg/txt files in data/myfiles vertically and horizontally (mirror left/right and top/bottom)
#       python mirrorxyz.py data/myfiles z            
#
#
#
# if the associated rectangle markup files are found it will read, and flip the coordinations of the rectangle
# matching the mirrored jpg file will have the same string added to the basename of the newly created txt file
#
#  test.jpg --> test-xX.jpg
#  test.txt --> test-xX.jpg
#  test2.jpg --> test2-yY.jpg
#  test2.txt --> test2-yY.txt
#  test3.jpg --> test3-zZ.jpg
#  test3.txt --> test3-zZ.txt
#

import cv2
import sys
import time
import os
import shutil
import fnmatch

flipmap = { 'x': 0, 'y' : 1, 'z' : -1 }

#
# using cv2 flip the source image around the specified axes
#  -1 (xy), 0=x, +1=y
# save into a new file specified by dest
#
def flipimage (src, dest, flipxyz):
    img = cv2.imread(src)
    if img is None:
        print ("Failed", src)
        return None
    else:
        flipped = cv2.flip( img, flipxyz)
        cv2.imwrite (dest, flipped)
        print ("Mirrored ", src, " to ", dest)
    return True

#
#  if the srctxtfile exists, flip the center of the rectangles specified in the srctxtfile, around 
#  the axes specified by flipxyz, and saved into mirror_txt_file 
#
def fliprect (srctxtfile, mirror_txt_file, flipxyz):
    try:
        # if it exists we are going to adjust the x coordinate of the centroid to sync with the mirror image
        with open(srctxtfile,"r") as f:
           lines= f.readlines()
           linesout = []
           # for each line adjust the centroid x coordinate to match the mirror image
           # s[1] is the x corrd, s[2] is the y coord
           for l in lines:
               s = l.split()
               if len(s) != 5:
                   continue
               # if flipxyz is 0, then just adjust y coord (top to bottomn flip of rectangle)
               # if flipxyz is 1, then just adjust x coord (left to right flip of rectangle)
               # if flipxyz is 2, then just adjust x,y coord (do both)
               if flipxyz == 0 or flipxyz == -1 :
                   s[2] = str(round(1.0 - float(s[2]), 6))
               if flipxyz == 1 or flipxyz == -1:
                   s[1] = str(round(1.0 - float(s[1]), 6))
               linesout.append(s)
       # make the txt file for the mirror destination image matching the mirror file name
        print ("Saving mirror rectangle file:", mirror_txt_file)
        try:
           outfile=open (mirror_txt_file, "w")
           for l in linesout:
               outfile.write (" ".join(l)+"\n\r")
           outfile.close()
        except IOError:
           print ("Error: failed writing ", mirror_txt_file)
           return False
    except IOError:
        print ("Warning: Bounding rectangle file does not exist: ", srctxtfile)
    return True
    
#
#  Main section that plucks and validates the args, and processes the file list
#
if len(sys.argv) == 3:
    # get path to directory to convert
    path = sys.argv[1]

    # validate the dir path and scan for jpg files
    try:
        dirlist = fnmatch.filter(os.listdir(path), "*.jpg")
    except:
        print ("Error:", sys.argv[0],": exception accessing",sys.argv[1] )
        sys.exit()

    # get the axis that we want to mirror the file around
    fliptag = sys.argv[2].lower()
    flipxyz = flipmap.get (fliptag)
    if flipxyz == None:
        print (sys.argv[0] + " : " + sys.argv[2] + " is not valid direction should be one of x, y, or z ")
        sys.exit()

    # fliptag will be the thing we append to the file basename to form the new file, it will be one of -xX, -yY, -zZ
    fliptag = "-" + fliptag + fliptag.upper()
    flipcounter = 0
    # process eash file in the dirlist
    for file in dirlist:
        # form the full path to the source jpg file
        src = os.path.join (path, file)
        # check that it is an original jpg file, and not a mirror file (which has the -xX, -yY, -zZ at the end
        if src[-7:] not in ["-xX.jpg", "-yY.jpg", "-zZ.jpg"]:
            # it is a jpg file, so form the path where we are going to put the mirror file (same directory)
            dest=src[:-4]+fliptag + ".jpg"
            # flip the image and store it into the destination path
            flipimage (src, dest, flipxyz)
            #now look for the rectangle file associated with the source jpg file
            txtfile=src[:-4] + ".txt"
            mirror_txt_file = dest[:-4]+".txt"
            fliprect (txtfile, mirror_txt_file, flipxyz)
            flipcounter += 1

    print (flipcounter, "files mirrored around", sys.argv[2])



            



