import csv
import os

def analyze_price_sensitivity_by_neighborhood(csv_file):
    # Dictionary to store neighborhood-wise price level counts
    neighborhood_price_levels = {}

    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Iterate through each row in the CSV file
        for row in reader:
            neighborhood = row['neighborhood']
            price_level = row['price_level']
            
            # Convert price level to float and round to nearest integer
            try:
                price_level = int(round(float(price_level)))
            except ValueError:
                price_level = None
            
            # Map numerical price levels to corresponding categories
            if price_level == 1:
                price_category = '$'
            elif price_level == 2:
                price_category = '$$'
            elif price_level == 3:
                price_category = '$$$'
            elif price_level == 4:
                price_category = '$$$$'
            else:
                price_category = 'Not Available'
            
            # Update the count for each price level within each neighborhood
            if neighborhood not in neighborhood_price_levels:
                neighborhood_price_levels[neighborhood] = {'$': 0, '$$': 0, '$$$': 0, '$$$$': 0, 'Not Available': 0}
            
            neighborhood_price_levels[neighborhood][price_category] += 1

    # Print the price sensitivity analysis results by neighborhood
    print("Price Sensitivity Analysis by Neighborhood:")
    for neighborhood, price_levels in neighborhood_price_levels.items():
        print(f"\nNeighborhood: {neighborhood}")
        for price_level, count in price_levels.items():
            print(f"Price Level: {price_level}, Count: {count}")

# Get the path to the Desktop directory
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Specify the name of your CSV file
csv_file_name = 'restaurants.csv'

# Combine the Desktop path and CSV file name to get the full file path
csv_file_path = os.path.join(desktop_path, csv_file_name)

# Call the function to analyze price sensitivity by neighborhood
analyze_price_sensitivity_by_neighborhood(csv_file_path)
