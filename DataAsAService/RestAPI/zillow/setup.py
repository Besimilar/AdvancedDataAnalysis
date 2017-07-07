# @author Hongwei
from setuptools import setup

setup(
    name='zillow',
    packages=['zillow'],
    include_package_data=True,
    install_requires=[
        'flask',
        'boto3',
        'geopy',
        'pandas'
    ],
)

