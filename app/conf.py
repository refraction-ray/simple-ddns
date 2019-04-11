import os
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_config(name=None, override=None, path=None):
    if not path:
        dirpath = os.path.dirname(os.path.abspath(__file__))
    else:
        dirpath = path
    if not name:
        name = "config.yaml"
    with open(os.path.join(dirpath, name), 'r') as conffile:
        conf = load(conffile, Loader=Loader)
    if override:
        try:
            with open(os.path.join(dirpath, override), "r") as conffile:
                confo = load(conffile, Loader=Loader)
            conf.update(confo)
        except FileNotFoundError:
            pass
    return conf


confpath = os.environ.get("OVERRIDE_CONF", None) or "config_override.yaml"

conf = get_config(override=confpath)
