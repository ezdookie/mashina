import os
import sys
from glob import glob

from jinja2 import Environment, FileSystemLoader


def generate_project_folder(project_name):
    src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'psql_project')
    env = Environment(loader=FileSystemLoader(src_path))
    hidden_files = [src_path + h_file for h_file in ('/.gitignore', '/api/.dockerignore')]

    for f in glob(os.path.join(src_path, '**'), recursive=True) + hidden_files:
        _file = os.path.relpath(f, src_path)
        _file_replaced = _file.replace('project_name', project_name)
        if os.path.isdir(f):
            os.makedirs(os.path.join(project_name, _file_replaced))
        elif os.path.isfile(f):
            template = env.get_template(_file)
            file_content = template.render(project_name=project_name)
            if _file_replaced.endswith('.tpl'):
                _file_replaced = _file_replaced[:-4]
            with open(os.path.join(project_name, _file_replaced), 'w') as fh:
                fh.write(file_content)
                fh.write('\n')

    generate_app_folder('todo', 'todos', [project_name, 'api', project_name])


def generate_app_folder(singular, plural, path=None):
    src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'app')
    env = Environment(loader=FileSystemLoader(src_path))

    _path = os.path.dirname(sys.argv[0]) if not path else os.path.join(*path)
    apps_path = os.path.join(_path, 'apps')

    app_package = '%s.apps.%s' % (os.path.basename(_path), plural)
    dst_path = os.path.join(apps_path, plural)
    os.makedirs(dst_path, exist_ok=True)

    for f in glob(os.path.join(src_path, '**'), recursive=True):
        if os.path.isfile(f):
            _file = os.path.relpath(f, src_path)
            template = env.get_template(_file)
            file_content = template.render(
                singular=singular,
                singular_capitalized=singular.capitalize(),
                plural=plural,
                app_package=app_package
            )
            if _file.endswith('.tpl'):
                _file = _file[:-4]
            with open(os.path.join(dst_path, _file), 'w') as fh:
                fh.write(file_content)
                fh.write('\n')
