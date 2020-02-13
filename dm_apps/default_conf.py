# INSTRUCTIONS:  #
##################
# please refer to the README and the project wiki for the most up-to-update information.
# Duplicate this file and rename it to my_conf.py
# The 'my_conf.py' file is in the .gitignore
# create a file called prod.cnf in the root project dir to specify connection to production db server
# The 'prod.cnf' file is also in the .gitignore
# It is recommended to leave this file unmodified unless you are making improvements

import os
from decouple import config
from .utils import is_connection_available

# DO NOT INTERACT WITH THESE VARIABLES HERE
########################################################################
FORCE_DEV_DB = False
DEV_DB_NAME = None
DEV_DB_HOST = None
USING_LOCAL_DB = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
########################################################################

# Should Microsoft Azure AD be used for authentication? By default, if a file called `oauth_settings.yml' is in the root dir, azure aad will be turned on
# this is a manual override. Uncomment to turn off AAD regardless of the presence of the above mentioned file.
# AZURE_AD = False

# Should the ticketing app be displayed on the main index page?
SHOW_TICKETING_APP = True

# Should DEBUG mode be turned on? Uncomment the line below to turn on debugging
# DEBUG = True

# To add any custom hosts to this application's list of allowed hosts, provide them here
ALLOWED_HOSTS_TO_ADD = []

# If the line below is uncommented, you will connect to the dev database even if production database strings are present
# FORCE_DEV_DB = True

# check to see if the which databases are available:
IS_PROD_DB_AVAILABLE = is_connection_available("PROD")
IS_DEV_DB_AVAILABLE = is_connection_available("DEV")

# if a database is listed and we are not forcing dev mode...
if IS_PROD_DB_AVAILABLE and not FORCE_DEV_DB:
    USING_PRODUCTION_DB = True
# otherwise, check to see if we can connect to a dev db
elif IS_DEV_DB_AVAILABLE:
    # There are 3 scenarios: 1) there is no PROD_DB_NAME in the .env file; 2) FORCE_DEV_DB is set to True; or 3) both
    if IS_PROD_DB_AVAILABLE:
        print("production connection string is present however running dev mode since FORCE_DEV_MODE setting is set to True")
    # this variable is used in base.html to indicate which database you are connected to
    USING_PRODUCTION_DB = False
    # if we have a connection to dev, get the names of db and host to pass in as context processors
    DEV_DB_NAME = config('DEV_DB_NAME')
    DEV_DB_HOST = config('DEV_DB_HOST')
else:
    USING_PRODUCTION_DB = False
    USING_LOCAL_DB = True

# add new applications to this dictionary; grey out any app you do not want
# the dict key should be the actual name of the app
# if there is a verbose name, it should be the key value, otherwise None
APP_DICT = {
    'inventory': 'Metadata Inventory',
    'grais': 'grAIS',
    'oceanography': 'Oceanography',
    'herring': 'HerMorrhage',
    'camp': 'CAMP db',
    'meq': 'Marine environmental quality (MEQ)',
    'diets': 'Marine diets',
    'projects': 'Science project planning',
    'ihub': 'iHub',  # dependency on masterlist
    'scifi': 'SciFi',
    'masterlist': 'Masterlist',
    'shares': 'Gulf Shares',
    'travel': 'Travel Management System',
    'sar_search': "SAR Search",
    'spot': 'Grants & Contributions (Spot)',  # dependency on masterlist, sar_search
    'ios2': 'Instruments',
    'staff': "Staff Planning Tool",
    'publications': "Project Publications Inventory",
    'trapnet': "TrapNet",
    'whalesdb': "Whale Equipment Deployment Inventory",
}

MY_INSTALLED_APPS = [app for app in APP_DICT]

# Specify your database connection details
if USING_LOCAL_DB:
    print("Database connection information missing from environmental variables. Using local Sqlite db")
    my_default_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
else:
    DB_CONNECTION_PREFIX = "PROD" if USING_PRODUCTION_DB else "DEV"
    my_default_db = {
        'ENGINE': 'django.db.backends.mysql',
        'TIME_ZONE': 'America/Halifax',
        'OPTIONS': {
            'host': config(DB_CONNECTION_PREFIX + '_DB_HOST'),
            'port': config(DB_CONNECTION_PREFIX + '_DB_PORT', cast=int),
            'database': config(DB_CONNECTION_PREFIX + '_DB_NAME'),
            'user': config(DB_CONNECTION_PREFIX + '_DB_USER'),
            'password': config(DB_CONNECTION_PREFIX + '_DB_PASSWORD'),
            'init_command': 'SET default_storage_engine=INNODB',
        }}

DATABASES = {
    'default': my_default_db,
}
