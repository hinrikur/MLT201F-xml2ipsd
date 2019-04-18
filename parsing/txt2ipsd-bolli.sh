
'''
Hinrik Hafsteinsson 2019
Based on IcePaHC preperation scripts<
'''

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



echo "Removing temporary files"
# rm $1.enc
# rm $1.tagged
# rm $1.lemmatized
rm $1.ipsdx

echo "Done"
