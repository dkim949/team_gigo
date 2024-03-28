import csv
import os

def calculate_average_ratings(csv_file):
    # Dictionary to store restaurant names and corresponding ratings
    restaurant_ratings = {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV file
        for row in reader:
            restaurant_name = row['name']
            rating = float(row['rating'])
            
            # Check if restaurant name already exists in the dictionary
            if restaurant_name in restaurant_ratings:
                # If yes, update the sum of ratings and count of ratings
                restaurant_ratings[restaurant_name]['total_rating'] += rating
                restaurant_ratings[restaurant_name]['total_reviews'] += 1
            else:
                # If no, initialize the restaurant entry in the dictionary
                restaurant_ratings[restaurant_name] = {
                    'total_rating': rating,
                    'total_reviews': 1
                }

    # Calculate average rating for each restaurant
    for restaurant, data in restaurant_ratings.items():
        average_rating = data['total_rating'] / data['total_reviews']
        print(f"Restaurant: {restaurant}, Average Rating: {average_rating:.2f}")

# Get the path to the Desktop directory
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Specify the name of your CSV file
csv_file_name = 'restaurants.csv'

# Combine the Desktop path and CSV file name to get the full file path
csv_file_path = os.path.join(desktop_path, csv_file_name)

# Call the function to calculate average ratings
calculate_average_ratings(csv_file_path)
