import os

BNC = open('../data/BNC_freq.txt', 'r')
f = open('../data/data.txt', 'r') # This method will not use training and testing split. It is the most naive model.
BNC_dict = BNC.readlines()
data = f.readlines()
output = open('dict_output.txt', 'w')
punct = ['.', ',', '?', '\"', '\'', '!', '>', '<', ':', ';']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
starters = ['#', '@']
num = 0

for line in data:
	num += 1
	if num % 4 == 1:
		output.write(line)
	elif num % 4 == 2:
		words = line.split(' ')
		for word in words:
			if word in BNC_dict:
				output.write(word + "\ten")
			elif word in punct or word[0] in starters or word in numbers:
				output.write(word + "\trest")
			else:
				output.write(word + "\thi")