#!/usr/bin/python
'''cleanupnames.py  src-dir dest-dir basename</h2>
#
#  Script to clean up names of JPG and yolo_mark label files into a new directory.
#
#  Many times I will do a mass download of files using a tool like googleimagesdownload
#  which ends up getting a lot of very long ugly filenames.
#
#
#  Note:
#  It makes duplicate jpg and (the associated yolo_mark formatted lables files exists)
#  in the dst-directory using the basname + counter.
#
#  It will not modify the source JPG/TXT file in the src-dir.
#  It will overwrite files in the dest-dir.
#
#  If the .txt file associated with a .jpg file is missing it just process the JPG file,
#  and silently continue.
#
#  It will ONLY process .txt files for which a JPG file exists.
#
#  If the JPG/TXT file is a result of the script mirrorxyz.py (tagged wtih -xX, or -yY, or -zZ)
#  This way its still easy to tell that its a mirror image.
#
#
#   python cleanupnames.py src-dir dest-dir  img
#
#   src-dir/foo99999.jpg   -> dest-dir/img0.jpg
#   src-dir/foo99999.txt   -> dest-dir/img0.txt
#   src-dir/crappppyyy.jpg -> dest-dir/img1.txt
#   src-dir/232432-xX.jpg  -> dest-dir/img2-xX.jpg
#   src-dir/232432-xX.txt  -> dest-dir/img2-xX.txt
#
'''

import os
import sys
import shutil
import fnmatch

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "src-dir dst-dir base-filename")
    sys.exit()

# get path to directory to convert
srcpath = sys.argv[1]
dstpath = sys.argv[2]
newname = sys.argv[3]

if not os.path.exists(srcpath):
    print(sys.argv[0], srcpath, "does not exist")
    sys.exit()
if not os.path.exists(dstpath):
    print(sys.argv[0], dstpath, "does not exist")
    sys.exit()

counter = 0
dirlist = fnmatch.filter(os.listdir(srcpath), "*.jpg")
for file in dirlist:
    # form the full path to the source jpg file
    srcjpg = os.path.join(srcpath, file)
    basename = newname
    if file[-7:] in ["-xX.jpg", "-yY.jpg", "-zZ.jpg"]:
        basename = basename + file[-7:-4]

    txtfile = srcjpg[:-4] + ".txt"
    dstjpg = os.path.join(dstpath, basename+str(counter) + ".jpg")
    dsttxt = os.path.join(dstpath, basename+str(counter) + ".txt")
    shutil.copyfile(srcjpg, dstjpg)
    print("Copy:", srcjpg, "to", dstjpg)
    if os.path.exists(txtfile):
        shutil.copyfile(txtfile, dsttxt)
        print("Copy:", txtfile, "to", dsttxt)
    counter += 1

print(sys.argv[0], ": processed", counter, "jpg files")
