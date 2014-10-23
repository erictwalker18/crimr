''' CSV Cleaner.py

    In order to make the import into PSQL as painless as possible,we used this script
        to clear out unimportant info from the DATE column of the CSV.

    The column had MM/DD/YYYY along with a timestamp. We had to get rid of everything
        but the MM/DD/YYYY date in order to import it directly into our PSQL date column
        with type 'date'. (Additionally, the timestamp attached to each DATE was trivially
        set at 12:00:00 AM, so it was useless anyway.)

    * More info about important files in this folder *
        - python_cleaned_dates_csv.csv is the output from this program (with cleaned up dates)
        - truncated_data.csv is the next step: we truncated our dataset down due to its massive size
            (we chopped off everything after the 999th entry)
        - truncated_data_NoHeaders.csv is the final product, ready for PSQL importation. As the name
            suggests, it's just truncated_data.csv with the headers removed.
'''

import csv
import sys

# dataset_with_the_useful_columns.csv is our dataset with some unnecessary
#   columns removed (like ADDRESS, TIME, and LOCATION, which was redundant
#   and just combined the info in the x and y columns).
orig = open("dataset_with_the_useful_columns.csv", "r")
result = open("python_cleaned_dates_csv.csv", "w")

reader = csv.reader(orig)
writer = csv.writer(result)

headingRow = reader.next()
writer.writerow(headingRow)

for row in reader:
    # The first ten characters of the date column is the
    #   desired MM/DD/YYYY date:
    row[4] = row[4][:10]
    writer.writerow(row)
