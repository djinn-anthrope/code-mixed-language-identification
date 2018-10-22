import re

class HMM:
    def __init__(self):
        self.emmision = {}
        self.transition = {}
        self.train_corpus = []
        self.test_corpus = []
        self.test_corp_correct = []
        self.context = {}
        self.word_tag_sets = {}
        self.unique_lang = []
        self.most_probable_lang = {}
        self.bigram_count = {}
        self.split_corpus()
        self.generate_model()
        # self.accuracy_hmm()

    def tag_sentences(self):
        ifile = open("../data/output.txt", "r")
        regex_param = re.compile(r'[0-9]+')
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
        params.append(temp)
        split_params = [[(pair.split(" ")[0], pair.split(" ")[-1].strip('\n')) for pair in sent if " " in pair] for sent in params if sent != []]
        words = [[pair.split(" ")[0] for pair in sent if " " in pair] for sent in params if sent != []]
        return split_params, words


    def split_corpus(self):
        tagged_sentences, sentences = self.tag_sentences()
        total = len(tagged_sentences)
        cutoff = int(0.65 * total)
        self.train_corpus = tagged_sentences[:cutoff]
        self.test_corpus = sentences[cutoff:]
        self.test_corp_correct = tagged_sentences[cutoff:]

    def accuracy_hmm(self):
        Ncount = 10000
        total_count = 0
        corr_count = 0
        for ind, sentence in enumerate(self.test_corpus[:Ncount]):
            predicted = self.viterbi_algorithm(sentence)
            actual = [pos for word, pos in self.test_corp_correct[ind]]
            total_count += len(actual)
            for j, pred in enumerate(predicted):
                if predicted[j] == actual[j]:
                    corr_count += 1

        print("Accurracy of HMM Model:: ", corr_count / total_count * 100)

    def generate_model(self):
        for sentence in self.train_corpus:
            # print(sentence)
            l1 = len(sentence)
            trigram = ("<lang>", "<lang>")
            bigram = ("<s>",)
            for word, pos in sentence:
                if pos not in self.unique_lang:
                    self.unique_lang.append(pos)
                    self.most_probable_lang[pos] = {}

                if word not in self.most_probable_lang[pos]:
                    self.most_probable_lang[pos][word] = 0

                self.most_probable_lang[pos][word] += 1

                if word not in self.word_tag_sets:
                    self.word_tag_sets[word] = set()
                self.word_tag_sets[word].add(pos)

                bigram += (pos,)

                trans_key = trigram + (pos,)
                if trans_key not in self.transition:
                    self.transition[trans_key] = 0
                self.transition[trans_key] += 1

                emm_key = bigram + (word,)

                if (bigram[0], word) not in self.bigram_count:
                    self.bigram_count[(bigram[0], word)] = 0
                self.bigram_count[(bigram[0], word)] += 1

                if emm_key not in self.emmision:
                    self.emmision[emm_key] = 0
                self.emmision[emm_key] += 1
                # print(trans_key, emm_key)
                trigram = (trigram[1], pos)
                bigram = (word,)

            trans_key = (sentence[l1 - 2][1], sentence[l1 - 1][1], '</lang>')
            if trans_key not in self.transition:
                self.transition[trans_key] = 0
            self.transition[trans_key] += 1

        # emm_key = (sentence[l1-1][0],'</pos>','</s>')
        # if emm_key not in self.emmision:
        # 	self.emmision[emm_key] = 0
        # self.emmision[emm_key] += 1

        N = sum(self.transition.values())
        V = len(self.transition.values())
        lmdb = 0.05
        for tran in self.transition:
            # self.transition[tran] /= self.context[tran[0:2]]
            self.transition[tran] = (self.transition[tran] + lmdb) / (N + lmdb * V)
        self.transition['_'] = lmdb / (N + lmdb * V)

        N = sum(self.emmision.values())
        V = len(self.emmision.values())
        for emm in self.emmision:
            # self.emmision[emm] /= self.context[emm[0:2]]
            self.emmision[emm] = (self.emmision[emm] + lmdb) / (N + lmdb * V)
        self.emmision['_'] = lmdb / (N + lmdb * V)

        N = sum(self.bigram_count.values())
        V = len(self.bigram_count.values())
        for bg in self.bigram_count:
            # self.bigram_count[bg] /= tots
            self.bigram_count[bg] = (self.bigram_count[bg] + lmdb) / (N + lmdb * V)
        self.bigram_count['_'] = lmdb / (N + lmdb * V)

    def get_prob(self, d, word):
        possible = 0
        if word in d:
            possible = d[word]
        else:
            possible = d['_']
        return possible

    def forward_algorithm(self, sequence):
        alpha = {}
        for i, word in enumerate(sequence):
            alpha[i] = {}
            if i == 0:
                possible = []
                if word in self.word_tag_sets:
                    possible = self.word_tag_sets[word]
                else:
                    possible = self.unique_lang
                for pos in possible:
                    emm_prob = self.get_prob(self.emmision, ("<s>", pos, word))
                    init_prob = self.get_prob(self.bigram_count, ("<s>", word))
                    alpha[i][pos] = init_prob * emm_prob
            else:
                possible = []
                prev1 = []
                prev2 = []
                if word in self.word_tag_sets:
                    possible = self.word_tag_sets[word]
                else:
                    possible = self.unique_lang
                # print(sequence[i-1][0])
                if sequence[i - 1] in self.word_tag_sets:
                    prev1 = self.word_tag_sets[sequence[i - 1]]
                else:
                    prev1 = self.unique_lang
                # print(prev1)
                if i > 1:
                    if sequence[i - 2] in self.word_tag_sets:
                        prev2 = self.word_tag_sets[sequence[i - 2]]
                    else:
                        prev2 = self.unique_lang
                else:
                    prev2 = ["<lang>"]
                for pos in possible:
                    x_prob = 0
                    emm_prob = self.get_prob(self.emmision, (sequence[i - 1], pos, word))
                    sum1 = 0
                    for prev_pos in prev1:
                        # print(prev_pos, pos)
                        sum2 = 0
                        for prev_pos2 in prev2:
                            sum2 += self.get_prob(self.transition, (prev_pos2, prev_pos, pos))
                        sum1 += alpha[i - 1][prev_pos] * sum2
                    alpha[i][pos] = emm_prob * sum1

        # print(alpha)
        prob_obs = 0
        for key in alpha[i]:
            if key == '_':
                continue
            # print(key, alpha[i][key])
            prob_obs += alpha[i][key]
        return prob_obs

    def viterbi_algorithm(self, sequence):
        dp = {}
        bp = {}
        n = len(sequence)
        dp[-1] = {}
        dp[-1][("<lang>", "<lang>")] = 1
        for i, word in enumerate(sequence):
            possible = []
            prev1 = []
            prev2 = []
            if word in self.word_tag_sets:
                possible = self.word_tag_sets[word]
            else:
                possible = self.unique_lang

            prevword = ''
            if i == 0:
                prevword = '<s>'
                prev1 = ['<lang>']
                prev2 = ['<lang>']
            elif i == 1:
                prevword = sequence[i - 1]
                if sequence[i - 1] in self.word_tag_sets:
                    prev1 = self.word_tag_sets[sequence[i - 1]]
                else:
                    prev1 = self.unique_lang
                prev2 = ['<lang>']
            else:
                prevword = sequence[i - 1]
                if sequence[i - 1] in self.word_tag_sets:
                    prev1 = self.word_tag_sets[sequence[i - 1]]
                else:
                    prev1 = self.unique_lang
                # print(prev1)
                if sequence[i - 2] in self.word_tag_sets:
                    prev2 = self.word_tag_sets[sequence[i - 2]]
                else:
                    prev2 = self.unique_lang
            dp[i] = {}
            bp[i] = {}
            for pos in possible:
                emm_prob = self.get_prob(self.emmision, (prevword, pos, word))
                for prev_pos1 in prev1:
                    maxval = -999999
                    argmax = ''
                    for prev_pos2 in prev2:
                        trans_prob = self.get_prob(self.transition, (prev_pos2, prev_pos1, pos))
                        # print(pos, prev_pos1, prev_pos2,dp,dp[i-1])
                        prod = dp[i - 1][(prev_pos2, prev_pos1)] * trans_prob
                        if prod > maxval:
                            maxval = prod
                            argmax = prev_pos2
                    dp[i][(prev_pos1, pos)] = emm_prob * maxval
                    bp[i][(prev_pos1, pos)] = argmax
            # dp[0]['<pos> ' + pos] = {'v':emm_prob*init_prob,'b':0}
        # else:
        # possible = []
        # prev1 = []
        # prev2 = []
        prev1 = []
        prev2 = []

        # print(sequence[i-1][0])
        if sequence[n - 1] in self.word_tag_sets:
            prev1 = self.word_tag_sets[sequence[n - 1]]
        else:
            prev1 = self.unique_lang
        # print(prev1)
        if n - 2 == -1:
            prev2 = ['<lang>']
        else:
            if sequence[n - 2] in self.word_tag_sets:
                prev2 = self.word_tag_sets[sequence[n - 2]]
            else:
                prev2 = self.unique_lang
        POS = [0] * n
        argmax = ()
        maxval = -999999
        # print(dp)
        for prev_pos1 in prev1:
            for prev_pos2 in prev2:
                trans_prob = self.get_prob(self.transition, (prev_pos2, prev_pos1, '</lang>'))
                # print(dp[n-1])
                prod = dp[n - 1][(prev_pos2, prev_pos1)] * trans_prob
                if prod > maxval:
                    maxval = prod
                    argmax = (prev_pos2, prev_pos1)
        POS[n - 1] = argmax[1]
        POS[n - 2] = argmax[0]
        # print(POS)
        # print(bp)
        for i in range(n - 3, -1, -1):
            # print(bp[i])
            POS[i] = bp[i + 2][(POS[i + 1], POS[i + 2])]

        return POS

    def get_bestfit_tags(self, index):
        sentence = self.test_corpus[index]
        # print("\n==========TESTING==========\n\nGiven Observation Sequence:: ", ' '.join(sentence))

        # prob_obs = self.forward_algorithm(sentence)
        POS = self.viterbi_algorithm(sentence)

        # print("\nProbability of Observation Sequence:: ", prob_obs)
        # print("\nBEST FIT SEQUENCE:::\n")

        n = len(sentence)

        for i in range(n):
            # print(sentence[i],'\t\t',POS[i])
            print('{:<17} {}'.format(sentence[i], POS[i]))

        # print("\n===========================\n")

    def get_ABP(self):
        return (self.transition, self.emmision, self.bigram_count)

    def print_most_probable_tags(self):
        print("\nTOP 50 MOST PROBABLE WORD FOR EACH LANG\n")
        for pos, val in self.most_probable_lang.items():
            sorted_val = [word[0] for word in sorted(val.items(), key=lambda x: x[1], reverse=True)[:50]]
            print('{:<10} {}'.format(pos, sorted_val))
        print('\n\n\n')


    def print_output(self):
        for i in range(len(self.test_corpus)):
            self.get_bestfit_tags(i)
            print('\n\n\n')

hmm = HMM()
hmm.print_most_probable_tags()
# hmm.print_output()
hmm.accuracy_hmm()
A, B, P = hmm.get_ABP()