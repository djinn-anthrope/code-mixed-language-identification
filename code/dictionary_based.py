import os
import re

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

def get_corpus():
	file = open("../data/data.txt", "r")
	data = file.readlines()
	information = dict()
	count = 0
	key = 0
	while count < len(data):
		if count % 4 == 0:
			key = data[count].split("\t")[1].split("\n")[0]
		elif count % 4 == 1:
			information[key] = data[count].split("\t")[1].split("\n")[0]
		count += 1
	return information

def classifier(lang1_dict, sentence):
	regex = re.compile('[@]*[#]*[A-Z]{2,}(?![a-z])[_]*|[@]*[#]*[A-Z][a-z]+(?=[A-Z])[_]*|[@]*[#]*[\w]+[_]*')
	words = re.findall(regex, sentence)
	numbers = [str(i) for i in range(1000000)]
	classed_sent = list()
	for word in words:
		if word.lower() in lang1_dict:
			classed_sent.append((word, "en"))
		elif '#' in word or '@' in word or '_' in word:
			classed_sent.append((word, "rest"))
		elif word in numbers:
			classed_sent.append((word, "rest"))
		else:
			classed_sent.append((word, "hi"))

	return classed_sent

def output(classed_sent, corpus):
	f = open("../output/dict_output.txt")
	

# print(get_words()
# print(get_corpus())
example = 'My sis @cool_nikkki is saying that "Aaj jo Indian Idol ke Grand Finale me aayi to wo Kareena nhi balki uski hamshakl thi.. " #Irony'

words = get_words()
corpus = get_corpus()
classed_sent = classifier()
for entry in corpus:
	print(classifier(get_words(), corpus[entry]))