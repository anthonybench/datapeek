from pathlib import Path, PurePosixPath
from rich import print
from sys import exit
import pandas as pd
from sleepydatapeek_toolchain.params import *
from sleepydatapeek_toolchain.utils import *


def main(input_path:str, groupby_count_column:str=None):
  '''✨sleepydatapeek✨
  
  A minimal tool to summarize the data or metadata of a file.
  '''
  path_object = Path(input_path)
  format = PurePosixPath(input_path).suffix.lower()[1:]

  # guards
  if not path_object.exists():
    errorMessage(f'Path {input_path} does not exist.')
    exit(1)
  elif not path_object.is_file():
    errorMessage(f'Path {input_path} is not a file.')
    exit(1)
  elif format not in supported_formats:
    errorMessage(f'Format not supported, must be one of: {", ".join(supported_formats)}')
    exit(1)
  elif supported_formats[format] == 'metadata' and groupby_count_column:
    errorMessage(f'Groupby count column not supported for metadata type.')
    exit(1)

  # load (datafiles only)
  type = supported_formats[format]
  if type == 'data':
    match format:
      case 'csv':
        df = pd.read_csv(input_path)
      case 'parquet':
        df = pd.read_parquet(input_path)
      case 'json':
        try:
          df = pd.read_json(input_path)
        except Exception as e:
          errorMessage(f'JSON not formatted as pandas expects.\n{e}')
          exit(1)
      case 'pkl':
        df = pd.read_pickle(input_path)
      case 'xlsx':
        df = pd.read_excel(input_path, engine='openpyxl')

  # display
  match type:
    case 'data':
      print(summarizeDataframe(
        df,
        filename=path_object.name,
        groupby_count_column=groupby_count_column
      ))
    case 'metadata' if format == 'pdf':
      print(f'[white]{getPDFMetadata(pdf_path=path_object)}[/white]')
    case 'metadata' if format == 'png':
      print(f'\n[green]🖼️ {path_object.name}[/green]')
      print(getPNGMetadata(image_path=path_object))
      print()
    case 'metadata' if format in ['jpg', 'jpeg']:
      print(getJPGMetadata(image_path=path_object))