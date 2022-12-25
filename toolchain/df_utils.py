import pandas as pd
from sys import exit

# Utility: read csv
def preview_csv(data_format: str, limit: int, input_path: str) -> object:
  '''Takes raw csv file and outputs limited dataframe'''
  try:
    df = pd.read_csv(input_path, encoding='unicode_escape', header=None)
    return df.head(limit)
  except Exception as e:
    print(f"Error reading {data_format} file:\n{e}")
    exit(1)

# Utility: read parquet
def preview_parquet(data_format: str, limit: int, input_path: str) -> object:
  '''Takes raw parquet file and outputs limited dataframe'''
  try:
    df = pd.read_parquet(input_path)
    return df.head(limit)
  except Exception as e:
    print(f"Error reading {data_format} file:\n{e}")
    exit(1)

# Utility: read excel
def preview_excel(data_format: str, limit: int, input_path: str) -> object:
  '''Takes raw excel file and outputs limited dataframe'''
  try:
    df = pd.read_excel(input_path, header=None)
    return df.head(limit)
  except Exception as e:
    print(f"Error reading {data_format} file:\n{e}")
    exit(1)

# Utility: read json
def preview_json(data_format: str, limit: int, input_path: str) -> object:
  '''Takes raw json file and outputs limited dataframe'''
  try:
    df = pd.read_json(path_or_buf=input_path)
    return df.head(limit)
  except Exception as e:
    print(f"Error reading {data_format} file:\n{e}")
    exit(1)
