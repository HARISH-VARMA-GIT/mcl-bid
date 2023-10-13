import requests
import tabula
import pandas as pd
from io import BytesIO

def process_table_cell(cell):
    # Check if the cell is a string
    if isinstance(cell, str):
        # Replace newline characters with spaces and remove any extra spaces
        return cell.replace('\r', ' ').strip()
    else:
        return cell

def compare(filepath):
    pdf_url = filepath
    response = requests.get(pdf_url)
    pdf_file = BytesIO(response.content)
    
    try:
        tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True, area=[124, 40, 800, 900])
    except Exception as e:
        print("Error extracting tables:", e)
        return
    
    dataframes = []
    
    for table in tables:
        # Process table cells to replace newlines with spaces
        processed_table = [[process_table_cell(cell) for cell in row] for row in table.values]
        df = pd.DataFrame(processed_table, columns=table.columns)
        dataframes.append(df)
    
    combined_dataframe = pd.concat(dataframes, ignore_index=True)

    #print(combined_dataframe)
    combined_dataframe.iloc[:, 1] = combined_dataframe.iloc[:, 1].str.replace(" ", "")
    combined_dataframe.iloc[:, 2] = combined_dataframe.iloc[:, 2].str.replace(" ", "")

    # Exclude first and last rows
    data_to_compare = combined_dataframe.iloc[1:-1]

    print(data_to_compare)

    # Initialize a list to store unsatisfied specifications
    unsatisfied_specifications = []

    # Get column indices
    specification_index = 0
    bid_requirement_index = 1
    offered_index = 2

    # Compare Bid Requirement and Offered columns for each specification
    for idx, row in data_to_compare.iterrows():
        if idx==1:
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


compare("https://res.cloudinary.com/dvxhxquyh/image/upload/v1693124799/ODISHA_TRAVELS_kgpt4b.pdf")
    

