import importlib
from os.path import dirname, basename, isfile
import glob


def __list_all_modules():
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [importlib.import_module("adapters.ip." + basename(f)[:-3]) for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]
    return all_modules


adapters = {
    module.server: module.IpWhois for module in __list_all_modules() if module.server
}
