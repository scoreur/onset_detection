name = raw_input("please input the file which is to be modified\n")

f = open(name,"r");
g = open('_'+name,"w");
for line in f:
    data = line.split(' ')
    pitch = int(data[0])

    if (pitch % 12 ==1) or (pitch %12 == 2) or (pitch % 12 == 3):
        pitch = pitch +12
    pitch = pitch -12
    
    print(data[0]+"->",pitch)
    data[0] = str(pitch)
    new_line = ' '.join(data)
    g.write(new_line)

print("correction is finished")    
f.close()
g.close()
