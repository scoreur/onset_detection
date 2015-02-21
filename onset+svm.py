import sys
import os
from fCQT import *
from libsvm.python.svmutil import *

"""os.chdir("C:\Users\hq\Documents\GitHub\onset_detection")
name = raw_input('please input the name of the .wav file \n')
length = int(raw_input())
x,time = fCQT(name,length)
y = [0]*len(x)

#y0,x0 = svm_read_problem("libsvm\data\_train2201.dat")
#model = svm_train(y0,x0,'-t 0 -c 10')
#svm_save_model("libsvm\data\model.dat",model)
model = svm_load_model('libsvm\data\model.dat')
p_labels, p_acc, p_vals = svm_predict(y,x,model)

for i in range(len(y)):
    print int(p_labels[i]),transfer_pitch(int(p_labels[i])),time[i]"""

"""def onset_svm(signal,nframerate,length=200000,compress=1):
    x,time = fCQT(signal,nframerate,length,compress)
    y = [0]*len(x)
	
    model = svm_load_model('libsvm\data\model.dat')
    p_labels, p_acc, p_vals = svm_predict(y,x,model)
	
    str_labels=[0]*len(y)
    for i in range(len(y)):
       p_labels[i] = int(p_labels[i])
       str_labels[i] = transfer_pitch(int(p_labels[i]))

    return p_labels,str_labels,time"""

	
	
os.chdir("C:\Users\hq\Documents\GitHub\onset_detection")
name = raw_input('please input the name of the .wav file \n')
length = int(raw_input('please input the length\n'))
compress = int(raw_input('please input the compress rate \n'))	
print "processing\n"+name
[signal,params] = wav_in(name)
nchannels, sampwidth, framerate, nframes = params[:4]

p_labels,str_labels,time = onset_svm(signal,framerate,length,compress)
for i in range(len(time)):
    print p_labels[i],str_labels[i],time[i]

