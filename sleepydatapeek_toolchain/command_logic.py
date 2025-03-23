from pathlib import Path, PurePosixPath
from sys import exit
import pandas as pd
from sleepydatapeek_toolchain.params import *
from sleepydatapeek_toolchain.utils import *


def main(input_path:str, groupby_count_column:str=None):
  '''✨sleepydatapeek✨
  
  A simple tool to summarize the contents of a datafile.
  '''

  path_object = Path(input_path)
  format = PurePosixPath(input_path).suffix.lower()[1:]

  # guards
  if not path_object.exists():
    print(f'Error. Path {input_path} does not exist.')
    exit(1)
  elif not path_object.is_file():
    print(f'Error. Path {input_path} is not a file.')
    exit(1)
  elif format not in supported_formats:
    print(f'Error. Format not supported, must be one of: {", ".join(supported_formats)}')
    exit(1)

  # load
  match format:
    case 'csv':
      df = pd.read_csv(input_path)
    case 'parquet':
      df = pd.read_parquet(input_path)
    case 'json':
      try:
        df = pd.read_json(input_path)
      except Exception as e:
        print(f'Error. JSON not formatted as pandas expects.\n{e}')
        exit(1)
    case 'pkl':
      df = pd.read_pickle(input_path)
    case 'xlsx':
      df = pd.read_excel(input_path, engine='openpyxl')

  # display
  print(summarizeDataframe(
    df,
    filename=path_object.name,
    groupby_count_column=groupby_count_column
  ))