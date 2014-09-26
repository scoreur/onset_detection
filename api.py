import sys
import os
from fCQT import *
#from libsvm.python.svmutil import *

if len(sys.argv)<5:
    print "usage: <input wav> <input model> <output txt> <length> <compress>"
    exit(1)


inputFile = sys.argv[1]
modelFile = sys.argv[2]
outputFile = sys.argv[3]
length = int(sys.argv[4])
compress = int(sys.argv[5])

print "processing\n"+inputFile




p_labels,str_labels,time = onset_svm(inputFile, modelFile, outputFile, length,compress)

