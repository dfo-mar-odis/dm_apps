#!c:\users\thompsone\documents\github\dm_apps\dm_apps_venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'xhtml2pdf==0.2.3','console_scripts','xhtml2pdf'
__requires__ = 'xhtml2pdf==0.2.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('xhtml2pdf==0.2.3', 'console_scripts', 'xhtml2pdf')()
    )
