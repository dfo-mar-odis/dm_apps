## Repository for the DFO Science DM Apps Website (formally Gulf Science Data Management Website)

### Prerequisite to running the application
1. Install Python 3 (<https://www.python.org>), and make sure that Python is added to your PATH variable.
1. Working from your root projects directory (e.g., `~/my_projects`), create python virtual environment: `python -m venv dm_apps_venv`
1. Activate the virtual environment: `.\dm_apps_venv\Scripts\activate` (Windows) OR `source ./dm_apps_venv/bin/activate` (Linux)
1. Clone project: `git clone https://github.com/dfo-mar-odis/dm_apps`
1. navigate into the project director: `cd dm_apps`
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

1. For an Oracle Database Backend
    1. Run the command `python -m pip install cx_oracle --upgrade`
    1. In the directory `\dm_apps\dm_apps\` locate, copy and rename the file `default_conf.py` to `my_conf.py`
    1. Change `DATABASES = MYSQL_DATABASES` to `DATABASES = ORACLE_DATABASES`
    1. You may need to install the [Oracle Instant client](https://www.oracle.com/technetwork/database/database-technologies/instant-client/overview/index.html)
    
### Running the django development server
1. If you are using a local Sqlite database (i.e. this is the default configuration), 
be sure to run migrations before you get started: `python manage.py migrate`.
1. Change directory to the root `dm_apps` folder (if not already there) and run the development server: `python manage.py runserver`

### Collaborative workflow
1. If you are reading this, your contributions and collaborations are welcomed :)
1. Please do your work locally and make sure to pull regularly from `origin/master`
1. When ready to merge your work, please be sure to run the projects unit tests before creating your merge request
    1. if you are using windows, you can run the suite of test using the following batch file: `run_tests_in_windows.txt`
1. Please do not create a merge request that has conflicts with the master branch, unless you specifically need help with dealing with any conflicting code.
    1. in the case of the latter, please be sure to properly assign your merge request and add the appropriate comments
