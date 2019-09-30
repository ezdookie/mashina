import mashina
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mashina',
    version=mashina.__version__,
    scripts=['bin/mashina-admin.py'],
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True
)
