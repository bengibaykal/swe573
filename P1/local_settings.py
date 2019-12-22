import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME' : 'community4',
        'USER' : 'postgres',
        'PASSWORD' : 'Berlin1992!',
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}

DEBUG = True