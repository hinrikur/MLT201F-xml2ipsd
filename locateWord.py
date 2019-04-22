import os
import xml.etree.ElementTree as et
import sys
import re
import time
from line_profiler import LineProfiler

'''
Hinrik Hafsteinsson - Vor 2019

Skripta sem ber saman lista af sagnorðum (hér heitir hún
'dat_acc_sagnir.txt') við .xml skrár í Risamálheild Árnastofnunar (RMH) og
skilar setningu á token/tag/lemma formi ef viðkomandi sagnorð finnst í
setningunni.

Inntak skriptunnar er hér miðað við undirmálheild RMH sem byggist upp af undir-
möppunum ÁR undirundirmöppunum MÁNUÐUR.
'''

''' ========================= '''
'''    Breytur skilgreindar   '''
''' ========================= '''

verbs = tuple(open('dat_acc_sagnir.txt', 'r').readlines())
punctuation = ('!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~')

cwd = os.getcwd()

rmh_dir = sys.argv[0]
rmh_dir = '/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff/rmh_morgunbladid'


positive_xmls = []
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
        pass
    else:
        print('Crateing output folder: "match_sentences"')
        os.mkdir(target_dir)

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
    print(in_dir)
    for year in os.listdir(in_dir):
        if year.startswith('.'): continue
        print(year)
        print('\nBegin:', year)
        print('...')
        start = time.time()
        year_path = os.path.join(in_dir, year)
        print(year_path)
        for dir, months, files in os.walk(year_path, topdown=True):
            for xml in files:
                if not xml.endswith('.xml'): continue
                xml_file = os.path.join(dir, xml)
                # print(xml_file)
                tree = et.parse(xml_file)
                root = tree.getroot()
                # dates = root.iter('{http://www.tei-c.org/ns/1.0}date')
                # dates = [date.text for date in dates]
                # doc_year = dates[1][:4]
                for sentence in root.iter('{http://www.tei-c.org/ns/1.0}s'):
                    if match_verb(sentence):
                        out_file_name = str(year) + '.lemmatized'
                        out_file = open(out_file_name, 'a+')
                        write_to_file(string_sent(sentence), out_file)
        end = time.time()
        print('End:', year+'.', 'Time elapsed:', '%.2f' % (end - start), 'seconds.')
        # print('Writing log to file')


''' ========================= '''
'''        Föll keyrð         '''
''' ========================= '''

# verb_dict = populate_dict(verbs)

make_dirs(out_folder)
os.chdir(out_dir)

traverse_subfolders(rmh_dir)

# log_dict(verb_dict)
