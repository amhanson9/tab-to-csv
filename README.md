# tab-to-csv

## Description
Convert tab delimited preservation log to CSV, saved in the same location, with logging.

If there is a parsing error, it saves the CSV without a header for later manual update.
If the columns are not what is expected, it saves the CSV as-is for later manual update.

The original tab delimited text file is NOT deleted, for later verification of the conversion.

## Script Argument
update_dir: the path to the backlogged or closed folder, which is organized collection/accession/preservation_log.txt
