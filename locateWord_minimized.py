import os
import xml.etree.ElementTree as et
import sys
import re
import time
import subprocess
from line_profiler import LineProfiler

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

# verbs = tuple(open('dat_acc_sagnir.txt', 'r').readlines())



specific_verb = sys.argv[1]
punctuation =  ('!', '"', '#', '$', '%', '&', '(', ')', '*',
                '+', ',', '-', '/', ':', ';', '<', '=', '>',
                '?', '@', '[', ']', '^', '_', '`', '{', '|',
                '}', '~')

cwd = os.getcwd()
search_folder = sys.argv[2]
search_dir = os.path.join('/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff/', search_folder)
# rmh_dir = '/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff/rmh_morgunbladid'

# python3 locateWord_minimized.py gefa rmh_morgunbladid

print(search_folder)
print(search_dir)

# positive_xmls = []
out_folder = 'match_sentences'
out_dir = os.path.join(cwd, out_folder)

''' ========================= '''
'''      Föll skilgreind      '''
''' ========================= '''

def make_dirs(target_dir):
    '''
    Býr til möppu fyrir úttakskrár, ef hún er þegar ekki til.
    '''
    if os.path.isdir(target_dir):
        print('Output folder "match_sentences" exists. Using that')
        pass
    else:
        print('Creating output folder: "match_sentences"')
        os.mkdir(target_dir)

def make_sentFolder(year):
    out_year = os.path.join(out_dir, year + '_lemmatized')
    if os.path.isdir(out_year):
        print('Output folder "{0}" exists. Using that'.format(out_year))
        pass
    else:
        print('Creating output subfolder: "{0}"'.format(year + '_lemmatized'))
        os.mkdir(out_year)

def move_outputFile(file, year):
    out_year = os.path.join(out_dir, year + '_lemmatized')
    out_file = os.path.join(out_dir, file)
    subprocess.call(["mv", out_file, out_year])

# @profile
def match_verb(sentence):
    '''
    Tekur inn setningu og skilar True ef sögn í sagnalistanum er í setningunni
    '''
    for word in sentence:
        lemma = word.get('lemma')
        mark = word.get('type')
        for verb in verbs:
            verb_string = verb.strip()
            if verb_string == lemma and mark[0] == 's':
                return True
            else:
                pass

def match_specific_verb(sentence):
    '''
    Tekur inn setningu og skilar True ef tilgreind sögn er í setningunni
    '''
    for word in sentence:
        lemma = word.get('lemma')
        mark = word.get('type')
        if specific_verb == lemma and mark[0] == 's':
            return True
        else:
            continue

# # @profile
def parse_sent(sentence):
    word_list = []
    for token in sentence:
        word_list.append(token.text)
    return word_list

# @profile
def string_sent(sentence):
    '''
    Strengir saman token, tag og lemma og prentar
    Dæmi:
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
        if word.get('lemma') == None:
            word = str(word.text + ' ' + word.text + ' ' + word.text)
        else:
            word = str(word.text + ' ' + word.get('type') + ' ' + str(word.get('lemma')))
        word_list.append(word)
    return word_list

# # @profile
def write_to_file(sentence_list, file):
    file.write('\n'.join(sentence_list))
    file.write('\n\n')

# @profile
def traverse_subfolders(in_dir):
    sentence_counter = 0
    for year in os.listdir(in_dir):
        out_file_number = 1
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
                    if match_specific_verb(sentence):
                        sentence_counter += 1
                        # print(sentence_counter)
                        out_file_name = year + '_' + str(out_file_number) + '.lemmatized'
                        out_file = open(out_file_name, 'a+')
                        write_to_file(string_sent(sentence), out_file)
                        if sentence_counter == 10000:
                            print('Lemmatized file created:', out_file_name)
                            out_file_number += 1
                            sentence_counter = 0
        for dir, folders, files in os.walk(out_dir, topdown=False):
            for file in files:
                if not file.endswith('.lemmatized'): continue
                move_outputFile(file, year)
        end = time.time()
        print('End:', year+'.', 'Time elapsed:', '%.2f' % (end - start), 'seconds.')
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
