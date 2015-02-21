import random


f = open("train.dat",'r')
g1 = open("train80%.dat",'w+')
g2 = open("cv20%.dat","w+")

for line in f:
    if (random.random()>=0.8):
        g2.write(line)
    else:
        g1.write(line)

f.close()
g1.close()
g2.close()
