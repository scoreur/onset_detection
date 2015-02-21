import os,sys

f = open("train.dat",'r')
g = open("train1.dat",'w+')
for line in f:
    pitch = int(line.split(' ')[0])
    if (pitch>=5) and (pitch<=86):
        g.write(line)

f.close()
g.close()
