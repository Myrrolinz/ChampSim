#!/bin/bash

mkdir -p $PWD/../traces
i=0
while read LINE
do
    wget -P $PWD/../traces -c http://hpca23.cse.tamu.edu/champsim-traces/speccpu/$LINE
done < lab_traces.txt
