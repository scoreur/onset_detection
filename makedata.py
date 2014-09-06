import sys
import os
from fCQT import *

filterType = ['wav']
num = 0
dict = {'A':1,'Bb':2,'bB':2,'B':3,'C':4,'bD':5,'Db':5,'D':6,'bE':7,'Eb':7,'E':8,'F':9,'bG':10,'Gb':10,'G':11,'bA':12,'Ab':12}
files = ['']*10000
pitch = [0]*10000

def search(path=None):
    if not path:
        print('path or searchString is empty')
        return
    global num
    _loopFolder(path)
    print("%s file find" % num)
 
def _loopFolder(path):
    global num
    
    arr = path.split('/')
    if not arr[-1].startswith('.'): 
        if os.path.isdir(path):
            folderList = os.listdir(path)
            for x in folderList:
                _loopFolder(path+"/"+x)
        elif os.path.isfile(path):
            if path.split('.')[-1].lower() in filterType:
                str = path.split('.')[-3]
                
                try:
                    pitch[num] = dict[str[:-1]]+int(str[-1])*12
                    
                except:
                    print path,str
                else:
                    if (pitch[num]>=5) or (pitch[num]<=86):
                        if (num>=1300):  #the number of the wav file to makedata
                            print num,"file"
                            fCQT(path,pitch[num])
                        print pitch[num]
                        files[num] = path
                        num+=1
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("invalid parameters")
    else:
        search(sys.argv[1])

print zip(range(100),pitch[:100],files[:100])


"""from freq_analysis import *



plt.plot(freq,F[0][int(len(F[0])/2):])
file_object = open("train.dat","w+")
for i in range(nKey):
    for j in range(len(F[i])):
        if F[i][j]!=0:
            file_object.write(str(j+1)+":"+str(F[i][j])+" ")
    file_object.write("\n")
file_object.close()"""
