"""Score students

Read in all submissions of students, check validity of format, and evaluate prediction quality.
Assumes the main submission directory is downloaded from ILIAS and contains sub-directories named
like "<<Name>>_<<uxxxx>>_<<some number>>". The script allows each of these sub-directories to
contain multiple prediction files (e.g., if the initial one was slightly invalid, e.g., wrong
column name, and we manually created a fixed version (because we are nice)). Fixed versions of
original prediction files should contain the substring "-fixed".

Usage: python -m score_students
"""


import csv
import glob
import os
import re
from typing import Union

import pandas as pd
from sklearn.metrics import matthews_corrcoef


GROUND_TRUTH_FILE = "data/test_target.csv"  # created by prepare_dataset.py
SUBMISSION_DIR = "data/submissions/"  # should be downloaded from ILIAS


# Check format of "submission" (relative to a "ground_truth") and return string with first issue
# found. Empty string if no issues.
def check_submission_validity(submission: Union[pd.DataFrame, pd.Series],
                              ground_truth: pd.Series) -> str:
    if isinstance(submission, pd.DataFrame):
        return f'Number of columns wrong: {submission.shape[1]}.'
    if submission.shape[0] != ground_truth.shape[0]:
        return f'Number of data objects wrong: {submission.shape[0]}.'
    if submission.name != ground_truth.name:
        return 'Column name wrong (might be quoted).'
    if ((submission != True) & (submission != False)).any():
        return 'At least one invalid value.'
    if submission.isna().any():
        return 'At least one NA.'
    return ''


if __name__ == '__main__':
    y_test = pd.read_csv(GROUND_TRUTH_FILE).squeeze(axis='columns')
    results = []
    student_dirs = [x.name for x in os.scandir(path=SUBMISSION_DIR) if x.is_dir()]
    for student_dir in student_dirs:
        full_name = re.sub(pattern='_u[a-z]{4}.*', repl='', string=student_dir)
        account_name = re.search(pattern='_(u[a-z]{4})_', string=student_dir).group(1)
        submission_files = glob.glob(pathname=SUBMISSION_DIR + student_dir + '/*_prediction.csv')
        # There might be multiple submission files in a student's directory:
        for submission_file in submission_files:
            submission_name = os.path.basename(submission_file).replace('_prediction.csv', '')
            is_fixed = '-fixed' in submission_name  # manually fixed to adhere to formatting requirements
            current_result = {'Full name': full_name, 'Submission name': submission_name,
                              'Account': account_name, 'is fixed': is_fixed}
            prediction = pd.read_csv(submission_file, header=0, quoting=csv.QUOTE_NONE).squeeze(
                axis='columns')  # header and quotes will be validated
            validity_status = check_submission_validity(submission=prediction, ground_truth=y_test)
            current_result['Issue'] = validity_status
            if validity_status == '':
                current_result['Score'] = matthews_corrcoef(y_true=y_test, y_pred=prediction)
            else:
                current_result['Score'] = float('nan')
            results.append(current_result)
    results = pd.DataFrame(results)
    print(results.sort_values(by='Score', ascending=False).reset_index(drop=True))
