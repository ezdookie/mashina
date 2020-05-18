import os

import pytest
from click.testing import CliRunner
from falcon import testing


@pytest.fixture(scope='module')
def setup_db():
    os.environ['MASHINA_SETTINGS_MODULE'] = '{{ project_name }}.config.settings'
    from mashina.commands import migrate
    runner = CliRunner()

    result = runner.invoke(migrate)
    assert result.exit_code == 0

    yield 1
    os.remove('testing.db')


@pytest.fixture(scope='module')
def falcon_client(setup_db):
    os.environ['TESTING_MODE'] = '1'
    from mashina.app import App
    return testing.TestClient(app=App())
