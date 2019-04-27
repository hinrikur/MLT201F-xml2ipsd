# echo "Encoding special markup"
# python3 ./scripts/encodemarkup.py $1.tok $1.enc

# echo "Tagging using IceTagger"
# cat $1.enc | java -classpath "../IceNLP/IceNLPCore.jar" is.iclt.icenlp.runner.RunIceTagger > $1.tagged
#
# echo "Lemmatizing using Lemmald"
# cat $1.enc | java -Xmx256m -classpath "../IceNLP/IceNLPCore.jar" is.iclt.icenlp.runner.RunIceTagger -of 1 -lem > $1.lemmatized

# python3 ./scripts/joinlemma.py $1.tagged $1.lemmatized

#debug
echo $0
echo $1
echo $2



# Generate .tagged file from .lemmatized file
awk '/ / {print $1 " " $2} !/ / {print $0}' $1.lemmatized > $1.taggedx # file where line breaks need fixing
# changing single newlines to space and double newlines to single newlines
awk '{printf "%s ", $0}' $1.taggedx | sed 's/  /\
/g' > $1.tagged

echo "Parsing using IceParser"
cat $1.tagged | java -classpath "../IceNLP/IceNLPCore.jar" is.iclt.icenlp.runner.RunIceParser -f -l > $1.ipsdx

echo "Converting IceParser's ipsd output to labeled bracketing"
# Assumes .ipsd input and .psd output
python3 ./scripts/ipsd2psd.py $1

echo "Decoding special markup"
python ./scripts/decodemarkup.py $1.ipsd $1.ipsd

# echo "Running additional CorpusSearch revision queries"
# ./runall-OBJ.sh $1.ipsd $1.psd

# making directories
echo "Moving output files"

mv $1.tagged $1.taggedx $1.ipsdx $1.ipsd ../../xml2ipsd/parsing/$2/intermediate_files/
# mv $1.lemmatized ../../sagnir_bolli/parsing/lemmatized
# mv $1.psd ../../xml2ipsd/parsing/$2/parsed/

# ../../xml2ipsd/match_sentences/1999

echo "Removing temporary files"
# rm $1.enc
# rm $1.tagged
# rm $1.lemmatized
# rm $1.ipsdx

echo "Done"
