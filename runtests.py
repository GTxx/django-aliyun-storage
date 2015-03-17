#! /usr/bin/env python
import os


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    os.system('django-admin.py test --settings=settings')
