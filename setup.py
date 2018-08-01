from setuptools import setup

__version__ = '0.0.1'
__author__ = 'felix.scriptworld'

requirements = [
    'selenium',
    'typing',
    'schedule',
    'fake_useragent'
]

description = 'Travian Kingdoms automation bot.'

setup(
    name='king-bot',
    version=__version__,
    author=__author__,
    author_email='felix@scriptworld.net',
    url='https://github.com/scriptworld-git/king-bot',
    description=description,
    install_requires=requirements,
    include_package_data=True,
)
