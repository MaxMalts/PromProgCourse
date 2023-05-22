#!/bin/bash

size=0

analyze_file() {
    cur_size=$(( $(stat -c%b $1) * $(stat -c%B $1) ))
    (( size += cur_size ))
    
    if [ -d $1 ]
    then
        for file in $(ls $1)
        do
            analyze_file $1/$file
        done
    fi

}

analyze_file $1
echo $(( $size / 1024 ))'K	'$1
