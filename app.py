import requests
import pandas as pd
from datetime import datetime

restauranturl = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
country_code_df = pd.read_excel("Country-Code.xlsx")
country_code_df.columns = ["country_id", "country"]

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
restaurant_id_df.columns = ["restaurant_id"]

restaurant_name_df = df["name"].to_frame()
restaurant_name_df.columns = ['name']
temp = restaurant_name_df[restaurant_name_df['name'] == "Chili's Grill & Bar"]

locations_df = df['location']
country_id_df = locations_df.apply(lambda row: row["country_id"]).to_frame()
country_id_df.columns = ['country_id']
country_df = pd.merge(country_code_df, country_id_df, on = "country_id", how = "right")

city_df = locations_df.apply(lambda row: row['city']).to_frame()
city_df.columns = ["city"]

user_rating_df = df['user_rating']
rating_votes_df = user_rating_df.apply(lambda row: row["votes"]).to_frame()
rating_votes_df.columns = ["votes"]

aggregate_rating_df = user_rating_df.apply(lambda row: float(row["aggregate_rating"])).to_frame()
aggregate_rating_df.columns = ["aggregate_rating"]

cuisines_df = df["cuisines"].to_frame()
cuisines_df.columns = ["cuisines"]

restaurants = pd.concat([restaurant_id_df, restaurant_name_df, country_df, city_df, rating_votes_df, aggregate_rating_df, cuisines_df], axis = 1)

# restaurants.to_csv("restaurants.csv", index = False)

def filter_event(row):
    zomato_event = row["zomato_events"]
    if type(zomato_event) == list:
        target = datetime.strptime("2019-04", "%Y-%m")
        event_data = zomato_event[0]["event"]
        start_date = event_data["start_date"][:7]
        start_date = datetime.strptime(start_date, "%Y-%m")
        end_date = event_data["end_date"][:7]
        end_date = datetime.strptime(end_date, "%Y-%m")
        if start_date <= target and end_date >= target:
            return True

print()
event_filtered_df = df.apply(lambda row: row if filter_event(row) else None, axis = 1)
print(event_filtered_df.loc[29])
print(datetime.strptime(df.loc[29]["zomato_events"][0]["event"]["start_date"][:7], "%Y-%m") <= datetime.strptime("2019-04", "%Y-%m"))
print(df.loc[29]["zomato_events"])