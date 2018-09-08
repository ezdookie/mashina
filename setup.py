from setuptools import setup, find_packages

setup(name='mashina',
    version='1.0.0',
    install_requires=[
        'falcon==1.4.1',
        'SQLAlchemy==1.2.10',
        'click==6.7',
        'marshmallow==2.15.4',
        'marshmallow-sqlalchemy==0.14.1'
    ],
    packages=find_packages()
)
