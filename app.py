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

city_df = locations_df.apply(lambda row: row['city']).to_frame()
city_df.columns = ["city"]

user_rating_df = df['user_rating']
rating_votes_df = user_rating_df.apply(lambda row: row["votes"]).to_frame()
rating_votes_df.columns = ["votes"]

aggregate_rating_df = user_rating_df.apply(lambda row: float(row["aggregate_rating"])).to_frame()
aggregate_rating_df.columns = ["aggregate_rating"]

cuisines_df = df["cuisines"].to_frame()
cuisines_df.columns = ["cuisines"]