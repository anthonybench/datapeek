#!/usr/bin/env python

'''README
Usage:
  # pip install sleepydatapeek
  # pip install --upgrade sleepydatapeek

  from sleepydatapeek import sleepydatapeek
  from sys import argv, exit

  sleepydatapeek(argv[1:])
  exit(0)
'''

# stdlib
from sys import exit
# custom
from toolchain.commands import datapeek_logic
# 3rd party
try:
  import typer
except ModuleNotFoundError as e:
  print("Error: Missing one or more 3rd-party packages (pip install).")
  exit(1)


def sleepydatapeek(input_path:str, output_path:str='') -> str:
  app = typer.Typer()
  @app.command()
  def datapeek(input_path:str, output_path:str='') -> str:
    '''Data Peek

    Get a summary of the contents of a data file quickly.

    ───Params
    input_path:str :: local datafile path
    output_path:str :: path to write to, else print to console

    ───Return
    str :: formatted summary with tabulated sample
    '''
    return datapeek_logic(input_path, output_path)
  if (__name__ == 'sleepydatapeek') or (__name__ == '__main__'):
    app()


## Local Testing
# sleepydatapeek(argv)
