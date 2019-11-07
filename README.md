# swe573
Bogazici University SWE 573 Project

Installation:

```
git clone https://github.com/bengibaykal/swe573.git
virtualenv -p python3.4 venv # Note: python3.5 should also work
. bin/activate
pip install -r requirements.txt
cd community
python manage.py migrate
python manage.py runserver # starts the server 
```
