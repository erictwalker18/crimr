''' populations2tablerows.py

    A script for converting the city data in "Baltimore,14,26,47..." form into
    rows that match the populations table structure "Baltimore,1790,14",
    "Baltimore,1800,26", etc.
'''

import csv
import sys

orig = open("dataset_with_the_useful_columns.csv", "r")
result = open("python_cleaned_csv.csv", "w")

reader = csv.reader(orig)
writer = csv.writer(result)

headingRow = reader.next()
writer.writerow(headingRow)

for row in reader:
    # print row
    row[4] = row[4][:10]
    writer.writerow(row)
#     row = map(str.strip, row)
#     assert len(row) == len(headingRow) + 1
#     cities[row[0]] = row[1:]
#
# for city in cities:
#     for k in range(len(headingRow)):
#         cityRow = cities[city]
#         yearString = headingRow[k]
#         populationString = cityRow[k].replace(',', '') # if the CSV numbers have commas in them, delete them
#         if populationString == '':
#             populationString = '0'
#         writer.writerow([city, yearString, populationString])
