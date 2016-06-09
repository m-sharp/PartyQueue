from pathlib import Path
from setuptools import find_packages, setup


project_path = Path(__file__).parent

install_requires = [
    'gmusicapi',
    'slackclient'
]

packages = ['party_queue.' + pkg for pkg in find_packages('party_queue', exclude=['tests', 'tests.*'])]

setup(
    name='party-queue',
    version='0.0.1',
    author='Mike Harp',
    author_email='msharp185@gmail.com',
    description='Party Queue Slack Integration for Google Play Music',
    packages=packages,
    install_requires=install_requires,
)
