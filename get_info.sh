#!/bin/bash

DIRECTORY='./match_sentences'
# in_dir=$1
out_filename='sentfiles_info.txt'
echo -e 'File\tNo. of sents.\tIdentical sents.\tNo. of tokens' >> $out_filename
for filename in $DIRECTORY/*.lemmatized; do
  echo $filename
  sentcount=$(wc -l < $filename)
  tokencount=$(wc -w < $filename)
  identicals=$(sort $filename | uniq -d | wc -l)
  echo -e ${filename: -8}'\t'$sentcount'\t'$identicals'\t'$tokencount >> $out_filename
done
