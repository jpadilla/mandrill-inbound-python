# -*- coding: utf-8 -*

import os
from setuptools import setup, find_packages

readme_md = os.path.join(os.path.dirname(__file__), 'README.md')

try:
    import pandoc
    pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'
    doc = pandoc.Document()
    doc.markdown = open(readme_md).read()
    long_description = doc.rst
except (IOError, ImportError):
    long_description = open(readme_md).read()

setup(
    name='python-mandrill-inbound',
    version='0.0.4',
    packages=find_packages(),
    author='José Padilla',
    author_email='jpadilla@webapplicate.com',
    description='Python wrapper for Mandrill Inbound',
    long_description=long_description,
    license='MIT License',
    url='https://github.com/jpadilla/mandrill-inbound-python',
    download_url='https://github.com/jpadilla/mandrill-inbound-python/tarball/master',
)
