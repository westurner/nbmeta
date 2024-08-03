#!/usr/bin/env python

"""nbmeta/setup.py script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'jinja2',
    'dominate',
    'rdflib',
    'pygments',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Wes Turner",
    author_email='wes@wrd.nu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description=(
        "RDF, JSON-LD, YAML-LD metadata support for Jupyter Notebook, Sphinx"),
    entry_points={
        'console_scripts': [
            'nbmeta=nbmeta.cli:main',
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nbmeta',
    name='nbmeta',
    packages=find_packages(include=['nbmeta', 'nbmeta.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/westurner/nbmeta',
    version='0.1.0',
    zip_safe=False,
)
