python -m venv venv
.\venv\Scripts\activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pip install -r requirements.txt
export FLASK_APP=src/main.py
