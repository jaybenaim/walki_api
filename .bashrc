alias act="pyenv activate walki_api"
alias deact="pyenv deactivate"
alias pys="python3 manage.py runserver"
alias pym="python3 manage.py"
alias loadDB="python3 manage.py makemigrations;python3 manage.py migrate;python3 manage.py load data main_app/fixtures/db.json"
source .env

# Activate virtual env
eval "act"
