from tool.cqt import *
from onset_detection import *
from tool.normalizer import max_normalize
import matplotlib.pyplot as plt

nKey = len(seq_onset)

fmin = 32.7
fmax = 3951
b_hop = 7 # 31 bins per note, 31 can be replaced by any other odd number. trade-off between effiency and accuracy
bins = b_hop * 12
rad = int(b_hop/2)
drd = CQT(fmin,fmax,bins,framerate,hamming)
F = [0]*nKey
for j in range(nKey):
    i = seq_onset[j]
    """if (i>=2):
        print i,(i+1.0)/framerate*h
        x1 = drd.fast(signal[int((i-2)*h):int(i*h)])
        y1 = []
        for k in range(1,83):
            y1 += [sum(x1[k*b_hop-rad:k*b_hop+rad+1])/b_hop]
        y1 = max_normalize(y1)
    else :
        y1 = [0]*82"""
        
    if (i<=M-4):   
        print i,(i+1.0)/framerate*h
        x2 = drd.fast(signal[int((i+2)*h):int((i+4)*h)])
        y2 = []
        for k in range(1,83):
            y2 += [sum(x2[k*b_hop-rad:k*b_hop+rad+1])/b_hop]
        y2 = max_normalize(y2)
    else:
        y2 = [0]*82
        
    F[j] = y2

freq = [32.7*2**((i+1)/12.0) for i in range(82)] 

#plt.plot(freq,F[0][int(len(F[0])/2):],'r')

plt.plot(freq,F[0],'r')

plt.show()

file_object = open("train.dat","w")
for i in range(nKey):
    file_object.write("%d " %13)
    for j in range(len(F[i])):
        if F[i][j]!=0:
            file_object.write(str(j+1)+":"+str(F[i][j])+" ")
    file_object.write("\n")
file_object.close()
