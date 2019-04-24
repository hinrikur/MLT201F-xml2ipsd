
for year in ../../xml2ipsd/match_sentences_gefa/*; do
  # echo $year
  for filename in $year/*; do
    echo "Current file: $filename"
    ./txt2ipsd-OBJ.sh "${filename//.lemmatized}" morgunbladid_gefa
  done
done


echo "Running additional CorpusSearch revision queries"
for file in ../../xml2ipsd/parsing/morgunbladid_gefa/intermediate_files/* ; do
  if [[ $file == *.ipsd ]]; then
    ./runall-OBJ.sh $file "${file//.ipsd}".psd
    mv "${file//.ipsd}".psd ../../xml2ipsd/parsing/morgunbladid_gefa/parsed/
  fi
done

mv ../../xml2ipsd/parsing/morgunbladid_gefa/intermediate_files/$1.psd ../../xml2ipsd/parsing/morgunbladid_gefa/parsed/$1.psd
