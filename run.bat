@echo off

if not exist "venv\" (
    echo No env found
    echo Run setup.bat
    exit /b 1
)

call venv\Scripts\activate.bat
python pca_analysis.py data/metrics.csv