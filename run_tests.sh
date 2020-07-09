#!/bin/bash
printf "\n"
echo "RUNNING TESTS FOR: shared_models app"
python manage.py test --keepdb shared_models.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: projects app"
mkdir ./media
mkdir ./media/projects
mkdir ./media/projects/temp
python manage.py test --keepdb projects.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: travel app"
python manage.py test --keepdb travel.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: whalesdb"
python manage.py test --keepdb whalesdb.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: inventory"
python manage.py test --keepdb inventory.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: shiny"
python manage.py test --keepdb shiny.test -v 0
