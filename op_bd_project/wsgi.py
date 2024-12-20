"""
WSGI config for op_bd_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import webbrowser
from multiprocessing import Process

from updater.main import Parser
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'op_bd_project.settings')

thread = Process(target=Parser)
thread.start()

webbrowser.open("http://127.0.0.1:8000/")

application = get_wsgi_application()
