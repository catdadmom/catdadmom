"""
CatDadMom
=========

Feral cat protection community.

"""
from setuptools import setup


setup(
    name='CatDadMom',
    version='dev',
    url='https://github.com/catdadmom/web',
    author='CatDadMom',
    description='Feral cat protection community',
    long_description=__doc__,
    zip_safe=False,
    packages=['catdadmom', 'catdadmom.web'],
    package_data={
        'catdadmom.web': ['templates/*.*', 'static/*.*']
    },
    install_requires=[
        'Flask',
        'SQLAlchemy',
        'bcrypt'
    ]
)
