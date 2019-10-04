import os
os.environ['MASHINA_SETTINGS_MODULE'] = '{{ project_name }}.config.settings'
from mashina.app import App

application = App()
