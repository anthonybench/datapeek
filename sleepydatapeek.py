#!/usr/bin/env python

'''README

Usage:
  ./sleepydatapeek.py <path> [options]
'''

import typer
from sleepydatapeek_toolchain.command_logic import main

if __name__ == "__main__":
  typer.run(main)