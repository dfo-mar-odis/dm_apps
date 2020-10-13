# DM Apps

## Basic Setup

### Prerequisite to running the application
1. Install Python 3 (<https://www.python.org>), and make sure that Python is added to your PATH variable.
1. Working from your root projects directory (e.g., `~/my_projects`), create python virtual environment: `python -m venv dm_apps_venv`
1. Activate the virtual environment: `.\dm_apps_venv\Scripts\activate` (Windows) OR `source ./dm_apps_venv/bin/activate` (Linux)
1. Clone project: `git clone https://github.com/dfo-mar-odis/dm_apps`
1. navigate into the project directory: `cd dm_apps`
1. Install the Python packages required by the DM APPS application: `pip install -r requirements.txt`
    - If you get an error when installing this, you will have to open the requirements.txt and comment out the lines for `mysqlclient` and `shapely`.
    - Rerun the package installation line above
    - You will have to download a precompiled version of `mysqlclient` and `shapely`. The binary versions of these packages are available here:
        - [mysqlclient](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient). Be sure to select the file that matches your system configuration.
        - [shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely). Be sure to select the file that matches your system configuration.
    - So, for example, if your a running python 3.6 on an AMD64 processor, you would download the file called 'mysqlclient‑1.x.x‑cp36‑cp36m‑win_amd64.whl.'.
    If you do not select the correct file version, it will not work. 
    - Once you have downloaded the files, you can install them as follows:
        - `pip install /path/to/local/file/mysqlclient‑1.x.x‑cp36‑cp36m‑win_amd64.whl`
        - `pip install /path/to/local/file/shapely‑1.x.x‑cp36‑cp36m‑win_amd64.whl`
    - ***Do not forget to uncomment the two lines from the requirements.txt file***

### Running the django development server
1. If you are using a local Sqlite database (i.e. this is the default configuration), 
be sure to run migrations before you get started: `python manage.py migrate`.
1. Change directory to the root `dm_apps` folder (if not already there) and run the development server: `python manage.py runserver`



## Getting Started with this Project for Development
Before proceeding any further, make sure you have completed the steps outlined above.

### Create a superuser for local development
1. to create a superuser, use the following command `python manage.py createsuperuser`
1. please note that all usernames in this project should be an email address. Otherwise you will have trouble logging in through the login page.

### Import fixtures
1. To import some of the basic reference tables, please use the follow command in windows: `import_fixtures.bat`
NOTE: For linux users, sorry, we don't have a script yet. You will have to import the fixtures manually using `python manage.py loaddata my_fixture.json`. 

### Local configuration file
We are attempting to build this project in a modular fashion that will allow flexible implementation of the application.
The idea is that there might be multiple instances of this app in production and each instance will want to have its own custom settings, for example, 
which database it is connecting to, which apps are connected, allowed hostnames, etc... 

Without any customizations, the site will connect to a local sqlite3 database. This is an ideal, fast and simple option for local development. 
After running the `migrate` command an empty sqlite database will be created in the project root called `db.sqlite3`. 
This file is already in the .gitignore file. 

### Static files
Static files are not stored in the git repository, they can be pushed to the static file server using `python manage.py findstatic` and downloaded to a machine for local development using `python manage.py collectstatic`. If this step is skipped the "you are not using chrome" warning message will show and images will appear broken on the "127.0.0.1:8000/en" page

**The first step of customizing the site's configuration is by cloning the `.env_sample` file and renaming this copy to `.env`.** This file is also in the .gitignore.
This file has numerous switches and flags that can be used for customizing the application. The `.env_sample` file has a lot of annotation and the configuration 
settings should be fairly straight-forward. If you find any of them confusing, please open an issuein the `dmapps` repo. 

Most types of customizations can be done through the `.env` file. However, changes made to which apps are switched on/off or which type of database backend you want to 
use must be done in a separate file. **To do these types of customization, make a copy of the file called `./dm_apps/default_conf.py` to `./dm_apps/my_conf.py`.**
The latter file is in the .gitignore therefore none of the changes made will be recorded to the repo. If the `my_conf.py` file is present when the 
application boots up, the `default_conf.py` file will be ignored and the application will look to the `my_conf` file. At this point you would be free
to make any changes you like to the `my_conf`. 

If you are connecting to a mysql database, you do not need to make a custom `my_conf`. Instead simply provide the database credentials in the `.env`. 

**Important:** You should not be making changes to the `.env_sample` and/or `default_conf.py` unless these are changes that are meant to be 
persist in the repository for all users. For example, if you were working on a new app, you would eventually have to modify the `default_conf`.   

### Connecting existing apps to an instance
Apps can be easily connected and disconnected from an instance of the application. To do so, you simply comment / uncomment
the app of interest in the app dictionary: `my_conf.APP_DICT`. Each connected app should have a card display on the site's main index page.


## Collaborative workflow
1. If you are reading this, your contributions and collaborations are welcomed :)
1. Please do your work locally and make sure to pull regularly from `origin/master`
1. When ready to merge your work, please be sure to run the project's unit tests before creating your merge request
    1. if you are using windows, you can run the suite of test using the following batch file: `run_tests_in_windows.txt`
1. Please do not create a merge request that has conflicts with the master branch, unless you specifically need help with dealing with any conflicting code.
    1. in the case of the latter, please be sure to properly assign your merge request and add the appropriate comments
