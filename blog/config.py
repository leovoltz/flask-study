import os
from dynaconf import FlaskDynaconf


HERE = os.path.dirname(os.path.adspath(__file__))


def configure(app):
    FlaskDynaconf(app, extensions_list="EXTENSIONS", root_path=HERE)
