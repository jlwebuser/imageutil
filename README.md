usage: python mirrorxyz.py directory x|y|z

Read each jpg file in directory, and make a mirror image of it flipped on the specified axis/axes
  x  -> flip upside down
  y  -> flip left/right
  z -> flip bottom left to top right (and x and y flip combined)

This is used to create more sample images for machine learning, it may help reduce directional bias.

The files created will have the following string added to the basename of the source jpg file (-xX, -yY, -zZ)

Examples:
 Flip all jpg/txt files in data/myfiles vertical around the x-axis (mirror image top/bottom)
       python mirrorxyz.py data/myfiles x

 Flip all jpg/txt files in data/myfiles horizontally around the y-axis (mirror image left/right)
       python mirrorxyz.py data/myfiles y

 Flip all jpg/txt files in data/myfiles vertically and horizontally (mirror left/right and top/bottom)
       python mirrorxyz.py data/myfiles z

If the associated rectangle markup files are found it will read, and flip the coordinations of the rectangle
matching the mirrored jpg file will have the same string added to the basename of the newly created txt file

  test.jpg --> test-xX.jpg
  test.txt --> test-xX.jpg
  test2.jpg --> test2-yY.jpg
  test2.txt --> test2-yY.txt
  test3.jpg --> test3-zZ.jpg
  test3.txt --> test3-zZ.txt

Notes
   tested on python3 on Windows 10
   requires opencv2 to be installed

   it will not overwrite your original jpg/txt files
   it will not attempt to process files that end in -xX.jpg, -yY.jpg, -zZ.jpg (they have already been flipped)
   if you run it multiple times on the same directory, it will overwrite previously generated mirrored jpg/txt files (-xX.*, -yY.*, -zZ.*)
    

