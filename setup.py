#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from distutils.core import Command
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=('calaccess_scraped',),
            MIDDLEWARE_CLASSES=()
        )
        from django.core.management import call_command
        import django
        django.setup()
        call_command('test', 'calaccess_scraped')


setup(
    name='django-calaccess-scraped-data',
    version='3.4.0',
    author='California Civic Data Coalition',
    author_email='b@palewi.re',
    url='https://www.californiacivicdata.org',
    description='A Django app to scrape campaign-finance data from '
                'the California Secretary of State’s CAL-ACCESS website',
    long_description=read('README.rst'),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including static files
    cmdclass={'test': TestCommand},
    install_requires=(
        'django>=3.2',
        'pytz',
        'bs4',
        'selenium',
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License'
    ],
    project_urls={
        'Project': 'https://www.californiacivicdata.org/',
        'Funding': 'https://www.californiacivicdata.org/about/',
        'Source': 'https://github.com/california-civic-data-coalition/django-calaccess-scraped-data',
        'Testing': 'https://github.com/california-civic-data-coalition/django-calaccess-scraped-data/actions/workflows/tests.yaml',
        'Tracker': 'https://github.com/california-civic-data-coalition/django-calaccess-scraped-data/issues'
    },
)
