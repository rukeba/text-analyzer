pushd %~dp0

if not exist venv: virtualenv venv

call venv\scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
python manage.py migrate

pushd fronend
yarn install
yarn build
popd

popd