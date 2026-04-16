#!/bin/bash

if [ ! -d "venv" ]; then
    echo "No env found"
    echo "Run ./setup.sh"
    exit 1
fi
source venv/bin/activate
python python pca_analysis.py data/metrics.csv