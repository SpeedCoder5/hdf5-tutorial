import importlib
from pathlib import Path
import re
import sys

REQUIRED_PYTHON = "python3"


def main():
    system_major = sys.version_info.major
    print("Using interpreter: " + sys.executable)
    # check to see if the venv is running https://stackoverflow.com/a/58026969
    if sys.prefix == sys.base_prefix:
        raise ModuleNotFoundError("venv not activated. " +
        "Please first activate venv for project via `source activate`.\n" +
        "To debug, after activating venv, use `which python` to get interpreter path " + 
        "to add VS code via https://code.visualstudio.com/docs/python/environments.")
    
    # print python version
    print(f'python version  == {sys.version}')

    contents = Path('requirements.txt').read_text()
    overrides = {
        '-e .':'',
    }
    libraries = [line for line in contents.split('\n') if line and not line.startswith('#')]
    for i,library_name in enumerate(libraries):
        ln = str(re.search('^[^~<>=#\r\n]*', library_name)[0]).strip() # ignore end of line comments and version strings
        if ln != library_name:
            library_name = ln
            libraries[i] = library_name
        if library_name in overrides:
            libraries[i]=overrides[library_name]
    print(libraries)
    for library_name in libraries:
        if library_name:
            print(f'importing {library_name}', end=':')
            module = importlib.import_module(library_name)        
            version = getattr(module, '__version__', None)        
            if version:
                print(f"{version}")
            else:
                print("no __version__")
    
    print(">>> Development environment passes all tests!")

if __name__ == '__main__':
    main()
