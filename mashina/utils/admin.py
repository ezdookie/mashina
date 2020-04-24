import click

from mashina.utils.generator import generate_project_folder


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
def startproject(name):
    generate_project_folder(name)
    click.secho('Project successfully created!', fg='green')
