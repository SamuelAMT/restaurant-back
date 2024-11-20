"""
WSGI config for bookabite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv(dotenv_path='.env.local')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookabite.settings")

application = get_wsgi_application()

app = application
