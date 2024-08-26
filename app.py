import requests
import json
import pandas as pd

restauranturl = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"

response = requests.get(restauranturl)
data = response.json()

print(data[0])
