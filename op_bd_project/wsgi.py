"""
WSGI config for op_bd_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from multiprocessing import Process

from updater.main import Parser
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'op_bd_project.settings')

thread = Process(target=Parser)
thread.start()

application = get_wsgi_application()
