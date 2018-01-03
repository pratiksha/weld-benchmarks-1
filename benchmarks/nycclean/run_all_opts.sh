#!/bin/bash

input='all_opts'
while ln= read -r var
do
    echo ">>> $var"
    ./bench -f data/taxi_sf\=1.csv.small.0.5 -p $var -s 1 -t 1 | sed -n 5p
done < "$input"
