#!e:\runpython\runpython\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'future==0.16.0','console_scripts','futurize'
__requires__ = 'future==0.16.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('future==0.16.0', 'console_scripts', 'futurize')()
    )
