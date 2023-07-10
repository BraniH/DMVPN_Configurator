import os
import openpyxl
import pypandoc
from Clean_config import CleanConfig


def get_cells(sheet):
    merged_unmerged_dict = {}

    # Get the merged cell ranges
    merged_ranges = sheet.merged_cells.ranges

    # Initialize the current merged key and unmerged values list
    current_merged_key = None
    unmerged_values = []

    # Iterate over the cells in columns A and B
    for row in sheet.iter_rows(min_row=1, min_col=1, max_col=2):
        cell_A, cell_B = row

        # Check if the cell is part of any merged range
        is_merged = False

        for merged_range in merged_ranges:
            if cell_A.coordinate in merged_range or cell_B.coordinate in merged_range:
                is_merged = True
                # Extract the value from the merged cell
                merged_value = merged_range.start_cell.value

                # If a new merged key is encountered, update the current merged key and create a new list for unmerged values
                if merged_value != current_merged_key:
                    if current_merged_key is not None:
                        merged_unmerged_dict[current_merged_key] = unmerged_values
                    current_merged_key = merged_value
                    unmerged_values = []

                break

        # Check if the row has more than one cell
        if not is_merged and cell_B.value is not None:
            # Add the value of cell A as key and value of cell B as the value in the dictionary
            unmerged_values.append({str(cell_A.value): cell_B.value})

    # Add the last set of unmerged values to the dictionary
    if current_merged_key is not None:
        merged_unmerged_dict[current_merged_key] = unmerged_values

    return merged_unmerged_dict


def parse_excel(filename, sheet_name):
    # Get the full file path
    path = os.path.join(os.getcwd(), filename)

    # Open the Excel file
    workbook = openpyxl.load_workbook(path)

    # Select the specified sheet
    sheet = workbook[sheet_name]

    # Get merged cells and unmerged cells dictionary
    merged_unmerged_dict = get_cells(sheet)
    print(merged_unmerged_dict)

    return merged_unmerged_dict


def transform_to_txt(docx_file):
    txt_file = docx_file.rsplit(".", 1)[0] + ".txt"  # Generate the output .txt file path

    # Convert .docx to .txt using Pandoc
    pypandoc.convert_file(docx_file, 'plain', outputfile=txt_file, format='docx')

    print(f"Conversion complete. Text saved to {txt_file}")



if __name__ == "__main__":


    ''' Transform the config docx file to txt. '''
    standard_config = "\\Config\\DMVPN - Copy.docx"
    standard_config_txt=transform_to_txt(os.getcwd() + standard_config)

    ''' Parse the setup.xlsx to a dictionary '''
    setup = "setup.xlsx"
    setup_config = parse_excel(setup, "Main Info")
    
    
    ''' Clear DMVPN config - only parts which are required will remain '''
    CleanConfig(os.getcwd() + standard_config.replace("docx", "txt"), setup_config)
  
  
    ''' Parsing values into the config '''
    
    











