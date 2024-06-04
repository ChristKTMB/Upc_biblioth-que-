from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Configure les variables d'environnement pour Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RH.settings')

# Créez une instance de Celery et configurez-la
app = Celery('RH')

# Charge la configuration à partir des paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Recherche automatiquement les tâches dans toutes les applications installées
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
