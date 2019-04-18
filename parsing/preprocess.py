import os
import sys

wd = os.getcwd()
parent = os.path.dirname(wd)

# sent_file = '10_fyrstu_mbl_1999.txt'
# filepath = os.path.join(parent, sent_file)
# outname = sent_file[:-4] + '.lemmatized'

# filepath = 'match_sentences/1999.txt'
filepath = sys.argv[1]
filepath = os.path.join(parent, filepath)
outname = filepath[-4:]

def process(sentence):
    words = []
    sent = sentence.split()
    unneed = ['"', '%', '"']
    for word in sent:
        word = word.replace('/', ' ')
        word = word.split()
        if word[0] in unneed:
            continue
        if word[2] == 'None':
            word[2] = word[0]
            word[1] = word[0]
        word = ' '.join(word)
        words.append(word)
    return words

def get_sents(infile):
    with open(infile, 'r') as file:
        sents = file.readlines()
        return sents

with open(outname, 'w+') as outfile:
    for sent in get_sents(filepath):
        for i in process(sent):
            outfile.write(i + '\n')
        outfile.write('\n')
