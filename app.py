import requests
import json
import pandas as pd

restauranturl = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
countrydf = pd.read_excel("Country-Code.xlsx")
countrydf.columns = ["country_id", "country"]

response = requests.get(restauranturl)
data = response.json()


column_names = list(data[0]["restaurants"][0]['restaurant'].keys())
df = pd.DataFrame(columns=column_names)
row_count = 0
for row in data:
    for restaurant in row["restaurants"]:
        df.loc[row_count] = restaurant['restaurant']
        row_count += 1

country_id = df['location']
print(country_id.loc[0]['address'])
country_id = country_id.apply(lambda row: row["country_id"])
country_id = country_id.to_frame()
country_id.columns = ['country_id']

country = pd.merge(countrydf, country_id, on = "country_id")
print(country)