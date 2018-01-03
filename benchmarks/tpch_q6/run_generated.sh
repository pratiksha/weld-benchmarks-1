#!/bin/bash

cols=20
nitems=10000000
sels=(0.01 0.5)

for sel in "${sels[@]}"
do
    for i in $(seq 2 $cols)
    do
        python generate_benchmarks.py $i $cols > generated.weld;
        ./gen -n $nitems -c $cols -m $i -s $sel;
    done > dynamic_${sel}.tsv
done
