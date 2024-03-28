import folium
import pandas as pd

# Read the restaurant data from CSV
df = pd.read_csv('/Users/kayla/Desktop/restaurants.csv')

# Create a map centered at a specific location
m = folium.Map(location=[df['lat'].mean(), df['lng'].mean()], zoom_start=12)

# Add markers for each restaurant
for index, row in df.iterrows():
    folium.Marker(location=[row['lat'], row['lng']], popup=row['name']).add_to(m)

# Display the map
m.save('restaurant_map.html')
