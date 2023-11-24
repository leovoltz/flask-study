from setuptools import setup


setup(
    name="blog-flask",
    version="0.1.0",
    packages=["blog"],
    install_requires=[
        "flask",
        "flask-pymongo",
        "dynaconf",
        "python-slugify",
        "flask-bootstrap",
        "mistune",
        "flask-simplelogin",
        "flask-admin",
    ],
)
