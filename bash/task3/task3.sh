#!/bin/bash

IFS=  # so that strings are oparated "as is"

while [ $# -gt 0 ]
do
    key=$1
    case $key in
    --num_workers)
        num_workers=$2
        shift 2
        ;;
    --input_file)
        input_file=$2
        shift 2
        ;;
    --links_index)
        links_index=$2
        shift 2
        ;;
    --output_folder)
        output_folder=$2
        shift 2
        ;;
    *)
        shift 1
        ;;
    esac
done

links=$(awk "BEGIN {FS = \",\"}
{    
    if (NR == 1) {
        for (i = 1; i <= NF; ++i) {
            if (\$i == \"${links_index}\") {
                links_column = i
            }
        }
        
    } else {
        print \$links_column
    }
}" $input_file)

echo $links | parallel -j $num_workers wget -P $output_folder