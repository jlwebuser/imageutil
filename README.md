<h1>Utilties for working on image/label data for ML</h1>

For detailed usage just specify --help on the command line for any file.

<strong>cleanupnames.py - scan a directory for all .jpg and associated yolo_mark .txt files and copy to a new directory with a new base filename +integer.

<strong>detectimg.py</strong> - Run detection on an MxNet network drawing bounding boxes of classes detected in model in the images specified. Numerous options to control threshold, images, display/recording of detection.

<strong>mirrorxyz.py</strong> - make a mirror copy of a jpg around the x, y, or z axis (to get a reflection to increase) and if there is a yolo_mark label file of the same name, created a mirror of it also.

<strong>makelst.py</strong> - reads a directoy of jpg and txt files that are of the yolo_mark format transforms to stdout a LST file that can be input   to im2rec.py so you can make a mxnet REC file for training or validation... 

<strong>resizeimg.py</strong>Resize all jpg files in a directory preserving aspect ratio.

<strong>dvr.py</strong>Class implements a simple recorder for short clips into an mp4 file. It is built to record a short clip of recgonition images after a network has detected an object.  Once triggered it runs for a specified duration to get context after a detection occurrs. 