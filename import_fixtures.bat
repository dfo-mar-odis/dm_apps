@echo off
setlocal EnableDelayedExpansion
set /p continue="Are you sure you want to import fixtures into the current database? THIS ACTION CAN BE VERY HARMFUL IF BEING RUN AGAINST A PRODUCTION DATABASE!! Proceed (yes/no)? "
if "%continue%"=="yes" (
    set /p venv="In order to run this script, the virtual environment must be activated. Proceed (yes/no)? "
    if "%venv%"=="yes" (
        set "fixtures="
        for /R .\inventory\fixtures %%g in (*.json) do (
            set "fixtures=!fixtures! %%g"
        )

    )
)

if "%continue%"=="yes" (
    if "%venv%"=="yes" (
        python manage.py loaddata %fixtures%
    )
)



