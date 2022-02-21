#!/usr/bin/env python3
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))


setup(
    name='aiogram_dialog_extras',
    description='A pack of extras for better use of the aiogram-dialog framework',
    version='0.1.0',
    url='https://github.com/SamWarden/aiogram_dialog_extras',
    author='Aivan Warden',
    author_email='SamWardenSad@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(include=['aiogram_dialog_extras', 'aiogram_dialog_extras.*']),
    install_requires=[
        'aiogram_dialog>=1.2.0,<2',
    ],
    python_requires=">=3.9",
)
