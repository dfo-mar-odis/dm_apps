#!/bin/bash
printf "\n"
echo "RUNNING TESTS FOR: shared_models app"
python manage.py test --keepdb shared_models.test

printf "\n"
echo "RUNNING TESTS FOR: projects app"
mkdir ./media
mkdir ./media/projects
mkdir ./media/projects/temp
python manage.py test --keepdb projects.test

printf "\n"
echo "RUNNING TESTS FOR: travel app"
python manage.py test --keepdb travel.test

printf "\n"
echo "RUNNING TESTS FOR: whalesdb"
python manage.py test --keepdb whalesdb.test

printf "\n"
echo "RUNNING TESTS FOR: inventory"
python manage.py test --keepdb inventory.test

printf "\n"
echo "RUNNING TESTS FOR: shiny"
python manage.py test --keepdb shiny.test
