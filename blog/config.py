from dynaconf import FlaskDynaconf
from pathlib import Path


ROOT = Path(__file__).parent


def configure(app):
    FlaskDynaconf(app, extensions_list="EXTENSIONS", root_path=ROOT)
