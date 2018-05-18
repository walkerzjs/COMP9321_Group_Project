import pandas as pd


def get_pm_data(year):
    pm25 = pd.read_csv("data_publication_pm/data/potential data/PM2.5/API_EN.ATM.PM25.MC.M3_DS2_en_csv_v2.csv", sep='\t')
    pm25 = pm25[["Country Name", "{}".format(year)]]
    pm25 = pm25.rename(columns={"Country Name": "Country", "{}".format(year): "PM2.5"})
    return pm25.to_json(orient="records")
