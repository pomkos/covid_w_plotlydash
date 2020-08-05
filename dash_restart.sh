#! /bin/bash
source /opt/tljh/user/bin/activate
conda activate ubicorn_env
pkill gunicorn
gunicorn -w 4 -b 0.0.0.0:8050 covid_dash:server &
conda deactivate
