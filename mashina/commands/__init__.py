import click
from mashina.utils.skeleton import generate_file_from_tpl
from mashina.models.seeds import do_seed


@click.group()
def main():
    pass

@main.command()
@click.argument('name')
def generate(name):
    data = {'name': name, 'name_slug': name.lower()}

    # Generating controller file...
    generate_file_from_tpl('controller.tpl', 'controllers/{}.py'.format(data['name_slug']), data)

    # Generating model file...
    generate_file_from_tpl('model.tpl', 'models/{}.py'.format(data['name_slug']), data)

    # Adding new model..
    models_file = open('models/__init__.py', 'a')
    models_file.write('from .{name_slug} import {name}\n'.format(**data))
    models_file.close()

@main.command()
@click.argument('file_name')
def seed(file_name):
    do_seed(file_name)
