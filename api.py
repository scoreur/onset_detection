import sys
import os
from fCQT import *
from libsvm.python.svmutil import *

if len(sys.argv)<4:
    print "usage: <input wav> <input model> <length> <compress>"
    exit(1)


inputFile = sys.argv[1];
modelFile = sys.argv[2];
length = int(sys.argv[3])
compress = int(sys.argv[4])

print "processing\n"+inputFile


[signal,params] = wav_in(inputFile)
nchannels, sampwidth, framerate, nframes = params[:4]

p_labels,str_labels,time = onset_svm(signal,framerate, modelFile, length,compress)
for i in range(len(time)):
    print p_labels[i],str_labels[i],time[i]
