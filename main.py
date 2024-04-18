import sys
import pandas as pd
import pickle
import time
from sklearn.model_selection import train_test_split

sys.path.append("src")  # Add 'src' directory to Python path
from building_clustering import perform_kmeans
from survival_prediction import perform_survival_prediction


def main():

    # Clustering
    # data load
    # time the entire process
    start = time.time()
    print("Loading data for Clustering Analysis...")

    path = "data/processed/"
    building = pd.read_csv(path + "20240414_Survival_Features_Labeled.csv")
    review = pd.read_csv(path + "restaurant_review_240405.csv")
    br = building.merge(review, on="bin", how="left")

    # Select the relevant features for clustering
    X = br[
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
    # X["cluster"] = clusters
    # X["cluster"] = X["cluster"].astype("int")
    end = time.time()
    print(f"Data Loading and Clustering completed in {end - start:.2f} seconds.")

    pickle.dump(model, open("models/kmeans.pkl", "wb"))
    print("Model saved to 'models/kmeans.pkl'.")

    # Survival Prediction
    # time the entire process
    start = time.time()
    print("Loading data for Survival Prediction...")
    path = "data/processed/"
    surv = pd.read_csv(path + "20240414_Survival_Features_Labeled.csv")
    surv = surv.dropna()

    # feature selection
    df = (
        surv[
            [
                "flag_restaurant_one_year",
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
        ]
        .dropna()
        .copy()
    )

    # Split the dataset into training and testing sets for evaluation
    train, test = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df["flag_restaurant_one_year"],  # stratified sampling
    )
    X_train = train.drop("flag_restaurant_one_year", axis=1)
    y_train = train["flag_restaurant_one_year"]
    X_test = test.drop("flag_restaurant_one_year", axis=1)
    y_test = test["flag_restaurant_one_year"]

    # Perform survival prediction
    print("Performing survival prediction...")
    model, y_train_pred, y_test_pred = perform_survival_prediction(
        X_train, y_train, X_test, y_test
    )
    # X_train["prediction"] = y_train_pred
    # X_test["prediction"] = y_test_pred
    end = time.time()
    print(
        f"Data Loading and Survival Prediction completed in {end - start:.2f} seconds."
    )

    pickle.dump(model, open("models/xgb.pkl", "wb"))
    print("Model saved to 'models/xgb.pkl'.")


if __name__ == "__main__":
    main()
