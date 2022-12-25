# **DataPeek**
*A quick way to peek at local datafiles.*

<br />

## **Welcome to sleepydatapeek!**
In short, it's hand to have something be able to spit out a configurable preview of data from a file, and bonus points if you can just as easily output in markdown. It would also be nice if said tool could read all the formats.\
**DataPeek** has entered the chat!

<br />

### **Table of Contents** 📖
<hr>

  - **Get Started**
  - Usage
  - Technologies
  - Contribute
  - Acknowledgements
  - License/Stats/Author

<br />

## **Get Started 🚀**
<hr>

This repo is currently private, so adding this package is all the user needs to care about.

<br />

## **Usage ⚙**
<hr>

After setting up the tool, run `./sleepydatapeek.py [-h|--help]` to display this message:
```txt
This tool takes an input file path and outputs a limited dataframe to either stdout or a markdown file.


Limit defaults to 20 rows, and can be overwritten.
Format value has synonyms 'xlsx' and 'xls'
--------------
Usage:
  ./sleepydatapeek.py --format=[parquet|csv|json|excel] --path=<path> [--output=<path>] [--limit=<row-limit>]
Examples:
  ./sleepydatapeek.py --format=csv --path=sample-data/data.csv
  ./sleepydatapeek.py --format=csv --path=sample-data/data.csv --limit=6
  ./sleepydatapeek.py --format=csv --path=sample-data/data.csv --output=results.md
Info:
  ./sleepydatapeek.py [-h|--help]
--------------
```

<br />

## **Technologies 🧰**
<hr>

  - [Pandas](https://pandas.pydata.org/docs/)

<br />

## **Contribute 🤝**
<hr>

As stated in the welcome section, the corresponding GitHub repo is private. \
However, feel free to [reach out with opinions](https://github.com/anthonybench)!

<br />

## **Acknowledgements 💙**
<hr>

Cheers to the chaos of modern life for needing personalized agility in schema assessment.

<br />

## **License, Stats, Author 📜**
<hr>

<img align="right" alt="example image tag" src="https://i.imgur.com/jtNwEWu.png" width="200" />

<!-- badge cluster -->

![PyPI - License](https://img.shields.io/pypi/l/sleepydatapeek?style=plastic)

<!-- / -->
See [License](TODO) for the full license text.

This package was authored by *Isaac Yep*.