@echo off
echo PCA env setup

python -m venv venv
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist "data" mkdir data

echo Setup complete
echo Env activation:
echo source venv/bin/activate
echo Analysis run:
echo python pca_analysis.py metrics.csv