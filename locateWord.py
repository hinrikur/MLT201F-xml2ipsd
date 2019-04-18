import os
import xml.etree.ElementTree as et
import re
import time

'''
Hinrik Hafsteinsson - Vor 2019

Skrifta sem ber saman lista af sagnorðum (hér heitir hún
'dat_acc_sagnir.txt') við .xml skrár í Risamálheild Árnastofnunar (RMH) og
skilar setningu á token/tag/lemma formi ef viðkomandi sagnorð finnst í
setningunni.

Inntak skriptunnar er hér miðað við undirmálheild RMH sem byggist upp af undir-
möppunum ÁR undirundirmöppunum MÁNUÐUR.
'''

''' ========================= '''
'''    Breytur skilgreindar   '''
''' ========================= '''

verbs = open('dat_acc_sagnir.txt', 'r').readlines()

# ATH þetta er absolute directory sem virkar ekki nema í minni vél.
# settu dir á þinni eigin inntaksmöppu hér
rmh_dir = '/Users/hinrik/Documents/skoli/MA/vor_2019/MLT201F/morgunbladid_stuff/rmh_morgunbladid'

rmh = os.listdir(rmh_dir)

positive_xmls = []
out_folder = 'match_sentences'
out_dir = os.path.join(os.getcwd(), out_folder)

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
        os.mkdir(target_dir)

def populate_dict(verb_lst):
    '''
    (virkar ekki sem stendur)
    Býr til dict sem telur fjölda hvers sagnorðs sem finnst
    '''
    dict = {}
    for verb in verbs:
        dict[verb.strip()] = 0
    return dict

def match_verb(sentence, dict):
    '''
    Tekur inn setningu og skilar True ef sögn í sagnalistanum er í setningunni
    '''
    for word in sentence:
        lemma = word.get('lemma')
        mark = word.get('type')
        for verb in verbs:
            verb_string = verb.strip()
            # print(verb_string)
            if verb_string == lemma:
                # dict[verb_string] += 1
                # print(verb, '->', dict[verb.strip()])
                # return True
                # print(verb_string)
                return True
            else:
                pass

def log_dict(dict):
    '''
    (virkar ekki sem stendur)
    Skrifar teljara-dictið í skrá
    '''
    with open('verb_numbers.txt', 'w') as file:
        for k,v in dict.items():
            file.write(k + '\t' + str(v) + '\n')

def parse_sent(sentence):
    word_list = []
    for token in sentence:
        word_list.append(token.text)
    return word_list

def string_sent(sentence):
    '''
    Strengir saman token, tag og lemma með /
    '''
    word_list = []
    for word in sentence:
        word = str(word.text + '/' + word.get('type') + '/' + str(word.get('lemma')))
        word_list.append(word)
    return word_list

def write_to_file(sentence_list, file):
    file.write(' '.join(sentence_list))
    file.write('\n\n')

def traverse_subfolders(dir, dict):
    # print(verb_string)
    for year in dir:
        if not year.startswith('.'):
            year_path = os.path.join(rmh_dir, year)
            # print(year_path)
            for month in os.listdir(year_path):
                if not month.startswith('.'):
                    print('\nBegin:', month, '-', year)
                    print('...')
                    start = time.time()
                    month_path = os.path.join(year_path, month)
                    for xml in os.listdir(month_path):
                        if not xml.endswith('.xml'): continue
                        xml_file = os.path.join(month_path, xml)
                        tree = et.parse(xml_file)
                        root = tree.getroot()
                        for sentence in root.iter('{http://www.tei-c.org/ns/1.0}s'):
                            if match_verb(sentence, dict):
                                out_file_name = str(year) + '.txt'
                                out_file = open(out_file_name, 'a+')
                                write_to_file(string_sent(sentence), out_file)
                    end = time.time()
                    print('End:', month, '-', year+'.', 'Time elapsed:', '%.2f' % (end - start), 'seconds.')
                    print('Writing log to file')
                    # add_to_file(month, year)
                    # for k,v, in dict.items():
                    #     print(k,v)

''' ========================= '''
'''        Föll keyrð         '''
''' ========================= '''

verb_dict = populate_dict(verbs)

make_dirs(out_folder)
os.chdir(out_dir)

traverse_subfolders(rmh, verb_dict)

log_dict(verb_dict)
