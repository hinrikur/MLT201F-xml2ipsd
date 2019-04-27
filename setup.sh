#!/bin/bash

printf '\nMoving parsing scripts to /icecorpus/parsing/ directory...\n'
cp ./scripts/*.sh ../icecorpus/parsing/
echo 'Done.'

printf '\nCreating /parsing directory...\n'
if [ ! -d "./parsing" ];
  then
    mkdir ./parsing
  else
    echo 'Directory "/parsing" already exists. Using that.'
fi

echo 'Done.'
