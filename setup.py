from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mashina',
    version='1.0.0',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True
)
