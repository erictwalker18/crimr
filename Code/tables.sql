# Create the crime table with appropriate columns:
CREATE TABLE crimes (
  crime_id int,
  category text,
  description text,
  dayofweek text,
  date date,
  district text,
  resolution text,
  x real,
  y real
);

# Populate the table using the dataset's CSV file (with headers removed):
\copy crimes FROM '/Accounts/courses/cs257/jondich/web/earleyg/phase2/truncated_data_NoHeaders.csv' DELIMITER ',' CSV
