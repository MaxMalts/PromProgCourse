#!/bin/bash

LC_NUMERIC="en_US.UTF-8"

while [ $# -gt 0 ]
do
    key=$1
    shuffle=0
    case $key in
    --input)
        input=$2
        shift 2
        ;;
    --train_ratio)
        train_ratio=$2
        shift 2
        ;;
    --shuffle)
        shuffle=1
        shift 1
        ;;
    --train_file)
        train_file=$2
        shift 2
        ;;
    --val_file)
        val_file=$2
        shift 2
        ;;
    *)
        shift 1
        ;;
    esac
done

header=$(awk '(NR==1)' $input)
dataset=$(awk '(NR>1)' $input)
n_elements=$(printf "${dataset}" | awk 'END {print NR}')
n_train_elements=$(printf %.0f $(echo "${n_elements} * ${train_ratio}" | bc))

if [[ shuffle -eq 1 ]]
then
    dataset=$(printf "${dataset}" | sort -R)
fi

printf "${dataset}" | awk "BEGIN{print \"${header}\"} (NR<=${n_train_elements})" > $train_file
printf "${dataset}" | awk "BEGIN{print \"${header}\"} (NR>${n_train_elements})" > $val_file