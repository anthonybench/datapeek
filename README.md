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

<br />

## **Get Started 🚀**
<hr>

```sh
pip install sleepydatapeek
pip install --upgrade sleepydatapeek

python -m sleepydatapeek my_data.csv
python -m sleepydatapeek --help
```

<br />

## **Usage ⚙**
<hr>

Fetch dependencies:
```sh
pip install -r requirements.txt
```

Set a function in your shell environment to run a script like:
```sh
alias datapeek='python -m sleepydatapeek'
```

Presuming you've named said function `datapeek`, print the help message:
```sh
datapeek --help
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

<!-- / -->
See [License](LICENSE) for the full license text.

This package was authored by *Isaac Yep*.