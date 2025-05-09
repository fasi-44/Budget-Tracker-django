"""
ASGI config for budget project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# settings_module = 'budget.deployments_settings' if 'RENDER_EXTERNAL_HOST' in os.environ else 'budget.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget.deployments_settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget.settings')

application = get_asgi_application()
