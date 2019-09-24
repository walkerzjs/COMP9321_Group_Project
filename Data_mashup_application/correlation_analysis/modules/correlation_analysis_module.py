import requests
import json
import pandas as pd


# send api request to data publication server to retrieve the pm2.5 data with specific year from data publication api.
def retrieve_pm_backup(year):
    accept_tp = 'JSON'
    url = "http://127.0.0.1:5000/api/pm/{}".format(year)
    result = requests.get(url, params=None, headers={
                                      "ACCEPT": accept_tp})
    return json.loads(result.text)

def retrieve_pm(year):
    accept_tp = 'JSON'
    url = "http://127.0.0.1:1234/api/air_pollution/{}".format(year)
    result = requests.get(url, params=None, headers={
                          "ACCEPT": accept_tp})
    data_pm = json.loads(result.text)
    data_list = []
    for key in data_pm:
        value = data_pm[key]
        print(key,value)
        record = {'Country': key, 'PM2.5': value}
        data_list.append(record)
    data_json = pd.DataFrame.from_dict(data_list).to_json(orient="records")
    return data_json



# retrieve the world happiness report data with specific year from data publicaton api.
def retrieve_world_happiness(year):
    accept_tp = 'JSON'
    url = "http://127.0.0.1:1234/api/world_happiness/{}".format(year)
    result = requests.get(url, params=None,
                          headers={
                              "ACCEPT": accept_tp})
    result_json = json.loads(result.text)
    data = pd.DataFrame.from_dict(result_json['data'])
    data['Country'] = data.index
    return data.to_json(orient='records')


# retrieve joined pm2.5 and happiness report data from data curation api.
def retrieve_joined_data(year):
    pm_json = retrieve_pm(year)
    happy_json = retrieve_world_happiness(year)
    url = "http://127.0.0.1:1234/api/join"
    data_json = {"pm": pm_json, "world_happiness": happy_json}
    result = requests.post(url, json=data_json,
                           headers={"Content-Type": "application/json"})
    return json.loads(result.text)
