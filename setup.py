# -*- coding: utf-8 -*-

import os
import codecs

from setuptools import setup, find_packages

VERSION = "0.1.0"
HERE = os.path.dirname(__file__)


def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(HERE, f), 'r').read()
    return content


setup(
    name='spicey',
    url='https://github.com/CrowdRescueHQ/media-slack-scraper',
    author='GrowdRescueHQ',
    description='A bot that scrapes social media into slack.',
    version=VERSION,
    long_description=read('README.rst'),
    platforms=['any'],
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.rst'],
        'scraper': ['*'],
    },
    install_requires=read("requirements.txt"),
)
