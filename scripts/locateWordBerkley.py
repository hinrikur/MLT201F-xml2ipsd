import os
import xml.etree.ElementTree as et
import sys
import re
import time
import subprocess
import configparser
# from line_profiler import LineProfiler

'''
Hinrik Hafsteinsson - Spring 2019
MLT-201F - xml2ipsd project

Duplicate from locateWord.py

This script looks for a specific verb in a subcorpus of the Icelandic Gigaword
Corpus (Risamálheildin, RMH) and returns the word's sentence in a
token/tag/lemma format in an output file.

The script's input is preferrably a subcorpus of the RMH corpus, consisting of
the subdirectory <YEAR> and subsubdirectory <MONTH>.

The script's output are .txt files, which each
contain up to 10,000 match sentences each.
'''

''' ========================= '''
'''     Variables defined     '''
''' ========================= '''

cwd = os.getcwd()
cwd_parent = os.path.dirname(cwd)

punctuation =  ('!', '"', '#', '$', '%', '&', '(', ')', '*',
                '+', '-', '/', ':', ';', '<', '=', '>',
                '?', '@', '[', ']', '^', '_', '`', '{', '|',
                '}', '~')

# input verb list defined by input argument
# either a .txt file with list of verbs (one verb per line) or a single verb
# on command line
if sys.argv[1].endswith('.txt'):
    print('Searching for words in wordlist "{0}"'.format(sys.argv[1]))
    target_words = set([line.strip() for line in open(sys.argv[1], 'r').readlines()])
    print(target_words)
    search_folder = sys.argv[2]
    search_dir = os.path.join(cwd_parent, search_folder)
    out_folder = search_folder + '_inBP'
    out_dir = os.path.join(cwd, out_folder)
elif sys.argv[1] == '-p':
    params = configparser.ConfigParser()
    params.read('scripts/parameters.ini')
    search_folder = params['inputs']['input_name']
    search_dir = os.path.join(cwd_parent, search_folder)
    if params['words']['single'] == 'False':
        wordfile = params['words']['wordlist']
        target_words = set([line.strip() for line in open(wordfile, 'r').readlines()])
        out_folder = search_folder + '_inBP'
        out_dir = os.path.join(cwd, out_folder)
    else:
        target_words = params['words']['word']
        out_folder = search_folder + '_' + params['words']['word'] + '_inBP'
        out_dir = os.path.join(cwd, out_folder)
else:
    print('Searching for specific word: "{0}"'.format(sys.argv[1]))
    target_words = sys.argv[1]
    search_folder = sys.argv[2]
    search_dir = os.path.join(cwd_parent, search_folder)
    out_folder = search_folder + '_' + sys.argv[1] + '_inBP'
    out_dir = os.path.join(cwd, out_folder)

# command line example:
# ./scripts/locateWord.py -p
# or
# ./scripts/locateWord.py gefa rmh_morgunbladid match_sentences_gefa
# or
#

''' ========================= '''
'''     Functions defined     '''
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
    out_year = os.path.join(out_dir, year + '_inBP')
    if os.path.isdir(out_year):
        print('Output folder "{0}" exists. Using that'.format(year + '_inBP'))
        pass
    else:
        print('Creating output subfolder: "{0}"'.format(year + '_inBP'))
        os.mkdir(out_year)

def move_outputFile(file, year):
    '''
    Puts output files away in respective year folder.
    '''
    out_year = os.path.join(out_dir, year + '_inBP')
    out_file = os.path.join(out_dir, file)
    subprocess.call(["mv", out_file, out_year])

# String items

# @profile
def match_word(sentence):
    '''
    Tekur inn setningu og skilar True ef sögn í sagnalistanum er í setningunni
    '''
    for word in sentence:
        lemma = word.get('lemma')
        mark = word.get('type')
        if type(target_words) is set:
            if lemma in target_words and mark[0] == 's':
                return True
            else:
                continue
        else:
            if target_words == lemma and mark[0] == 's':
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

def string_sent_BP(sentence):
    '''
    Strings the words of a whole sentence.
    Specifically for BerkleyParser input.
    '''
    word_list = []
    for word in sentence:
        if word.text in punctuation: continue
        elif word.get('lemma') == None:
            word_list[-1] = word_list[-1] + word.text
        # elif word.text == '.':
        #     word_list[-1] = word_list[-1] + '.'
        # elif word.text == ',':
        #     word_list[-1] = word_list[-1] + ','
        else:
            word_list.append(word.text)
    return word_list

# # @profile
def write_to_file(sentence_list, file):
    '''
    Writes the sentence from a list of words to specific file
    '''
    file.write(' '.join(sentence_list))
    file.write('\n\n')

# @profile
def traverse_subfolders(in_dir):
    '''
    Traverses file structure, parses .xml files and calls helper functions to
    return sentences and writes them to files.
    '''
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
                    if match_word(sentence):
                        sentence_counter += 1
                        # print(sentence_counter)
                        out_file_name = year + '_' + str(out_file_number) + '.txt'
                        out_file = open(out_file_name, 'a+')
                        sentence_string = string_sent_BP(sentence)
                        if tuple(sentence_string) not in sentence_set:
                            write_to_file(string_sent_BP(sentence), out_file)
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
'''       Functions run       '''
''' ========================= '''

if __name__ == '__main__':
    make_dirs(out_folder)
    os.chdir(out_dir)
    traverse_subfolders(search_dir)
