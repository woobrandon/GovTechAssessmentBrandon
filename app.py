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

restaurant_id_df = df["id"].to_frame()
restaurant_id_df.columns = ["id"]

restaurant_name_df = df["name"].to_frame()
restaurant_name_df.columns = ['name']

locations_df = df['location']
country_id_df = locations_df.apply(lambda row: row["country_id"])
country_id_df = country_id_df.to_frame()
country_id_df.columns = ['country_id']
country = pd.merge(countrydf, country_id_df, on = "country_id")
