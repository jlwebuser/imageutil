<h1>Utilties for working on image/label data for ML</h1>

<strong>mirrorxyz.py</strong> - make a mirror copy of a jpg around the x, y, or z axis (to get a reflection to increase) and if there is a yolo_mark lable file of the same name, created a mirror of it also.

<strong>makelst.py</strong> - reads a directoy of jpg and txt files that are of the yolo_mark format transforms to stdout a LST file that can be input   to im2rec.py so you can make a mxnet REC file for training or validation... 


<h2>mirrorxyz.py</h2>

<strong>usage: python mirrorxyz.py directory x|y|z</strong>

Read each jpg file in directory, and make a mirror image of it flipped around the specified axis
<blockquote>
  
        x -> flip upside down
        y -> flip left/right
        z -> flip bottom left to top right (and x and y flip combined)
</blockquote>

This is used to create more sample images for machine learning, it may help reduce directional bias. I find flipping on the y axis is the most useful, but the others can add additional variation. 

The files created will have the following string added to the basename of the source jpg file (-xX, -yY, -zZ)

Examples:
<blockquote>
Flip all jpg/txt files in data/myfiles vertical around the x-axis (mirror image top/bottom)
  
       python mirrorxyz.py data/myfiles x

Flip all jpg/txt files in data/myfiles horizontally around the y-axis (mirror image left/right)

       python mirrorxyz.py data/myfiles y

Flip all jpg/txt files in data/myfiles vertically and horizontally (mirror left/right and top/bottom)
       
        python mirrorxyz.py data/myfiles z

If the associated rectangle lable markup file is found it will read, and flip the coordinations of the rectangle
matching the mirrored jpg file will have the same string added to the basename of the newly created txt file.
For example:

    test.jpg --> test-xX.jpg  
    test.txt --> test-xX.jpg

    test2.jpg --> test2-yY.jpg
    test2.txt --> test2-yY.txt
  
    test3.jpg --> test3-zZ.jpg
    test3.txt --> test3-zZ.txt
</blockquote>
Notes
   tested on python3 on Windows 10
   requires opencv2 to be installed

   it will not overwrite your original jpg/txt files
   it will not attempt to process files that end in -xX.jpg, -yY.jpg, -zZ.jpg (they have already been flipped)
   if you run it multiple times on the same directory, it will overwrite previously generated mirrored jpg/txt files (-xX.*, -yY.*, -zZ.*)
    
<h2>makelst.py</h2>

<strong>usage: python makelst.py  directory-to-scan</strong> 

Scans the specified directory for JPG files, and the associated .txt file in the yolo_mark format. Produces to standard out a tab delimited LST file that is compatible with im2rec.py for creation of a REC dataset file.

Note that the LST file has a minimal header (it does not include the image width height) instructions in the code if you need to add them.

Requires 
python3 and opencv to be installed


