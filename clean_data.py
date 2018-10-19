import os
import re

f = open('./data.txt', 'r')
clean = open('./cleaned_data.txt', 'a')
data = f.readlines()

exp = re.compile(r'\t\d*\t')
for line in data:
	altline = re.sub(exp, '', line)
	clean.write(altline)
	# print(line)