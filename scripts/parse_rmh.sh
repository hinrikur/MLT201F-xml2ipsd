
# input $1 = name of lemmatized folder


### making directories

OUT_NAME=${1//_lemmatized}_parsed
echo $OUT_NAME


echo "Creating /parsing/$OUT_NAME directory in xml2ipsd folder..."
pwd
if [ ! -d "../../xml2ipsd/parsing/$OUT_NAME" ];
  then
    mkdir ../../xml2ipsd/parsing/$OUT_NAME
  else
    echo "Directory '/parsing/$OUT_NAME' already exists. Using that."
fi

echo "Creating /parsing/$OUT_NAME/intermediate_files directory in xml2ipsd folder..."
if [ ! -d "../../xml2ipsd/parsing/$OUT_NAME/intermediate_files" ];
  then
    mkdir ../../xml2ipsd/parsing/$OUT_NAME/intermediate_files
  else
    echo "Directory '/parsing/$OUT_NAME/intermediate_files' already exists. Using that."
fi

echo "Creating /parsing/$OUT_NAME/parsed directory in xml2ipsd folder..."
if [ ! -d "../../xml2ipsd/parsing/$OUT_NAME/parsed" ];
  then
    mkdir ../../xml2ipsd/parsing/$OUT_NAME/parsed
  else
    echo "Directory '/parsing/$OUT_NAME/parsed' already exists. Using that."
fi

### Processing files

echo "Parsing files in $1"

for year in ../../xml2ipsd/$1/*; do
  # echo $year
  for filename in $year/*; do
    echo "Current file: ${filename##*/}"
    ./txt2ipsd-OBJ.sh "${filename//.lemmatized}" "${1//_lemmatized}_parsed"
    # echo "${filename//.lemmatized}" "${1//_lemmatized}_parsed"
  done
done

echo "Running additional CorpusSearch revision queries"
for file in ../../xml2ipsd/parsing/$OUT_NAME/intermediate_files/* ; do
  if [[ $file == *.ipsd ]]; then
    ./runall-OBJ.sh $file "${file//.ipsd}".psd
    mv "${file//.ipsd}".psd ../../xml2ipsd/parsing/$OUT_NAME/parsed/
  fi
done

# mv ../../xml2ipsd/parsing/morgunbladid_gefa/intermediate_files/.psd ../../xml2ipsd/parsing/morgunbladid_gefa/parsed/$1.psd


echo "All done!"
