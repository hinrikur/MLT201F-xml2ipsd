
## Introduction

___WORK IN PROGRESS___

This repository contains scripts that (1) extract sentences from Icelandic texts with based on specific words or words and (2) parse the sentences for use in syntactic research. The texts in question come from [the Icelandic Gigaword Corpus](https://malheildir.arnastofnun.is) (icel. *Risamálheildin, RMH*) which is run by the Árni Magnússon Institute for Icelandic Studies and can be downloaded from [Málföng.is](http://www.malfong.is).

The parsing scripts are based on the *Icelandic Parsed Historical Corpus* (*IcePaHC*, [available here](https://github.com/antonkarl/icecorpus)) which is required to use the parsing scripts in this repo.

## Instructions

### Crash course

#### Finding sentences by word:

1. Put your RMH subcorpus into your `xml2ipsd` folder's parent directory.
2. Edit the `parameters.ini` file to suit your data
3. Enter the following into the command line:

```
cd <relevent/path/here>/xml2ipsd/
python(3) ./scripts/locateWord.py -p
```
4. Your lemmatized data should be ready now.

#### Parsing lemmatized corpora (example corpus)

1. Enter the following into bash, line by line.

```
cd <relevent/path/here>/xml2ipsd/
./setup.sh
cd ../..icecorpus/parsing
./parse_rmh <your_lemmatized_folder_name>
```
2. Your parsed data should now be in your `xml2ipsd/parsing/` folder

### Extracting sentences  

The script `locateWord.py` (found in `xml2ipsd/scripts/`) takes in raw `.xml` data from any subdirectory of RMH and returns only sentences that contain specific words.

The script must be run from inside the `/xml2ipsd/` directory. The words can either be based on a text file, e.g. the `dat_acc_sagnir.txt` provided in the repo, or typed into the command line if looking for a single word.

By default the script uses the `parameters.ini` file in the `scripts/` directory to designate input. The input data (a subcorpus of the RMH corpus) should by default be located in the same directory as your `/xml2ipsd/`. ___Remote locations will be supported at a later date.___

<!--
The format is `python(3) ./scripts/locateWord.py <word origin> <input folder> <output>` .

Example if looking for specific word:

* `python3 ./scripts/locateWord.py gefa rmh_morgunbladid match_sentences_gefa`

Example if looking for words in a file:

* `python3 ./scripts/locateWord.py dat_acc_sagnir.txt rmh_morgunbladid match_sentences` -->

The texts are returned with a `.lemmatized` extension, with one token per line with the format "*token POS-tag lemma*".

## Parsing `.lemmatized` corpora

To parse the example *gefa*-corpus:

1. Download / clone this repository to the *same parent directory* as your __IcePaHC__ (your installation will likely be called `icecorpus`).

2. Go to the `/xml2ipsd` directory and run `setup.sh`. This copies the necessary scripts in your `icecorpus/parsing/` directory.

3. Extract `match_sentences_gefa.zip` to your `xml2ipsd/` directory.

4. Go to the `icecorpus/parsing` directory and run `parse_rmh_gefa.sh`. This script first runs the `txt2ipsd-OBJ.sh` script to parse the `.lemmatized` files in the example *gefa*-corpus and then runs the `runall-OBJ` to fix parsing errors in the files. This may take a while.

5. After running, the directory `/xml2ipsd/parsing/morgunbladid_gefa/` should now have appeared, containing your corpus in `.psd` format.
