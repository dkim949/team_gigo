import csv
import os

def calculate_average_ratings_by_neighborhood(csv_file):
    # Dictionary to store neighborhood-wise ratings
    neighborhood_ratings = {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV file
        for row in reader:
            neighborhood = row['neighborhood']
            rating = float(row['rating'])
            
            # Check if the neighborhood already exists in the dictionary
            if neighborhood in neighborhood_ratings:
                # If yes, update the sum of ratings and count of ratings
                neighborhood_ratings[neighborhood]['total_rating'] += rating
                neighborhood_ratings[neighborhood]['total_reviews'] += 1
            else:
                # If no, initialize the neighborhood entry in the dictionary
                neighborhood_ratings[neighborhood] = {
                    'total_rating': rating,
                    'total_reviews': 1
                }

    # Calculate average rating for each neighborhood
    for neighborhood, data in neighborhood_ratings.items():
        average_rating = data['total_rating'] / data['total_reviews']
        print(f"Neighborhood: {neighborhood}, Average Rating: {average_rating:.2f}")

# Get the path to the Desktop directory
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Specify the name of your CSV file
csv_file_name = 'restaurants.csv'

# Combine the Desktop path and CSV file name to get the full file path
csv_file_path = os.path.join(desktop_path, csv_file_name)

# Call the function to calculate average ratings by neighborhood
calculate_average_ratings_by_neighborhood(csv_file_path)
