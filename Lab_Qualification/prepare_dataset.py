"""Prepare dataset

Download and (slightly) pre-process auction-verification dataset (in particular, the prediction
dataset for verification result and verification time) created with
https://github.com/Jakob-Bach/Analyzing-Auction-Verification/blob/master/create_prediction_dataset.py
Create a classification dataset in (X, y) format with train and test fold.

Usage: python -m prepare_dataset
"""

import os
import urllib.request

import pandas as pd
from sklearn.model_selection import train_test_split


DATA_URL = 'https://archive-beta.ics.uci.edu/api/static/ml/datasets/713/data.csv'
TEMPFILE = 'temp_dataset.csv'  # will be deleted afterwards anyway
OUTPUT_DIR = 'data/'


if __name__ == '__main__':
    # Retrieve data
    urllib.request.urlretrieve(url=DATA_URL, filename=TEMPFILE)
    dataset = pd.read_csv(TEMPFILE)
    os.remove(path=TEMPFILE)

    # Format data
    dataset.drop(columns='verification.time', inplace=True)
    dataset.rename(columns=lambda x: x.replace('process.b', 'bidder'), inplace=True)
    dataset.rename(columns=lambda x: x.replace('property.', ''), inplace=True)
    dataset.rename(columns=lambda x: x.replace('verification.result', 'verification_result'), inplace=True)

    # Split data
    X = dataset.drop(columns='verification_result')
    y = dataset['verification_result']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=25, shuffle=True, stratify=y)

    # Save data
    os.makedirs(name=OUTPUT_DIR, exist_ok=True)
    X_train.to_csv(OUTPUT_DIR + 'train_features.csv', index=False)
    y_train.to_csv(OUTPUT_DIR + 'train_target.csv', index=False)
    X_test.to_csv(OUTPUT_DIR + 'test_features.csv', index=False)
    y_test.to_csv(OUTPUT_DIR + 'test_target.csv', index=False)
