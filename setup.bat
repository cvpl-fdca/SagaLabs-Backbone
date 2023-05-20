@echo off

python -m venv venv
.\venv\Scripts\activate
set PYTHONPATH=%PYTHONPATH%;%cd%\src
pip install -r requirements.txt
$env:FLASK_APP="src/main.py"
