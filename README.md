# swe573
Bogazici University SWE 573 Project

Installation:

```
git clone https://github.com/ChristianKreuzberger/django-rest-imageupload-example.git
cd django-rest-imageupload-example
mkdir uploaded_media # create a directory for the uploaded images
virtualenv -p python3.4 venv # Note: python3.5 should also work
source venv/bin/activate
pip install -r requirements.txt
cd django_rest_imageupload_backend
python manage.py migrate
python manage.py runserver # starts the server 
```
