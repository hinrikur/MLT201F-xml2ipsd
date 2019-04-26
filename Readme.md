
## Introduction

___WORK IN PROGRESS___

This repository contains scripts that (1) extract sentences from Icelandic texts with based on specific words or words and (2) parse the sentences for use in syntactic research. The texts in question come from [the Icelandic Gigaword Corpus](https://malheildir.arnastofnun.is) (icel. *Risamálheildin, RMH*) which is run by the Árni Magnússon Institute for Icelandic Studies and can be downloaded from [Málföng.is](http://www.malfong.is).

The parsing scripts are based on the *Icelandic Parsed Historical Corpus* (*IcePaHC*, [available here](https://github.com/antonkarl/icecorpus)) which is required to use the parsing scripts in this repo.

## Extracting sentences  

The script `locateWord.py` (found in __/xml2ipsd/scripts__) takes in raw `.xml` data from any subdirectory of RMH and returns only sentences that contain specific words.

The script must be run from inside the __/xml2ipsd/__ directory. The words can either be based on a text file, e.g. the `dat_acc_sagnir.txt` provided in the repo, or typed into the command line if looking for a single word. The script also requires the name of your input folder an arbitrary name of the requested output folder. The input data (a subcorpus of the RMH corpus) should by default be located in the same directory as your __/xml2ipsd/__. ___Otherwize you must edit the script with the correct location.___

The format is `python(3) ./scripts/locateWord.py <word origin> <input folder> <output>` .

Example if looking for specific word:

* `python3 ./scripts/locateWord.py gefa rmh_morgunbladid match_sentences_gefa`

Example if looking for words in a file:

* `python3 ./scripts/locateWord.py dat_acc_sagnir.txt rmh_morgunbladid match_sentences`

The texts are returned in a `.lemmatized` format, with one token per line with the format "*token POS-tag lemma*".

## Parsing `.lemmatized` corpora

To parse the example *gefa*-corpus:

1. Download / clone this repository to the *same parent directory* as your __IcePaHC__ (your installation will likely be called __icecorpus__).

2. Go to the __/xml2ipsd__ directory and run `setup.sh`. This copies the necessary scripts in your __/icecorpus/parsing__ directory.

3. Extract `match_sentences_gefa.zip` to your __/xml2ipsd__ directory.

4. Go to the __/icecorpus/parsing__ directory and run `parse_rmh_gefa.sh`. This script first runs the `txt2ipsd-OBJ.sh` script to parse the `.lemmatized` files in the example *gefa*-corpus and then runs the `runall-OBJ` to fix parsing errors in the files. This may take a while.

5. After running, the directory __/xml2ipsd/parsing/morgunbladid_gefa__ should now have appeared, containing your corpus in `.psd` format.
