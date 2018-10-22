import sys

ifile = open("../data/output.txt",'r')

temp = []
params = []
for line in ifile:
    temp.append(line)
    if " " not in line:
        if temp == []:
            continue
        params.append(temp)
        temp = []
        continue
params.append(temp)


count = len(params)
cutoff = int(float(sys.argv[1])*count)
train_corp = params[:cutoff]
test_corp = params[cutoff:]

ofile1 = open('../data/train_corp','w')
ofile2 = open('../data/test_corp','w')

for line in train_corp:
    for word in line:
        ofile1.write(word)

ofile1.close()
for line in test_corp:
    for word in line:
        ofile2.write(word)

ofile2.close()