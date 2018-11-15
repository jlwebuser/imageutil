#
#  This script scans the specified directory for JPG/TXT files using the "YOLO" markup 
#  The yolo markup is a txt file by the same name containing the labels for that image.
#  The yolo markup has the ClassID  Xcenter yCenter  xExtent y Extent
#  It produces to standard out a LST file that is suitable for the im2rec.py script 
#
#  Notes
#  if a JPG file is missing its associated Txt file, an empty label list will be returned, 
#  and a well formed line with a fake label of -1. -1. -1. -1. -1  will be emitted - if its
#  just left with no label it seems like recordio rejects it - https://github.com/zhreshold/mxnet-ssd/issues/163
#
#  If the txt file has multiple labels, they will all be read, converted, and emitted in a line 
#  in the lst file (its possible that they should be sorted by classid in the future)
#
#  The order of the output is determined by the directory listing - if you want to randomize the order, then use something like the unix shuf command.
#
#  if you have alot of lables (10+ make sure to set the label_width really large (like 500 in the hyperparameters))
#

import cv2
import sys
import time
import os
import shutil
import fnmatch


#
# Read the jpg file specified
# Read its associated lable (.txt) file that with the same directory/basename ending with .txt
# Produce the w, h, and a list containing the 0..n class id, and convert the center/extents of the label to a bounding rectangle
# Return None if it can't read the jpg file
#
def processfile (srcjpg):
    img = cv2.imread(srcjpg)
    if img is None:
        print (sys.argv[0], "Skipping image: failed reading", srcjpg)
        return None

    height, width, channels = img.shape

    txtfile=srcjpg[:-4] + ".txt"
    try:
        # if it exists, process the label box dimensions
        labels = [] 
        with open(txtfile,"r") as f:
            lines= f.readlines()
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
        print (sys.argv[0], "rectangle file does not exist: ", txtfile)
        return None
    global maxlab
    if len(labels) > maxlab:
        maxlab = len(labels)
        #print ("maxlab:", maxlab, srcjpg)
    if len(labels) == 0:
        labels.append(["-1.", "-1.", "-1.", "-1.", "-1."])
    return True, width, height, labels

#
#  Main section that plucks and validates the args, and processes the file list
#
maxlab = 0
count = 0
if len(sys.argv) == 2:
    # get path to directory to convert
    path = sys.argv[1]
    # validate the dir path and scan for jpg files
    try:
        dirlist = fnmatch.filter(os.listdir(path), "*.jpg")
    except:
        print (sys.argv[0],": exception accessing",sys.argv[1] )
        sys.exit()
    
    # get the lst file name to be created
    #lstfile = sys.argv[2]
    # process eash file in the dirlist
    for file in dirlist:      
        # form the full path to the source jpg file, read it and get the dimensions
        srcjpg = os.path.join (path, file)
        success, width, height, labels = processfile (srcjpg)
        labels = [item for sublist in labels for item in sublist]
 
        # this line format is documented https://mxnet.incubator.apache.org/api/python/image/image.html#image-iterator-for-object-detection
        # Index, A  B  [extra header]  [(object0), (object1), ... (objectN)] file
        # Where A is the width (number of fields including itself) of header (2 which are A(this number), and B (the number of fields in a single label)), 
        # B is the number of fields in a label. for this program a label has 5 fields  classid, xmin, ymin, xmax, ymax
        # if you wanted the image width and height in the header, just bump the A (str(2)) value up to str(4), and put str(width), str(height) before B(str(5))
        # i've not found anything that required width/height so leaving it out. 
        lstline = [str(count), str(2), str(5) ] + labels + [file]
        print ('\t'.join(lstline))
        #flat_list = [item for sublist in labels for item in sublist]
        if success:
            count +=1
        
else:
    print ("usage:", sys.argv[0], "directory-containing-jpg")

    



            



