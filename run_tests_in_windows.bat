:: testing for shared_models app
python manage.py test shared_models.test --keepdb -v 0

:: testing for projects app
python manage.py test projects.test --keepdb -v 0

:: testing for travel app
python manage.py test travel.test --keepdb -v 0

:: run tests for whalesdb app
python manage.py test whalesdb.test --keepdb -v 0

:: run tests for inventory app
python manage.py test inventory.test --keepdb -v 0

:: run tests for shiny
python manage.py test shiny.test --keepdb -v 0