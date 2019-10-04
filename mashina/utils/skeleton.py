import os
from glob import glob
from jinja2 import Template, Environment, FileSystemLoader


def generate_project_folder(project_name):
    src_path = os.path.join(os.path.dirname(__file__), 'templates/psql_project')
    env = Environment(loader=FileSystemLoader(src_path))
    hidden_files = [src_path + '/api/.dockerignore']

    for f in glob(src_path + '/**', recursive=True) + hidden_files:
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


def generate_app_folder(singular, plural, package):
    src_path = os.path.join(os.path.dirname(__file__), 'templates/app')
    env = Environment(loader=FileSystemLoader(src_path))

    dst_path = os.path.join(*package.split('.'), plural)
    os.makedirs(dst_path)

    for f in glob(src_path + '/**', recursive=True):
        if os.path.isfile(f):
            _file = os.path.relpath(f, src_path)
            template = env.get_template(_file)
            file_content = template.render(
                singular=singular,
                singular_capitalized=singular.capitalize(),
                plural=plural,
                package=package
            )
            if _file.endswith('.tpl'):
                _file = _file[:-4]
            with open(os.path.join(dst_path, _file), 'w') as fh:
                fh.write(file_content)
                fh.write('\n')
