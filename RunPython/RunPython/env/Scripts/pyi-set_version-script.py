#!e:\runpython\runpython\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.2.1','console_scripts','pyi-set_version'
__requires__ = 'PyInstaller==3.2.1'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('PyInstaller==3.2.1', 'console_scripts', 'pyi-set_version')()
    )
