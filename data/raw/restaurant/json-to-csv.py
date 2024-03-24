import pandas as pd
import json

f = open('restaurants.json')
content = f.read()
json_obj = json.loads(content)
df = pd.json_normalize(json_obj)

print(df)

df.to_csv('restaurants.csv', index=False)