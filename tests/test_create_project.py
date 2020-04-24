import os
import subprocess

from click.testing import CliRunner


def test_create_app(project):
    os.environ['MASHINA_SETTINGS_MODULE'] = '%s.config.settings' % project
    from mashina.commands import createapp
    runner = CliRunner()
    result = runner.invoke(createapp, ['animal', 'animals'])
    assert result.exit_code == 0


def test_run_server(wsgi_app):
    try:
        wsgi_app.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    finally:
        assert wsgi_app.returncode is None
