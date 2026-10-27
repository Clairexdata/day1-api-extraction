DAY 1: API Data Extraction and Transformation
Project Overview 
This project extracts user data from the JSONPlaceholder API, transforms nested JSON recordsinto a tabular structure and exports the cleaned data to a CSV file.
API Source
https://jsonplaceholder.typicode.com/users
Tools Used 
Python
Requests
Pandas
Pathlib

Approach
Fetch user records from the API.
Inspect the data structure and Python data types
Extract core customer fields
Build lists, tuples, and dictionaries using comprehensions.
Flatten nested JSON objects into a single-level structure.
Convert the flattened records into a Pandas Dataframe.
Export the cleaned data to output

How to run
Install the dependancies:
python -m pip install pandas requests

Run the script from the project directory
python extract_customers.py

Output 
The script generates output/customers_clean.csv containing the extracted users in a tabular format

Assumptions
The API returns a list of user records
Each user record follows the expected JSONPlaceholder structure
Nested dictionaries are flattened using underscores between key names
The Output CSV uses the required column names and order