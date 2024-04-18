import googlemaps
gmaps = googlemaps.Client(key='')

from tqdm import tqdm

import json
import time

import pandas as pd




# list of restaurants
restaurants = []

with open('restaurants.json') as f:
    restaurants = json.loads(f.read())

print(len(restaurants))


# function to save restaurants list as json file
def save_as_json(data, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))




# convert Places API response to one restaurant dict object.
# just get some fields of Places API
def restaurant_response(response_items):
    restaurant_responses = []
    for item in response_items:
        item_dict = {}
        item_dict['name'] = item.get('name')
        item_dict['place_id'] = item.get('place_id')
        item_dict['price_level'] = item.get('price_level')
        item_dict['rating'] = item.get('rating')
        item_dict['user_ratings_total'] = item.get('user_ratings_total')
        item_dict['business_status'] = item.get('business_status')
        item_dict['adr_address'] = item.get('adr_address')
        item_dict['formatted_address'] = item.get('formatted_address')
        item_dict['lat'] = item.get('geometry').get('location').get('lat')
        item_dict['lng'] = item.get('geometry').get('location').get('lng')
        restaurant_responses.append(item_dict)
    return restaurant_responses



df = pd.read_csv('tract_centroids.csv')

for idx in tqdm(df.index):
    if idx < 232:
        continue

    lat = df['lat'][idx]
    lon = df['lon'][idx]


    # fetch all the restaurant data within 400m from the center.
    flag = False
    counter = 0
    while flag == False:
        if counter == 0:
            results = gmaps.places(type="restaurant", location=[lat, lon], radius=400)
            response_items = results['results']
            restaurants.extend(restaurant_response(response_items))
            save_as_json(restaurants, 'restaurants.json')
            counter += 1
        else:
            if results.get('next_page_token') is None:
                flag = True
            else:
                next_page = results.get('next_page_token')
                time.sleep(2)
                results = gmaps.places(type="restaurant", location=[lat, lon], radius=400, page_token=next_page)
                response_items = results['results']
                restaurants.extend(restaurant_response(response_items))
                save_as_json(restaurants, 'restaurants.json')
                counter += 1

