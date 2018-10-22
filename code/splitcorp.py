import sys

ifile = open(sys.argv[1],'r')

temp = []
params = []
for line in ifile:
    if " " not in line:
        if temp == []:
            continue
        params.append(temp)
        temp = []
        continue
    temp.append(line)

count = len(params)
cutoff = int(int(sys.argv[2])*count)
train_corp = params[:cutoff]
test_corp = params[cutoff:]

ofile1 = open('../data/train_corp','w')
ofile2 = open('../data/test_corp','w')

for line in train_corp:
    ofile1.write(line)

ofile1.close()
for line in test_corp:
    ofile2.write(line)

ofile2.close()