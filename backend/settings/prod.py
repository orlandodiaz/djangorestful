from .base import *

import dj_database_url

DEBUG = True

# Add your domain to allowed hosts:
ALLOWED_HOSTS = [
    'orr-redux-auth-demo.herokuapp.com',
]

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600, ssl_require=True)

# Static FILES
STATIC_ROOT = os.path.join(BASE_DIR, 'frontend/build/static')


MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]