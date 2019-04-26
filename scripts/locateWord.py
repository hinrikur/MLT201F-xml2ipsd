import os
import xml.etree.ElementTree as et
import sys
import re
import time
import subprocess
# from line_profiler import LineProfiler

'''
Hinrik Hafsteinsson - Vor 2019

Minnkuð útgáfa af locateWord.py.
Leitar að tiltekinni sögn  við .xml skrár í Risamálheild Árnastofnunar (RMH) og
skilar setningu á token/tag/lemma formi ef viðkomandi sagnorð finnst í
setningunni.

Inntak skriptunnar er hér miðað við undirmálheild RMH sem byggist upp af undir-
möppunum ÁR undirundirmöppunum MÁNUÐUR.
'''

''' ========================= '''
'''    Breytur skilgreindar   '''
''' ========================= '''

# input verb list defined by input argument
# either a .txt file with list of verbs (one verb per line) or a single verb
# on command line
if sys.argv[1].endswith('.txt'):
    print('Searching for words in wordlist "{0}"'.format(sys.argv[1]))
    verbs = set([line.strip() for line in open(sys.argv[1], 'r').readlines()])
    print(verbs)
else:
    print('Searching for specific word: "{0}"'.format(sys.argv[1]))
    verbs = sys.argv[1]
    # print(verbs)

punctuation =  ('!', '"', '#', '$', '%', '&', '(', ')', '*',
                '+', ',', '-', '/', ':', ';', '<', '=', '>',
                '?', '@', '[', ']', '^', '_', '`', '{', '|',
                '}', '~')

cwd = os.getcwd()
cwd_parent = os.path.dirname(cwd)
search_folder = sys.argv[2]
search_folder = 'rmh_morgunbladid'
search_dir = os.path.join(cwd_parent, search_folder)
# search_dir = os.path.join('/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff/', search_folder)
# rmh_dir = '/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff/rmh_morgunbladid'

# command line example:
# ./scripts/locateWord.py gefa rmh_morgunbladid match_sentences_gefa

# out_folder = 'match_sentences'
out_folder = search_folder + '_lemmatized'
out_dir = os.path.join(cwd, out_folder)

''' ========================= '''
'''      Föll skilgreind      '''
''' ========================= '''

''' Directories and files '''

def make_dirs(target_dir):
    '''
    Býr til möppu fyrir úttakskrár, ef hún er þegar ekki til.
    '''
    if os.path.isdir(target_dir):
        print('Output folder "{}" exists. Using that'.format(out_folder))
        pass
    else:
        print('Creating output folder: "match_sentences"')
        os.mkdir(target_dir)

def make_sentFolder(year):
    out_year = os.path.join(out_dir, year + '_lemmatized')
    if os.path.isdir(out_year):
        print('Output folder "{0}" exists. Using that'.format(year + '_lemmatized'))
        pass
    else:
        print('Creating output subfolder: "{0}"'.format(year + '_lemmatized'))
        os.mkdir(out_year)

def move_outputFile(file, year):
    '''
    Puts output files away in respective year folder.
    '''
    out_year = os.path.join(out_dir, year + '_lemmatized')
    out_file = os.path.join(out_dir, file)
    subprocess.call(["mv", out_file, out_year])

# String items

# @profile
def match_verb(sentence):
    '''
    Tekur inn setningu og skilar True ef sögn í sagnalistanum er í setningunni
    '''
    for word in sentence:
        lemma = word.get('lemma')
        mark = word.get('type')
        if type(verbs) is set:
            if lemma in verbs and mark[0] == 's':
                return True
            else:
                continue
        else:
            if verbs == lemma and mark[0] == 's':
                return True
            else:
                continue

# # @profile
def parse_sent(sentence):
    '''
    Extracts word elements from sentence object in .xml tree
    '''
    word_list = []
    for token in sentence:
        word_list.append(token.text)
    return word_list

# @profile
def string_sent(sentence):
    '''
    Strings together the token, tag and lemma of each word in sentence.
    Adds greedy a newline character if the word is either 'en' or 'og' to
    simulate correct sentence structure for later syntactic parsing.
        Example:
        Því aa því
        er sfg3en vera
        meðal ae meðal
        annars fohee annar
        haldið sþghen halda
        fram aa fram
        . . .
    '''
    word_list = []
    for word in sentence:
        if word.text in punctuation: continue
        elif word.text in ['en', 'og']:
            wordLine = '\n' + str(word.text + ' ' + word.get('type') + ' ' + str(word.get('lemma')))
        elif word.get('lemma') == None:
            wordLine = str(word.text + ' ' + word.text + ' ' + word.text)
        else:
            wordLine = str(word.text + ' ' + word.get('type') + ' ' + str(word.get('lemma')))
        word_list.append(wordLine)
    return word_list

# # @profile
def write_to_file(sentence_list, file):
    '''
    Writes the sentence from a list of words to specific file
    '''
    file.write('\n'.join(sentence_list))
    file.write('\n\n')

# @profile
def traverse_subfolders(in_dir):
    for year in os.listdir(in_dir):
        sentence_counter = 0
        total_sents = 0
        out_file_number = 1
        sentence_set = set()
        if year.startswith('.'): continue
        print('\nBegin:', year)
        print('...')
        start = time.time()
        make_sentFolder(year)
        year_path = os.path.join(in_dir, year)
        for dir, months, files in os.walk(year_path, topdown=True):
            for xml in files:
                if not xml.endswith('.xml'): continue
                xml_file = os.path.join(dir, xml)
                tree = et.parse(xml_file)
                root = tree.getroot()
                for sentence in root.iter('{http://www.tei-c.org/ns/1.0}s'):
                    # print(sentence_counter)
                    if match_verb(sentence):
                        sentence_counter += 1
                        # print(sentence_counter)
                        out_file_name = year + '_' + str(out_file_number) + '.lemmatized'
                        out_file = open(out_file_name, 'a+')
                        sentence_string = string_sent(sentence)
                        if tuple(sentence_string) not in sentence_set:
                            write_to_file(string_sent(sentence), out_file)
                            sentence_set.add(tuple(sentence_string))
                        if sentence_counter == 10000:
                            sentence_set = set()
                            total_sents += sentence_counter
                            # print(total_sents)
                            print('Lemmatized file created:', out_file_name)
                            out_file_number += 1
                            sentence_counter = 0
        total_sents += sentence_counter
        sentence_counter = 0
        print('Moving output files to correct directory...')
        for file in os.listdir(out_dir):
            if not file.endswith('.lemmatized'): continue
            move_outputFile(file, year)
        print('Files moved.')
        end = time.time()
        print('End:', year+'.', 'Time elapsed:', '%.2f' % (end - start), 'seconds.')
        print('Total sentences for year {0}: {1}'.format(year, total_sents))
        # print('Writing log to file')


''' ========================= '''
'''        Föll keyrð         '''
''' ========================= '''

if __name__ == '__main__':
    # verb_dict = populate_dict(verbs)
    make_dirs(out_folder)
    os.chdir(out_dir)
    traverse_subfolders(search_dir)
    # log_dict(verb_dict)
