# from django.http import HttpResponse
from django.shortcuts import render
import requests
import datetime
from background_task import background
from .models import ControllerReadings

import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
application = newrelic.agent.register_application(timeout=10.0)

# global declarations
global minute_string, co2emission_all, minute_heat_rate_sum, minute_heat_rate_avg
minute_string = 1
co2emission_all, minute_heat_rate_sum, minute_heat_rate_avg = 0, 0, 0


# This is the function that pulls the records from the emissions API and processes them to create results
# It also creates database entries for the 'readings' model
@background(schedule=10)
def worker():
    global minute_string
    print("From the background task. Value of minute string is ", minute_string)
    # input params for the CO2, SO2 and NOX emissions
    # date_string = datetime.datetime.now().date()
    date_string = "2021-02-26"
    # minute_string = 12

    # for i in range(1, minute_string + 1):
    global co2emission_all, minute_heat_rate_sum, minute_heat_rate_avg
    # CO2 emissions so far
    req_str = 'http://127.0.0.1:8082/co2/2021-02-26/' + str(minute_string)
    resp_co2 = requests.get(req_str)
    co2emission_all = round(co2emission_all + resp_co2.json().get('emission_Mt'), 3)

    # Minute heat rate average so far
    req_str = 'http://127.0.0.1:8082/co2/2021-02-26/' + str(minute_string) + '/hr'
    minute_heat_rate_sum = minute_heat_rate_sum + requests.get(req_str).json().get('heat_rate')
    minute_heat_rate_avg = minute_heat_rate_sum / minute_string

    # get the standing value of the carbon dioxide reserve
    req_str = 'http://127.0.0.1:8082/co2/2021-02-26/' + str(minute_string) + '/reserve'
    co2_reserve = requests.get(req_str).json().get('co2_store')
    co2_reserve = round(co2_reserve / 1000)

    plant_efficiency = round(3412 * 100 / minute_heat_rate_avg, 2)

    # create objects in model for controller reading
    ControllerReadings.objects.get_or_create(cumulative_CO2=co2emission_all, minute_heat_rate_avg=minute_heat_rate_avg,
                                             plant_efficiency=plant_efficiency, co2_reserve=co2_reserve,
                                             measured_date="2021-02-26",
                                             measured_at_minute=minute_string)

    # send custom metrics to New Relic
    newrelic.agent.record_custom_metric('Custom/PlantEfficiency', plant_efficiency, application)

    # increment minute_string
    minute_string = minute_string + 1


def index(request):
    print("From index")
    worker(repeat=60, repeat_until=None)    # runs the worker background task once every minute

    # some assumptions
    coal_consumption = 400000000  # annual consumption of coal for electricity generation, in metric tons
    daily_coal = round(coal_consumption / 365)  # assumed to be uniform by time
    required_carbon_efficiency = 0.5  # some value

    # input params for the CO2, SO2 and NOX emissions
    date_string = datetime.datetime.now().date()

    # get the size of the existing ControllerReading table in the db; this is the latest information available
    # from the worker background task
    dataAll = ControllerReadings.objects.all()
    minuteLast = len(dataAll)
    print("Minute now set at", minuteLast, "from index")

    # get the model object values
    # data = ControllerReadings.objects.get(measured_date=datetime.datetime.now().date(), measured_at_minute=minuteLast)
    data = ControllerReadings.objects.get(measured_date="2021-02-26", measured_at_minute=minuteLast)
    co2emission_all_latest = data.cumulative_CO2
    plant_efficiency_latest = data.plant_efficiency
    co2_reserve_latest = data.co2_reserve
    return render(request, 'controller/index.html',
                  {"co2emission": co2emission_all_latest, "daily_coal": daily_coal, "plant_efficiency": plant_efficiency_latest,
                   "date": date_string, "co2_reserve": co2_reserve_latest})

