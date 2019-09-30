import os
import pytest
from falcon import testing


@pytest.fixture(scope='module')
def client():
    os.environ['MASHINA_SETTINGS_MODULE'] = '{{ project_name }}.config.settings'
    os.environ['TESTING_MODE'] = 'true'
    from mashina.app import App
    return testing.TestClient(app=App())
