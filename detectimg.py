#!/usr/bin/python
'''
usage: dettest.py [-h] --prefix PREFIX [--synset SYNSET] [--thresh THRESH]
                  [--pause PAUSE] [--nbbox NBBOX] [--width WIDTH]
                  [--imagedir IMAGEDIR] [--noplt]
                  ...

Draw bounding boxes of classes detected in model in the images found in
imagedir unless image(s) are specified on the command line.

positional arguments:
  args                 optional space separated list of files to load from
                       command line

optional arguments:
  -h, --help           show this help message and exit
  --prefix PREFIX      prefix of a trained model to load
  --synset SYNSET      text file name with list of class names one per line;
                       default synset.txt
  --thresh THRESH      show predictions >= thresh; default = 0.5
  --pause PAUSE        time to display image before moving to next; default
                       0.5s
  --nbbox NBBOX        max number of bounding boxes to draw; default 5
  --width WIDTH        width to scale input files for running inference;
                       default 600
  --imagedir IMAGEDIR  run detection on all jpg files in imagedir; default
                       tst.img
  --noplt              text only, do not popup plt canvass and draw bounding
                       boxes
'''

import mxnet as mx
import numpy as np
import cv2,sys,time
from collections import namedtuple
from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
import fnmatch, os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Draw bounding boxes of classes detected in model in the\nimages found in imagedir unless image(s) are specified on the command line.')
    parser.add_argument('--prefix', dest='prefix', required=True, type=str, 
                        help='prefix of a trained model to load')
    parser.add_argument ('--synset', dest='synset', type=str, default='synset.txt',
                        help='text file name with list of class names one per line; default synset.txt')
    parser.add_argument('--thresh', dest='thresh', type=float, default=0.5,
                        help='show predictions >= thresh; default = 0.5')
    parser.add_argument('--pause', dest='pause', type=float, default=0.5,
                        help='time to display image before moving to next; default 0.5s')
    parser.add_argument('--nbbox', dest='nbbox', type=int, default=5,
                        help='max number of bounding boxes to draw; default 5')
    parser.add_argument('--width', dest='width', type=int, default=600,
                        help='width to scale input files for running inference; default 600')
    parser.add_argument('--imagedir', dest='imagedir', default='tst.img',
                        help='run detection on all jpg files in imagedir; default tst.img')
    parser.add_argument('--noplt', dest='noplt', action='store_true',
                        help='text only, do not popup plt canvass and draw bounding boxes')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='optional space separated list of files to load from command line')
    args = parser.parse_args()
    return args

# load and bind the model specified by the prefix passed in
def loadModel(modelname):
        t1 = time.time()
        sym, arg_params, aux_params = mx.model.load_checkpoint(modelname, 0)
        t2 = time.time()
        t = 1000*(t2-t1)
        print("Loaded in %2.2f milliseconds" % t)
        arg_params['prob_label'] = mx.nd.array([0])
        mod = mx.mod.Module(symbol=sym)
        mod.bind(for_training=False, data_shapes=[('data', (1,3,416,416))])
        mod.set_params(arg_params, aux_params)
        return mod

# load in the label catagories contained in filename - having one label per line.
def loadCategories(filename):
        synsetfile = open(filename, 'r')
        synsets = []
        for l in synsetfile:
                synsets.append(l.rstrip())
        print ("Loaded Catagories: ", synsets)
        return synsets


# load the specified image, and adjust it for input into the network.
# the image will be scaled (preserving aspect ratio) to the width passed in
# this allows experiments to understand input resolution basis inference accuracy
def prepareNDArray(filename, width):
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        (h, w) = img.shape[:2]
        r = width / float(w)
        dim = (width, int(h * r))
        dim = (width, width)
        img = cv2.resize(img, dim)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]
        print ("\nFile: ", filename, "Shape: ", img.shape)
        return mx.nd.array(img)

# Load the specified image, prepair it for input into the network
# take the top n retuned predictions and split into parallel np arrays
# labels, scores, and bounding box       
def predict(filename, model, n, scale_width):
        t1 = time.time()
        array = prepareNDArray(filename, scale_width)
        Batch = namedtuple('Batch', ['data'])
        model.forward(Batch([array]))
        prob = model.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)
        t2 = time.time()
        t = (t2-t1)
        print("Predicted in %2.8f seconds" % t)
        a = prob[0:n]
        for z in a:
                if (z[0] >= 0):
                        print (z)
        r,c  = a.shape
        lab  = np.reshape (a[:,0], (r,1))
        score= np.reshape (a[:,1], (r,1))
        bbox = a[:,2:6]
        return lab, score, bbox

# Load network and catagories
def init(modelname, catfilename):
        model = loadModel(modelname)
        cats = loadCategories(catfilename)
        print ("loaded model:", modelname, "class names:", catfilename)
        return model, cats


args = parse_args()
net,classnames = init(args.prefix, args.synset)

if (len(args.args)>0):
    # use files from command line
    files = args.args
else:
    # use files in the specified imagedir
    files =  [ os.path.join(args.imagedir, x) for x in fnmatch.filter(os.listdir(args.imagedir),'*.jpg')]

print ("Using model:", args.prefix, "scaling to:", args.width)

for f in files:
        lables,scores,bbox = predict(f, net, args.nbbox, args.width)
        if not args.noplt:
            img = cv2.imread(f)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
            plt.close()  
            ax = utils.viz.plot_bbox(img, bbox, scores=scores, labels=lables, thresh=args.thresh, class_names=classnames, absolute_coordinates=False)
            plt.show(block=False)
            plt.pause (args.pause)

