import click
from mashina.utils.skeleton import generate_app_folder
from mashina.models.seeds import do_seed


@click.group()
def main():
    pass

@main.command()
@click.argument('singular')
@click.argument('plural')
def generate(singular, plural):
    generate_app_folder(['controllers', 'models', 'routes', 'schemas'], singular, plural)
    click.echo('App successfully created...!')

@main.command()
@click.argument('file_name')
def seed(file_name):
    do_seed(file_name)
