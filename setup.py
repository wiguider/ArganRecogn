# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='frbs',
    version='0.1.0',
    description='Face Recognition Using Convolutional Neural Nets',
    long_description=readme,
    author='Ilyas Chaoua, Walid Iguider',
    author_email='ilyas.chaoua@gmail.com, walid.iguider@gmail.com',
    url='https://github.com/rivas/frbs',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
