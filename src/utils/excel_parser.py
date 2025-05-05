import pandas as pd

def parse_excel(file_path):
    """
    Parses an Excel file and extracts financing plan data.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        DataFrame: A pandas DataFrame containing the financing plan data.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None