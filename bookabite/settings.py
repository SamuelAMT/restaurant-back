import os
from pathlib import Path

from bookabite.config.settings import *

if os.getenv('VERCEL'):
    ALLOWED_HOSTS.append('.vercel.app')
    DEBUG = False
    
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    if 'DATABASE_URL' in os.environ:
        import dj_database_url
        DATABASES['default'] = dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )