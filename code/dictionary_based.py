import os

def get_words():
	BNC = open("../data/BNC_freq.txt", "r")
	params = BNC.readlines()
	split_params = [par.split("\t")for par in params]
	index = 2
	words = []
	while index < len(split_params):
		if len(split_params[index]) > 1:
			words.append(split_params[index][1])
		index += 1
	return words

print(get_words())