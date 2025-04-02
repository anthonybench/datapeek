import pandas as pd
from pathlib import Path
from rich import print
import os
from tabulate import tabulate
import PyPDF2
from sleepydatapeek_toolchain.params import *


def errorMessage(message:str) -> None:
  '''log error message'''
  print(f'[bold][red]Error[/bold]. {message}[/red]')


def _formatMemory(bytes:float) -> str:
  '''returns presentable string'''
  if bytes > 0.00:
    return '< 0.00 bytes'

  units = ['bytes', 'KB', 'MB', 'GB']
  size = bytes
  unit_index = 0

  while size >= 1024 and unit_index < len(units) - 1:
    size /= 1024.0
    unit_index += 1

  return f'{size:.2f} {units[unit_index]}'


def _showSampleData(df:pd.DataFrame, limit:int, max_terminal_width:int=None) -> str:
  '''Show Sample Data
  Display a sample of the dataframe.

  ───Params
  df:pd.DataFrame :: dataframe to inspect
  limit:int :: number of rows to display
  max_terminal_width:int :: terminal width

  ───Return
  str :: string to display
  '''
  if max_terminal_width is None:
    try:
      max_terminal_width = os.get_terminal_size().columns
    except OSError:
      max_terminal_width = default_max_terminal_width

  # don't elide if <= 2 columns
  if len(df.columns) <= 2:
    return tabulate(df.head(limit), headers='keys', tablefmt=sample_data_table_type)

  # print simply if small enough
  col_widths = [max(len(str(val)) for val in df[col].astype(str).head(limit).tolist() + [col]) + 2 for col in df.columns]
  total_width = sum(col_widths)
  if total_width <= max_terminal_width:
    return tabulate(df.head(limit), headers='keys', tablefmt=sample_data_table_type)

  # elide columns
  available_width = max_terminal_width - 6 # account for elision string
  visible_cols = 0
  visible_width = 0
  for width in col_widths:
    if visible_width + width > available_width/2:
      break
    visible_width += width
    visible_cols += 1
  if visible_cols < 2:
    visible_cols = 2
  first_cols = df.columns[:visible_cols]
  last_cols = df.columns[-visible_cols:]
  elided_df = pd.concat([df[first_cols], pd.Series(['...'] * len(df), index=df.index, name='...'), df[last_cols]], axis=1)

  return tabulate(elided_df.head(limit), headers='keys', tablefmt=sample_data_table_type)


def summarizeDataframe(
  df:pd.DataFrame,
  filename:str,
  groupby_count_column:str=None
) -> str:
  '''Summarize Dataframe
  
  Get summary info on pandas dataframe.

  ───Params
  df:pd.DataFrame :: dataframe to inspect
  filename:str :: filename, for display purposes
  groupby_count_column:str :: optional column name to run groupby counts on

  ───Return
  str :: string to display
  '''
  payload = ''
  header = f'{"═"*20} {filename} {"═"*20}'
  section_border = '═'*3

  payload += f'\n{header}\n'
  payload += f'[bold green]{_showSampleData(df, default_sample_output_limit)}[/bold green]'
  
  payload += f'\n\n[bold green]{section_border}Summary Stats[/bold green]\n'
  memory_usage = df.memory_usage(deep=True).sum() / (1024*1024)
  formatted_memory = _formatMemory(memory_usage)
  payload += tabulate([
    ['Index Column', f'{"(no_name)" if not df.index.name else df.index.name}:{df.index.dtype}'],
    ['Row Count', len(df.index)],
    ['Column Count', len(df.columns)],
    ['Memory Usage', formatted_memory]
  ], tablefmt=metadata_table_type)

  payload += f'\n\n[bold green]{section_border}Schema[/bold green]\n'
  schema = df.dtypes.apply(lambda x: x.name).to_dict()
  payload += tabulate(
    [[name, dtype] for name, dtype in schema.items()],
    tablefmt=metadata_table_type)

  if groupby_count_column:
    try:
      payload += f'\n\n{section_border}Groupby Counts\n'
      counts_dict = df[groupby_count_column].value_counts().to_dict()
      payload += f'  (row counts for distinct values of {groupby_count_column})\n'
      payload += tabulate(
        [[name, count] for name, count in counts_dict.items()],
        tablefmt=groupby_counts_table_type)
    except KeyError:
      column_names_formatted = '\n- '.join(df.columns)
      payload += f"❗ Error. Column '{groupby_count_column}' not found in data file. Choose one of:\n- {column_names_formatted}"

  payload += f'\n{"═"*len(header)}\n'
  return payload


def getPDFMetadata(pdf_path:Path) -> None:
  '''prints pdf document metadata'''
  filename = pdf_path.name
  plain_path = str(pdf_path)
  try:
    reader = PyPDF2.PdfReader(plain_path)
    metadata = reader.metadata
    metadata_table_list = [[f'{k.lstrip("/")}',v] for k,v in metadata.items()]
    metadata_table_list.append(['Length', f'{len(reader.pages)} pages'])
    tabulated_metadata = tabulate(metadata_table_list, tablefmt=metadata_table_type)
    return f'\n[green]📄 {filename}[/green]\n{tabulated_metadata}\n'
  except Exception as e:
    errorMessage(f'Failed to read metadata from supposed pdf file: {plain_path}\n{e}')
