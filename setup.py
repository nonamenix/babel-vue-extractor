"""A setuptools based setup module for babel-angular-gettext
Based on:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='babel-vue-extractor',
    version='0.1.7',
    description='A plugin for babel to work with vue.js templates',
    long_description=read('README.rst'),
    url='https://github.com/nonamenix/babel-vue-extractor',
    author='Danil Ivanov',
    author_email='nonamenix@gmail.com',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 1.3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Internationalization',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='vuejs babel',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['babel', 'six'],
    extras_require={
        'dev': ['check-manifest', 'nose'],
        'test': ['coverage'],
    },
    package_data={},
    data_files=[],
)
