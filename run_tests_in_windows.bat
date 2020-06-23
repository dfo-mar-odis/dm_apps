:: testing for shared_models app
python manage.py test shared_models.test --keepdb

:: testing for projects app
python manage.py test projects.test --keepdb

:: testing for travel app
python manage.py test travel.test --keepdb

:: run tests for whalesdb app
python manage.py test whalesdb.test --keepdb

:: run tests for inventory app
python manage.py test inventory.test --keepdb

:: run tests for shiny
python manage.py test shiny.test --keepdb