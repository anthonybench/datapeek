#!/usr/bin/env python

'''README

Usage:
  ./sleepydatapeek.py <path> [options]
'''

import typer
from sleepydatapeek_toolchain.functions import *

if __name__ == "__main__":
  typer.run(main)