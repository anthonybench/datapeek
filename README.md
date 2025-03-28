# **sleepydatapeek**
*A quick way to peek at local datafiles.*

<br />

## **Welcome to sleepydatapeek!**
One often needs to spit out a configurable preview of a data file. It would also be nice if said tool could detect and read several formats automatically.\
**`sleepydatapeek`** has entered the chat!

Quickly summarize data files of type:
- `csv`
- `parquet`
- `json`
- `pkl`
- `xlsx`

> ℹ️ Note that this tool presumes format by file extension. If you leave out extensions, or give csv data a `.json` extension for funsies, then you're being silly.

<br />

## **Get Started 🚀**
<hr>

```sh
pip install sleepydatapeek
pip install --upgrade sleepydatapeek

python -m sleepydatapeek --help
python -m sleepydatapeek my_data.csv
```

<br />

## **Usage ⚙**
<hr>

Set a function in your shell environment to run a script like:
```sh
alias datapeek='python -m sleepydatapeek'
```

Presuming you've named said function `datapeek`, print the help message:
```sh
$ datapeek test.xlsx

════════════════════ test.xlsx ════════════════════
      Unnamed: 0    CustomerID  ProductName      Quantity  OrderDate      Price
--  ------------  ------------  -------------  ----------  -----------  -------
 0             0           101  Laptop                  2  2023-10-26      1200
 1             1           102  Mouse                   1  2023-10-26        25
 2             2           103  Keyboard                1  2023-10-27        50
 3             3           104  Monitor                 1  2023-10-27       300
 4             4           105  Headphones              3  2023-10-28        80

═══Summary Stats
╭──────────────┬─────────────────╮
│ Index Column │ (no_name):int64 │
├──────────────┼─────────────────┤
│ Row Count    │ 30              │
├──────────────┼─────────────────┤
│ Column Count │ 6               │
├──────────────┼─────────────────┤
│ Memory Usage │ < 0.00 bytes    │
╰──────────────┴─────────────────╯

═══Schema
╭─────────────┬────────╮
│ Unnamed: 0  │ int64  │
├─────────────┼────────┤
│ CustomerID  │ int64  │
├─────────────┼────────┤
│ ProductName │ object │
├─────────────┼────────┤
│ Quantity    │ int64  │
├─────────────┼────────┤
│ OrderDate   │ object │
├─────────────┼────────┤
│ Price       │ int64  │
╰─────────────┴────────╯
═══════════════════════════════════════════════════

```

Optionally, you can also get group-by counts for distinct values of a given column:
```sh
datapeek test.xlsx --groupby-count-column=ProductName

# typical output (elided)

═══Groupby Counts
  (row counts for distinct values of ProductName)
╭──────────────┬───╮
│ Laptop       │ 3 │
├──────────────┼───┤
│ Mouse        │ 3 │
├──────────────┼───┤
│ Keyboard     │ 3 │
├──────────────┼───┤
│ Monitor      │ 3 │
├──────────────┼───┤
│ Headphones   │ 3 │
├──────────────┼───┤
│ USB Drive    │ 3 │
├──────────────┼───┤
│ Printer      │ 3 │
├──────────────┼───┤
│ Webcam       │ 3 │
├──────────────┼───┤
│ Speakers     │ 3 │
├──────────────┼───┤
│ External HDD │ 3 │
╰──────────────┴───╯
═══════════════════════════════════════════════════

```

<br />

## **Technologies 🧰**
<hr>

  - [Pandas](https://pandas.pydata.org/docs/)
  - [Tabulate](https://pypi.org/project/tabulate/)
  - [Typer](https://typer.tiangolo.com/)
  - [PyArrow](https://arrow.apache.org/docs/python/index.html)
  - [openpyxl](https://pypi.org/project/openpyxl/)

<br />

## **Contribute 🤝**
<hr>

If you have thoughts on how to make the tool more pragmatic, submit a PR 😊.

To add support for more data/file types:
1. append extension name to `supported_formats` in `sleepydatapeek_toolchain.params.py`
2. add detection logic branch to the `main` function in `sleepydatapeek_toolchain/command_logic.py`
3. update this readme

<br />

## **License, Stats, Author 📜**
<hr>

<img align="right" alt="example image tag" src="https://i.imgur.com/jtNwEWu.png" width="200" />

<!-- badge cluster -->
![PyPI - License](https://img.shields.io/pypi/l/sleepydatapeek?style=plastic)
![PyPI - Version](https://img.shields.io/pypi/v/sleepydatapeek)
![GitHub repo size](https://img.shields.io/github/repo-size/anthonybench/datapeek)
<!-- / -->

See [License](LICENSE) for the full license text.

This package was authored by *Isaac Yep*.