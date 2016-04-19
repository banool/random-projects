#!/bin/bash

total=0
for file in *.mp3;
do extra=$(mp3info -p "%S\n" $file);
total=$(($total+$extra));
done;
#echo $total;

# From https://stackoverflow.com/questions/12199631/convert-seconds-to-hours-minutes-seconds-in-bash
function show_time () {
    num=$1
    min=0
    hour=0
    day=0
    if((num>59));then
        ((sec=num%60))
        ((num=num/60))
        if((num>59));then
            ((min=num%60))
            ((num=num/60))
            if((num>23));then
                ((hour=num%24))
                ((day=num/24))
            else
                ((hour=num))
            fi
        else
            ((min=num))
        fi
    else
        ((sec=num))
    fi
    echo "$day"d "$hour"h "$min"m "$sec"s
}

show_time $total;
