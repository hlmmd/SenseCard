#coding:utf-8
import os.path
#read sno
SNOS = []
with open('students.txt', encoding='utf-8') as file:
    lines = file.read().split('\n')
    for line in lines:
        if len(line)==0 or  line[0]=='#':
            continue
        cols = line.split(',')
        cols[3]=cols[3].strip()
        cols[3]= cols[3].lstrip()
        SNOS.append(cols[3])

print(len(SNOS))

for sno in SNOS:
    if (SNOS.count(sno)>1):
        print(sno)

exit()

count = 0
for SNO in SNOS:
    filename = "C:\\Users\\qinrui\\Desktop\\jpg\\" + str(SNO)+".jpg"
    #rint(filename)
    if os.path.exists(filename)==False:
        count+= 1
        print(SNO)
    elif os.path.exists(filename)==True :
        count+=1
print(count)
    

      