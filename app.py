import requests
import json
import pandas as pd

restauranturl = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"

response = requests.get(restauranturl)
data = response.json()

column_names = list(data[0]["restaurants"][0]['restaurant'].keys())
df = pd.DataFrame(columns=column_names)
row_count = 0
for row in data:
    for restaurant in row["restaurants"]:
        temp = restaurant['restaurant']
        temp["R"] = temp["R"]['res_id']
        df.loc[row_count] = restaurant['restaurant']
        row_count += 1

print(df)