# Introduction

I always wanted to learn how to create dashboards, this is my first venture into that world using Plotly-Dash. Hosting was done via Flask and Gunicorn, in Ubuntu 20.04.

# How to

1. Explore the data using `covid_explore.ipynb`
1. Install conda:
    ```bash
    wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
    bash /tmp/Anaconda3-2020.07-Linux-x86_64.sh
    ```
2. Create conda environment: `conda env create --name MY_ENV -f environment.yml python=3.8.*`
3. Update/Create the database: `python update_db.py`
4. Test the dashboard on port `8051`: `python covid_dash.py`
5. Deploy the dashboard on port `8050`: 
    ```bash
    # Or just run the update_db.sh script.
    conda activate MY_ENV
    pkill gunicorn
    gunicorn -w 4 -b 0.0.0.0:8050 covid_dash:server &
    conda deactivate
    ```
# Demo

![preview.png](https://raw.githubusercontent.com/pomkos/covid_dash/master/preview.png)

# Sources

* [World Data](https://covid.ourworldindata.org/data/)
* [US States Data](https://covidtracking.com/api/v1/states/)
* [Plotly Dash Tutorial](https://www.statworx.com/de/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/)
* [Dash Documentation](https://dash.plotly.com/)
* [Managing Conda Environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
* [Gunicorn Hosting Tutorial](https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-apps-using-gunicorn-http-server-behind-nginx#serving-python-web-applications-with-gunicorn)
