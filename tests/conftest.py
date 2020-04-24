import os
import shutil
import subprocess
import sys
from importlib import import_module

import pytest
from click.testing import CliRunner
from falcon import testing

from mashina.utils.admin import startproject


@pytest.fixture(scope='module')
def project():
    name = 'testingproject'
    runner = CliRunner()
    result = runner.invoke(startproject, [name])
    assert result.exit_code == 0

    subprocess.call(['pip', 'install', '-e', '%s/api' % name])
    sys.path.append('%s/api' % name)
    mod = import_module(name)
    assert mod.__version__ == '1.0'

    yield name
    shutil.rmtree(name)


@pytest.fixture(scope='module')
def setup_db(project):
    os.environ['MASHINA_SETTINGS_MODULE'] = '%s.config.settings' % project
    from mashina.commands import makemigration, migrate
    runner = CliRunner()

    result = runner.invoke(makemigration, ['initial'])
    assert result.exit_code == 0

    result = runner.invoke((migrate))
    assert result.exit_code == 0

    yield 1
    os.remove('testing.db')


@pytest.fixture(scope='module')
def wsgi_app(project):
    proc = subprocess.Popen(['gunicorn', '--reload', '%s.wsgi' % project, '--bind', ':9066'])
    yield proc
    proc.kill()


@pytest.fixture(scope='module')
def falcon_client(project, setup_db):
    os.environ['MASHINA_SETTINGS_MODULE'] = '%s.config.settings' % project
    os.environ['TESTING_MODE'] = '1'
    from mashina.app import App
    return testing.TestClient(app=App())
