import csv
import os
import pandas as pd
import sys


def log(row):
    """Make the log if row is header, or otherwise add to existing log"""
    log_path = os.path.join(update_dir, 'update_log.csv')
    if row == "header":
        with open(log_path, 'w', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(['Folder', 'Has_Pres_Log', 'Saved', 'Error'])
    else:
        with open(log_path, 'a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(row)


def update_pres_log(pres_path):
    """Read the preservation log, test for errors, and save as csv if no error"""
    new_pres_path = pres_path.replace('.txt', '.csv')
    try:
        # Read tab delimited text file and save as a csv, if it can be parsed correctly.
        pres_df = pd.read_csv(pres_path, delimiter='\t')
        pres_df.to_csv(new_pres_path, index=False)

        # Extra tabs can also cause there to be extra column names.
        # These can be saved without editing but need to be updated manually.
        if pres_df.columns.tolist() == ['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff']:
            return None
        else:
            return 'Column_Name_Error'

    # ParserError happens if there are extra tabs on some rows,
    # resulting in more columns than there are in the column header row.
    except pd.errors.ParserError as error_msg:
        # Read without automatically assigning a column header so that everything can be saved as a CSV.
        # These will need to be updated manually.
        # The intended column headers will be the first row.
        max_column = str(error_msg).split(' ')[-1]
        pres_df = pd.read_csv(pres_path, delimiter='\t', header=None, names=range(int(max_column)))
        pres_df.to_csv(new_pres_path, index=False)
        return f'ParserError, {error_msg}'


if __name__ == '__main__':

    # Give path to backlogged or closed folder. We'll run this 4 times.
    update_dir = sys.argv[1]

    # Start a log in update_dir.
    log('header')

    # Don't bother with checking if a folder is an accession, and just check if it has a preservation log or not.
    # If it does, it will be update_dir/collection/accession/preservation_log.txt
    for collection in os.listdir(update_dir):

        # Skip the log or it gives a NotADirectoryError in the next step.
        if collection == 'update_log.csv':
            continue

        for accession in os.listdir(os.path.join(update_dir, collection)):
            accession_path = os.path.join(update_dir, collection, accession)
            pres_log = os.path.join(accession_path, 'preservation_log.txt')

            # If there is no preservation_log.txt, logs and continues.
            # It probably isn't an accession. This is a double check.
            if not os.path.exists(pres_log):
                log([accession_path, False, 'n/a', 'n/a'])
            # Read, check for errors, save to csv, and log the results.
            else:
                errors = update_pres_log(pres_log)
                if errors:
                    log([accession_path, True, True, errors])
                else:
                    log([accession_path, True, True, 'n/a'])

