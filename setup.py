from setuptools import setup

__version__ = "0.0.1"
__author__ = "Felix Breuer"

requirements = [
    "selenium",
    "typing",
    "schedule",
    "fake_useragent",
    "chromedriver-py==2.38",
]

description = "Travian Kingdoms automation bot."

setup(
    name="king-bot",
    version=__version__,
    author=__author__,
    author_email="f.breuer94@gmail.com",
    url="https://github.com/breuerfelix/king-bot",
    description=description,
    install_requires=requirements,
    include_package_data=True,
)
