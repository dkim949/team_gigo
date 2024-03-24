import googlemaps
gmaps = googlemaps.Client(key='')

import json
import time

neighborhoods = []
with open('neighborhoods.txt') as f:
    for line in f:
        neighborhoods.append(line.strip())

# print(neighborhoods)

restaurants = []

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))

def restaurant_response(response_items, neighborhood):
    restaurant_responses = []
    for item in response_items:
        item_dict = {}
        item_dict['neighborhood'] = neighborhood
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


for neighborhood in neighborhoods:
    query = f"restaruants in {neighborhood}, Manhattan, New York City, USA"
    
    place = gmaps.geocode(query)
    place_info = place[0]
    geo_results = place_info['geometry']
    geo_coordinates = geo_results['location']
    lat = geo_coordinates['lat']
    lng = geo_coordinates['lng']

    flag = False
    counter = 0
    while flag == False:
        if counter == 0:
            results = gmaps.places(type="restaurant", location=[lat, lng], radius=3000)
            response_items = results['results']
            
            restaurants.extend(restaurant_response(response_items, neighborhood))
            print(len(restaurants))
            save_as_json(restaurants, 'restaurants.json')
            counter += 1
        else:
            if results.get('next_page_token') is None:
                flag = True
            else:
                next_page = results.get('next_page_token')
                time.sleep(2)
                results = gmaps.places(type="restaurant", location=[lat, lng], radius=3000, page_token=next_page)
                response_items = results['results']
                restaurants.extend(restaurant_response(response_items, neighborhood))
                print(len(restaurants))
                save_as_json(restaurants, 'restaurants.json')
                counter += 1


