import click
from mashina.utils.skeleton import generate_app_folder
from mashina.models.seeds import do_seed


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
def generate(name):
    data = {'name': name, 'name_slug': name.lower()}
    generate_app_folder(['controllers', 'models', 'routes', 'schemas'], data)
    click.echo('App %s successfully created!' % name)


@main.command()
@click.argument('file_name')
def seed(file_name):
    do_seed(file_name)
