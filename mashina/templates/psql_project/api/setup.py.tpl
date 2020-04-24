import {{ project_name }}
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='{{ project_name }}',
    version={{ project_name }}.__version__,
    install_requires=requirements,
    packages=find_packages()
)
