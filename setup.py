#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="django-aliyun-oss-storage",
    version='0.1',
    packages=find_packages(),
    author="GTxx",
    author_email="xiongxiong1986@gmail.com",
    url="https://github.com/GTxx/",
    license="MIT",
    description='django storage in aliyun oss',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
    install_requires=[],
)
