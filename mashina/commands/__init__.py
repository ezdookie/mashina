import click
from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig

from mashina.config import settings
from mashina.utils.generator import generate_app_folder
from mashina.utils.seeds import do_seed


@click.group()
def main():
    pass


@main.command()
@click.argument('singular')
@click.argument('plural')
def createapp(singular, plural):
    generate_app_folder(singular, plural)
    click.secho('App successfully created!', fg='green')


@main.command()
@click.argument('file_name')
def seed(file_name):
    do_seed(file_name)


@main.command()
def migrate():
    alembic_cfg = AlembicConfig(settings.ALEMBIC_CFG_PATH)
    alembic_command.upgrade(alembic_cfg, "head")


@main.command()
@click.argument('message')
def makemigration(message):
    alembic_cfg = AlembicConfig(settings.ALEMBIC_CFG_PATH)
    alembic_command.revision(config=alembic_cfg, message=message, autogenerate=True)
