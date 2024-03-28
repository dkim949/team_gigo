import csv
import os

def analyze_customer_engagement(csv_file):
    # Dictionary to store restaurant names and corresponding total ratings
    restaurant_engagement = {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV file
        for row in reader:
            restaurant_name = row['name']
            user_ratings_total = int(row['user_ratings_total'])
            
            # Update the total ratings for each restaurant
            if restaurant_name in restaurant_engagement:
                restaurant_engagement[restaurant_name] += user_ratings_total
            else:
                restaurant_engagement[restaurant_name] = user_ratings_total

    # Print the total ratings for each restaurant
    for restaurant, total_ratings in restaurant_engagement.items():
        print(f"Restaurant: {restaurant}, Total Ratings: {total_ratings}")

# Get the path to the Desktop directory
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Specify the name of your CSV file
csv_file_name = 'restaurants.csv'

# Combine the Desktop path and CSV file name to get the full file path
csv_file_path = os.path.join(desktop_path, csv_file_name)

# Call the function to analyze customer engagement
analyze_customer_engagement(csv_file_path)
