#!/bin/bash

echo "PCA env setup"

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

mkdir -p data

echo "Setup complete"
echo "Env activation:"
echo "source venv/bin/activate"
echo "Analysis run:"
echo "python pca_analysis.py metrics.csv"