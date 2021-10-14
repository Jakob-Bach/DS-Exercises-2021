"""Grocery dataset preparation

Run this script to download, preprocess, and save the Groceries dataset used for exercise sheet 3.

Usage: python procure_groceries_dataset.py
"""

import csv
import os
import warnings

import pyreadr
import rdata

if __name__ == '__main__':
    GROCERIES_URL = 'https://github.com/mhahsler/arules/raw/master/data/Groceries.rda'
    TMP_RDA_DIR = './'
    TMP_RDA_FILENAME = 'groceries.rda'
    GROCERIES_DIR = 'solution/'
    GROCERIES_FILENAME = 'groceries.csv'
    GROCERIES_STRUCTURE_FILENAME = 'groceries_structure.csv'

    # Download and parse:
    tmp_file_path = os.path.join(TMP_RDA_DIR, TMP_RDA_FILENAME)
    pyreadr.download_file(GROCERIES_URL, tmp_file_path)
    parsed = rdata.parser.parse_file(tmp_file_path)
    with warnings.catch_warnings():
        warnings.filterwarnings(action='ignore', message='Missing constructor for R class')
        converted = rdata.conversion.convert(parsed)
    os.remove(tmp_file_path)

    # Prepare hierarchy of item categories (for multi-level mining):
    structure_df = converted['Groceries'].itemInfo[['labels', 'level1', 'level2']].rename(columns={'labels': 'label'})
    structure_df.to_csv(os.path.join(GROCERIES_DIR, GROCERIES_STRUCTURE_FILENAME), index=False)

    # Prepare transaction data - is a sparse matrix in R (ngCMatrix), thus code slightly awkward:
    # - "i" contains the indices of all items in transaction-item matrix "rolled out" as a 1D
    # array (whose length corresponds to the total number of items over all transactions); the
    # items are sorted by transactions (i.e., first all items of 1st transaction, then all items of
    # 2nd transaction etc.), but the boundaries between transactions are not clear from "i" alone
    # - "p" tells at which indices "i" should be split to create the transactions; it is a 1D array
    # whose length corresponds to the number of transactions + 1
    item_labels = [structure_df.iloc[idx]['label'] for idx in converted['Groceries'].data.i]
    transactions = [item_labels[transaction_start_idx:transaction_end_idx]
                    for transaction_start_idx, transaction_end_idx
                    in zip(converted['Groceries'].data.p[:-1], converted['Groceries'].data.p[1:])]

    with open(os.path.join(GROCERIES_DIR, GROCERIES_FILENAME), mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        for row in transactions:
            writer.writerow(row)
