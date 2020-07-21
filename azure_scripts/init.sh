#!/bin/bash
-e

#CMD ["gunicorn",  "--bind", "8000:8000", "mysite.wsgi:application"]
docker restart dmapps_img
gunicorn -b 0.0.0.0:8000 dm_apps.wsgi:application