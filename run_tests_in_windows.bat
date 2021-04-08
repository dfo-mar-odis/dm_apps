:: testing for shared_models app
python manage.py test -b shared_models.test --keepdb

:: testing for projects app
python manage.py test -b projects2.test --keepdb

:: testing for travel app
python manage.py test -b travel.test --keepdb

:: run tests for whalesdb app
python manage.py test -b whalesdb.test --keepdb

:: run tests for inventory app
python manage.py test -b inventory.test --keepdb

:: run tests for shiny
python manage.py test -b shiny.test --keepdb

:: run tests for ihub
python manage.py test -b ihub.test --keepdb

:: run tests for csas
python manage.py test -b csas.test --keepdb

:: run tests for cruises
python manage.py test -b cruises.test --keepdb

:: run tests for whalebrary
python manage.py test -b whalebrary.test --keepdb

:: run tests for bio_diversity
python manage.py test --exclude-tag=Functional -b bio_diversity.test --keepdb

:: run tests for scuba
python manage.py test -b scuba.test --keepdb

:: run tests for publications
python manage.py test -b publications.test --keepdb

:: run tests for edna
python manage.py test -b edna.test --keepdb

:: run tests for edna
python manage.py test -b fisheriescape.test --keepdb