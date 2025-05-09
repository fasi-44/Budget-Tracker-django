"""
WSGI config for budget project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# settings_module = 'budget.deployments_settings' if 'RENDER_EXTERNAL_HOST' in os.environ else 'budget.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget.deployments_settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget.settings')

application = get_wsgi_application()
