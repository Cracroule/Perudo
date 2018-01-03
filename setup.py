__author__ = 'rpil'

from setuptools import setup, find_packages
from distutils.core import setup

setup(
    version='0.0.0.1',
    name='perudo',
    description='personal project about perudo contest',
    license='rpil',
    package_dir={},
    packages=['perudo'],
    scripts=['scripts/tournament.py'],
    install_requires=[]
)
