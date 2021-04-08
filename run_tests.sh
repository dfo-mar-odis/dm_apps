#!/bin/bash
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: shared_models app"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b  shared_models.test
echo "FINISHED RUNNING TESTS FOR: shared_models app"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: projects app"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
mkdir ./media
mkdir ./media/projects
mkdir ./media/projects/temp
python3.8 manage.py test -b projects2.test
echo "FINISHED RUNNING TESTS FOR: projects app"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: travel app"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b travel.test

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: whalesdb"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b whalesdb.test
echo "FINISHED RUNNING TESTS FOR: whalesdb"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: inventory"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b inventory.test
echo "FINISHED RUNNING TESTS FOR: inventory"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: shiny"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b shiny.test
echo "FINISHED RUNNING TESTS FOR: shiny"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: ihub"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b ihub.test
printf "\n"
echo "FINISHED RUNNING TESTS FOR: ihub"


printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: csas"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b csas.test
echo "FINISHED RUNNING TESTS FOR: csas"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: cruises"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b cruises.test
echo "FINISHED RUNNING TESTS FOR: cruises"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: whalebrary"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b whalebrary.test
echo "FINISHED RUNNING TESTS FOR: whalebrary"

printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: bio_diversity"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test --exclude-tag=Functional -b bio_diversity.test
echo "FINISHED RUNNING TESTS FOR: bio_diversity"



printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: scuba"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b scuba.test
echo "FINISHED RUNNING TESTS FOR: scuba"


printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: publications"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b publications.test
echo "FINISHED RUNNING TESTS FOR: publications"



printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: eDNA"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b edna.test
echo "FINISHED RUNNING TESTS FOR: eDNA"



printf "\n"
printf "\n"
printf "\n"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
echo "RUNNING TESTS FOR: fisheriescape"
printf "\n"
printf "#############################################################################################################################"
printf "\n"
python3.8 manage.py test -b fisheriescape.test
echo "FINISHED RUNNING TESTS FOR: fisheriescape"