import click
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command
from mashina.utils.skeleton import generate_app_folder
from mashina.models.seeds import do_seed
from mashina.config import settings


@click.group()
def main():
    pass


@main.command()
@click.argument('singular')
@click.argument('plural')
@click.argument('package')
def createapp(singular, plural, package):
    generate_app_folder(singular, plural, package)
    click.echo('App successfully created...!')


@main.command()
@click.argument('file_name')
def seed(file_name):
    do_seed(file_name)


@main.command()
def migrate():
    alembic_cfg = AlembicConfig(settings.ALEMBIC_CFG_PATH)
    alembic_command.upgrade(alembic_cfg, "head")


@main.command()
@click.option('--message')
def makemigrations(message):
    alembic_cfg = AlembicConfig(settings.ALEMBIC_CFG_PATH)
    alembic_command.revision(config=alembic_cfg, message=message, autogenerate=True)
