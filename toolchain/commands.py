# stdlib
from pathlib import Path, PurePosixPath
from sys import exit
import pandas as pd
# custom
from toolchain.utils import *
# 3rd party
try:
  from yaml import safe_load, YAMLError
  from IPython.display import display
  from tabulate import tabulate
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


#───Commands─────────────────
def datapeek_logic(input_path:str, output_path:str='') -> str:
  '''builds and delivers payload string'''

  supported_formats = [
    'csv',
    'parquet',
    'json',
    'tsv'
  ]
  limit = 5

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
    print(f'Error. Format not supported.')
    exit(1)

  # load
  if format == 'csv':
    df = pd.read_csv(input_path)
  elif format == 'parquet':
    df = pd.read_parquet(input_path)
  elif format == 'json':
    try:
      df = pd.read_json(input_path)
    except Exception as e:
      print(f'Error. JSON not formatted as pandas expects.\n{e}')
      exit(1)
  elif format == 'tsv':
    df = pd.read_csv(input_path, sep='\t')
  
  # prepare metadata
  res = f'''{input_path}\n───\nRow count    : {len(df.index)}
Column count : {len(df.columns)}\n───\n{df.dtypes}\n───\n'''

  # prepare sample
  df = df.sample(limit)
  res += tabulate(df, headers=[str(i) for i in df.columns])

  # deliver
  if output_path:
    try:
      with open(output_path, 'w') as target:
        target.write(res)
    except Exception as e:
      print(f'Error in writing to {output_path}.\n{e}')
  else:
    print(res)

  return res
