import sys
import pandas as pd
import pickle
import time


sys.path.append("src")  # Add 'src' directory to Python path
from building_clustering import perform_kmeans


def main():
    # data load
    # time the entire process
    start = time.time()
    print("Loading data...")

    path = "data/processed/"
    building = pd.read_csv(path + "20240414_Survival_Features_Labeled.csv")
    review = pd.read_csv(path + "restaurant_review_240405.csv")
    df = building.merge(review, on="bin", how="left")

    # Select the relevant features for clustering
    X = df[
        [
            "rating",
            "user_ratings_total",
            "lat",
            "lng",
            "food_100",
            "food_400",
            "food_800",
            "food_1000",
            "bus_100",
            "bus_400",
            "bus_1000",
            "train_100",
            "train_400",
            "train_1000",
            "office_area",
            "retail_area",
            "residential_area",
            "street_width_min",
            "street_width_max",
            "dist_station",
            "dist_park",
            "dist_school",
            "office_450",
            "retail_450",
            "residential_450",
            "ridership_morning_mean",
            "ridership_midday_mean",
            "ridership_evening_mean",
            "ridership_night_mean",
            "ridership_late_night_mean",
            "idw_aadt_mean",
            "idw_atvc_mean",
        ]
    ].dropna()

    # Perform K-means clustering
    print("Performing K-means clustering...")
    model, clusters = perform_kmeans(X, n_components=15, n_clusters=4)
    X["cluster"] = clusters
    X["cluster"] = X["cluster"].astype("int")
    end = time.time()
    print(f"Data Loading and Clustering completed in {end - start:.2f} seconds.")

    pickle.dump(model, open("models/kmeans.pkl", "wb"))
    print("Model saved to 'models/kmeans.pkl'.")


if __name__ == "__main__":
    main()
