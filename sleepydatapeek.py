#!/usr/bin/env python3
#===================================
# DataPeek; datafile previewer
#
#   - Isaac Yep
#===================================
mainDocString = '''
This tool takes an input file path and outputs a limited dataframe to either stdout or a markdown file.
'''

#---Dependencies---------------
# stdlib
from sys import argv, exit, getsizeof
from typing import List
from subprocess import run
# custom modules
from toolchain.option_utils import usageMessage, checkListOverlap, verifyOption, getOptionVal, stripOptionVals
from toolchain.df_utils import preview_csv, preview_parquet, preview_excel, preview_json
# 3rd party
try:
  from IPython.display import display
  from yaml import safe_load, YAMLError
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)

#---Entry----------------------
def sleepydatapeek(*userArgs):
  userArgs = argv[1:]
  minArgs  = 1
  maxArgs  = 4
  options  = { # ['--takes-arg=', 'int'|'str'],
    'help'   : ['-h', '--help'],
    'format' : ['--format=', 'str'],
    'path'   : ['--path=',   'str'],
    'output' : ['--output=', 'str'],
    'limit'  : ['--limit=',  'int'],
  }
  default_limit = 20
  ## Invalid number of args
  if len(userArgs) < (minArgs) or len(userArgs) > (maxArgs):
    usageMessage(f"Invalid number of options in: {userArgs}\nPlease read usage.")
    exit(1)
  ## Invalid option
  if (len(userArgs) != 0) and not (verifyOption(userArgs, options)):
    usageMessage(f"Invalid option(s) entered in: {userArgs}\nPlease read usage.")
    exit(1)
  ## Help option
  if checkListOverlap(userArgs, options['help']):
    print(mainDocString, end='')
    usageMessage()
    exit(0)
  else:
    output_flag = False
    output_path = ''
    limit = 1
    # Check and parse user args
    try:
      data_format = getOptionVal(userArgs, options['format'])
      input_path  = getOptionVal(userArgs, options['path'])
      if [i for i in userArgs if options['output'][0] in i] != []:
        output_path, output_flag = getOptionVal(userArgs, options['output']), True
      if [i for i in userArgs if options['limit'][0] in i] != []:
        limit = getOptionVal(userArgs, options['limit'])
      else:
        limit = default_limit
    except Exception as e:
      print(f"Error parsing arguments:\n{e}")
      exit(1)
    # CSV
    if data_format.lower() == 'csv':
      result = preview_csv('csv', limit, input_path)
      if output_flag:
        try:
          result.to_markdown(buf=output_path, mode='a')
        except Exception as e:
          print(f"Error writing output:\n{e}")
          exit(1)
      else:
        display(result)
      exit(0)
    # PARQUET
    if data_format.lower() == 'parquet':
      result = preview_parquet('parquet', limit, input_path)
      if output_flag:
        try:
          result.to_markdown(buf=output_path, mode='a')
        except Exception as e:
          print(f"Error writing output:\n{e}")
          exit(1)
      else:
        display(result)
    # EXCEL
    if (data_format.lower() == 'excel') or (data_format.lower() == 'xlsx') or (data_format.lower() == 'xls'):
      result = preview_excel('excel', limit, input_path)
      if output_flag:
        try:
          result.to_markdown(buf=output_path, mode='a')
        except Exception as e:
          print(f"Error writing output:\n{e}")
          exit(1)
      else:
        display(result)
    # JSON
    if (data_format.lower() == 'json'):
      result = preview_json('json', limit, input_path)
      if output_flag:
        try:
          result.to_markdown(buf=output_path, mode='a')
        except Exception as e:
          print(f"Error writing output:\n{e}")
          exit(1)
      else:
        display(result)

    exit(1)
