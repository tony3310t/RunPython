#!e:\runpython\runpython\env\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'yahoo-finance==1.4.0','console_scripts','yahoo-finance'
__requires__ = 'yahoo-finance==1.4.0'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('yahoo-finance==1.4.0', 'console_scripts', 'yahoo-finance')()
    )
