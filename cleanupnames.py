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
#   cleanupnames.py --srcdir src --dstdir dst  --basename img
#
#   src/foo99999.jpg   -> dst/img0.jpg
#   src/foo99999.txt   -> dst/img0.txt
#   src/crappppyyy.jpg -> dst/img1.txt
#   src/232432-xX.jpg  -> dst/img2-xX.jpg
#   src/232432-xX.txt  -> dst/img2-xX.txt
#
'''
import os
import sys
import shutil
import fnmatch
import argparse

def parse_args():
    '''Load args...'''
    description = '''Read all the JPG files (and associated yolo label txt files) in srcdir
    and copy them to dstdir using basename plus a counter.

    It will not modify the source JPG/TXT file in the srcdir.

    It will overwrite files in the dstdir.

    If the .txt file associated with a .jpg file is missing it just process the JPG file,
    and silently continue.

    It will ONLY process .txt files for which a JPG file exists.

    If the JPG/TXT file is a result of the script mirrorxyz.py (tagged
    with -xX, or -yY, or -zZ). This way its still easy to tell that its a
    mirror image.

    usage: cleanupnames.py --srcdir src --dstdir dst  --basename img

    for example:
    src/foo99999.jpg   -> dst/img0.jpg
    src/foo99999.txt   -> dst/img0.txt
    src/crappppyyy.jpg -> dst/img1.txt
    src/232432-xX.jpg  -> dst/img2-xX.jpg
    src/232432-xX.txt  -> dst/img2-xX.txt

    '''
    parser = argparse.ArgumentParser(description)
    parser.add_argument('--srcdir', dest='srcdir', required=True, type=str,
                        help='source directory to copy files from')
    parser.add_argument('--dstdir', dest='dstdir', required=True, type=str,
                        help='target directory to copy renamed files into')
    parser.add_argument('--basename', dest='basename', required=True, type=str,
                        help='basename to use to form new file names')

    args = parser.parse_args()
    return args

ARGS = parse_args()

if not os.path.exists(ARGS.srcdir):
    print(sys.argv[0], ARGS.srcdir, "(srcdir) does not exist", file=sys.stderr)
    sys.exit()

if not os.path.exists(ARGS.dstdir):
    print(sys.argv[0], ARGS.dstdir, "(dstdir) does not exist", file=sys.stderr)
    sys.exit()

#loop through one file at a time
COUNTER = 0
for file in fnmatch.filter(os.listdir(ARGS.srcdir), "*.jpg"):
    # form the full path to the source jpg file
    srcjpg = os.path.join(ARGS.srcdir, file)
    basename = ARGS.basename
    if file[-7:] in ["-xX.jpg", "-yY.jpg", "-zZ.jpg"]:
        # preserve extentions by mirrorxzy.py if the file has it
        basename += file[-7:-4]

    txtfile = srcjpg[:-4] + ".txt"
    dstjpg = os.path.join(ARGS.dstdir, basename+str(COUNTER) + ".jpg")
    dsttxt = os.path.join(ARGS.dstdir, basename+str(COUNTER) + ".txt")
    shutil.copyfile(srcjpg, dstjpg)
    print("Copy:", srcjpg, "to", dstjpg, file=sys.stderr)
    if os.path.exists(txtfile):
        shutil.copyfile(txtfile, dsttxt)
        print("Copy:", txtfile, "to", dsttxt, file=sys.stderr)
    COUNTER += 1

print(sys.argv[0], ": processed", COUNTER, "jpg files", file=sys.stderr)
