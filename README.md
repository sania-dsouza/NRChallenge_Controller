# NRChallenge_Services

## Objective: ##
This project is the browser app which displays cumulative information on the daily CO2 emissions and other numbers to be monitored by a non-tech person to get a high-level picture of emission data.
It uses the Django framework and the default sqlite database as a data store. It uses the django-background-tasks package to pull information from the services API running on AWS Lambda. 

## How to set up on local: ##

- Clone the repo : ``` git clone https://github.com/sania-dsouza/NRChallenge_Controller.git ```
- cd into the 'PlantEmissionController' folder: ``` cd PlantEmissionController ```
- Install dependencies: ``` pip install ```
- Run the project by sending information to New Relic at the same time
  ``` NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python manage.py runserver 8082 ```
- View the project running at http://127.0.0.1:8082/
This the front-end of the controller which displays cumulative emission data. The user needs to refresh the page to see this data. In the background, a service runs that pulls data from the power plant (the NRChallenge_Services aka the power plant).
Refresh the page periodically to see updated emission data as the day progresses. 
