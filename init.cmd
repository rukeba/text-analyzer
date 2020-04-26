if not exist venv: virtualenv venv

call venv\scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
python manage.py migrate
