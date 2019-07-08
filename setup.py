from setuptools import setup, find_packages

setup(
    name='mashina',
    version='1.0.0',
    install_requires=[
        'falcon==2.0.0',
        'SQLAlchemy==1.3.5',
        'alembic==1.0.11',
        'click==7.0',
        'marshmallow==2.19.5',
        'marshmallow-sqlalchemy==0.17.0'
    ],
    packages=find_packages(),
    include_package_data=True
)
