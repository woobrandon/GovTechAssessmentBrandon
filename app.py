import requests
import pandas as pd
from datetime import datetime

# importing the 2 datasets
restauranturl = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
country_code_df = pd.read_excel("Country-Code.xlsx")
country_code_df.columns = ["country_id", "country"]

response = requests.get(restauranturl)
data = response.json()

# convorting the json file into a pandas dataframe
column_names = list(data[0]["restaurants"][0]['restaurant'].keys())
df = pd.DataFrame(columns=column_names)
row_count = 0
for row in data:
    for restaurant in row["restaurants"]:
        df.loc[row_count] = restaurant['restaurant']
        row_count += 1

# creating individual columns dataframe
def get_column(column, dataframe = df, nested = False):
    if not nested:
        column_df = dataframe[column].to_frame()
    else:
        column_df = dataframe.apply(lambda row: row[column]).to_frame()
    column_df.columns = [column]
    return column_df

restaurant_id_df = get_column("id")

restaurant_name_df = get_column("name")

locations_df = df['location']

country_id_df = get_column("country_id", locations_df, True)
country_df = pd.merge(country_code_df, country_id_df, on = "country_id", how = "right")

city_df = get_column("city", locations_df, True)

user_rating_df = df['user_rating']

rating_votes_df = get_column("votes", user_rating_df, True)

aggregate_rating_df = get_column("aggregate_rating", user_rating_df, True)

cuisines_df = get_column("cuisines")

restaurants = pd.concat([restaurant_id_df, restaurant_name_df, country_df, city_df, rating_votes_df, aggregate_rating_df, cuisines_df], axis = 1)

# exporting restaurants to csv
restaurants.to_csv("restaurants.csv", index = False)

# filtering events to check if they fall in April 2019
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
    return False

filter_df = df.apply(lambda row: True if filter_event(row) else False, axis = 1)
df2 = df[filter_df].reset_index(drop = True)
zomato_events_df = df2["zomato_events"]

# creating individual columns dataframe
restaurant_id_df2 = restaurant_id_df[filter_df].reset_index(drop = True)

restaurant_name_df2 = restaurant_name_df[filter_df].reset_index(drop = True)

photo_url_df = zomato_events_df.apply(lambda row: row[0]['event']['photos'][0]['photo']['url'] if len(row[0]['event']['photos']) != 0 else "NA").to_frame()
photo_url_df.columns = ["photo_url"]

def zomato_events_filter(column):
    column_df = zomato_events_df.apply(lambda row: row[0]['event'][column]).to_frame()
    column_df.columns = [column]
    return column_df

event_id_df = zomato_events_filter("event_id")

event_title_df = zomato_events_filter("title")

start_date_df = zomato_events_filter("start_date")

end_date_df = zomato_events_filter("end_date")

restaurant_event_df = pd.concat([event_id_df, restaurant_id_df2, restaurant_name_df2, photo_url_df, event_title_df, start_date_df,end_date_df], axis = 1)

# exporting restaurant_event_df to csv file
restaurant_event_df.to_csv("restaurants_events.csv", index = False)

# merging aggregate_rating_df and rating_text_df
rating_text_df = get_column("rating_text", user_rating_df, True)
user_votes_ratings_df = pd.concat([aggregate_rating_df,rating_text_df], axis = 1)

# getting the threshold values and printing to the terminal
def threshold_filter(rating):
    rating_df = user_votes_ratings_df[user_votes_ratings_df["user_rating"] == rating]
    threshold_df = [min(rating_df["aggregate_rating"]),max(rating_df["aggregate_rating"])]
    print(threshold_df)
    return(threshold_df)

excellent_threshold = threshold_filter("Excellent")

very_good_threshold = threshold_filter("Very Good")

good__threhold = threshold_filter("Good")

average_threshold = threshold_filter("Average")

poor_threshold = threshold_filter("Poor")

