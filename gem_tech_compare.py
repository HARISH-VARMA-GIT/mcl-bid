import requests
import tabula
import pandas as pd
from io import BytesIO

#pd.set_option("display.max_columns", None)
#pd.set_option("display.width", None)

# URL of the PDF file
pdf_url = "https://res.cloudinary.com/dvxhxquyh/image/upload/v1692598089/ANANTA_SALES_ekgrpu.pdf"

# Send a GET request to the PDF URL
response = requests.get(pdf_url)

# Create a file-like object from the PDF content
pdf_file = BytesIO(response.content)

# Extract tabular data from the PDF using tabula
tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)

# Initialize an empty DataFrame
dataframes = []

# Convert each table into a DataFrame
for table in tables:
    df = pd.DataFrame(table)
    dataframes.append(df)

# Assuming you want to combine all tables into one DataFrame
combined_dataframe = pd.concat(dataframes, ignore_index=True)

#print(combined_dataframe)
combined_dataframe.iloc[:, 1] = combined_dataframe.iloc[:, 1].str.replace(" ", "")
combined_dataframe.iloc[:, 2] = combined_dataframe.iloc[:, 2].str.replace(" ", "")

# Exclude first and last rows
data_to_compare = combined_dataframe.iloc[1:-1]

# Initialize a list to store unsatisfied specifications
unsatisfied_specifications = []

# Get column indices
specification_index = 0
bid_requirement_index = 1
offered_index = 2

# Compare Bid Requirement and Offered columns for each specification
for idx, row in data_to_compare.iterrows():
    if row[specification_index] == "Type of car (Please select at least 3 options)":
        bid_cars = row[bid_requirement_index].replace(',', '').replace(' ', '')
        offered_cars = row[offered_index].replace(',', '').replace(' ', '')
        if not offered_cars in bid_cars:
            unsatisfied_specifications.append(row[specification_index])
    elif row[bid_requirement_index] != row[offered_index]:
        unsatisfied_specifications.append(row[specification_index])

# Check if any specifications are unsatisfied
if not unsatisfied_specifications:
    print("Satisfied: All specifications have matching Bid Requirement and Offered values.")
else:
    print("Not Satisfied: Specifications with mismatched Bid Requirement and Offered values:", unsatisfied_specifications)



