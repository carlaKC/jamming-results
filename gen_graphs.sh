#!/bin/bash

for DIR in ln50*/; do
    if [[ -d "$DIR" ]]; then
        python3 reputation_graph.py "${DIR}22_03d607.csv" 335351046537216
    fi
done
