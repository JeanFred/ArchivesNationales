#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = []
requires = ['MassUploadLibrary']
dependency_links = ["https://github.com/JeanFred/MassUploadLibrary/archive/master.tar.gz#egg=MassUploadLibrary"]
scripts  = []

setup(
    name         = 'ArchivesNationales',
    version      = '0.1',
    description  = 'Managing the Archives Nationales metadata conversion.',
    author       = 'Jean-Frederic',
    author_email = 'JeanFred@github',
    url          = 'http://github.com.org/JeanFred/ArchivesNationales',
    packages         = packages,
    install_requires = requires,
    dependency_links = dependency_links,
    )
