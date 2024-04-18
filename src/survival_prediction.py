import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE  # SMOTE for label imbalance
from xgboost import XGBClassifier  # xgboost clf
from sklearn.metrics import accuracy_score  # accuracy score
from sklearn.metrics import classification_report  # classification report


def perform_survival_prediction(X_train, y_train, X_test, y_test):
    """
    Perform survival prediction using the given dataset.

    Parameters
    ----------
    X_train : Pandas DataFrame
        The input training dataset.
    y_train : Pandas Series
        The target training dataset.
    X_test : Pandas DataFrame
        The input testing dataset.
    y_test : Pandas Series
        The target testing dataset.

    Returns
    -------
    model : XGBClassifier
        The trained XGBoost classifier.
    y_train_pred : ndarray
        The predicted labels for the training set.
    y_test_pred : ndarray
        The predicted labels for the testing set.
    """

    # SMOTE for label imbalance
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # standardize the dataset
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train_resampled)

    # train xgboost classifier using the hyperparameters from hyperopt
    model = XGBClassifier(
        objective="binary:logistic",
        n_estimators=490,
        learning_rate=0.13,
        max_depth=3,
        min_child_weight=8.0,
        subsample=0.5,
        colsample_bytree=0.7,
        scale_pos_weight=1.0,
        gamma=0.4,
        seed=42,
        eval_metric="logloss",
    )
    model.fit(X_train_resampled, y_train_resampled)
    y_train_pred = model.predict(X_train_resampled)
    y_test_pred = model.predict(X_test)

    # accuracy for train and test sets
    train_accuracy = accuracy_score(y_train_resampled, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Train accuracy: {train_accuracy:.2f}")
    print(f"Test accuracy: {test_accuracy:.2f}")
    # classification report
    print("Train classification report:")
    print(classification_report(y_train_resampled, y_train_pred))
    print("Test classification report:")
    print(classification_report(y_test, y_test_pred))

    return model, y_train_pred, y_test_pred
