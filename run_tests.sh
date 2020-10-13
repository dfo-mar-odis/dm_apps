#!/bin/bash
printf "\n"
echo "RUNNING TESTS FOR: shared_models app"
python manage.py test -v0 shared_models.test

printf "\n"
echo "RUNNING TESTS FOR: projects app"
mkdir ./media
mkdir ./media/projects
mkdir ./media/projects/temp
python manage.py test -v0 projects.test

printf "\n"
echo "RUNNING TESTS FOR: travel app"
python manage.py test -v0 travel.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: whalesdb"
python manage.py test -v0 whalesdb.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: inventory"
python manage.py test -v0 inventory.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: shiny"
python manage.py test -v0 shiny.test -v 0

printf "\n"
echo "RUNNING TESTS FOR: ihub"
python manage.py test -v0 ihub.test -v 0


printf "\n"
echo "RUNNING TESTS FOR: csas"
python manage.py test -v0 csas.test -v 0