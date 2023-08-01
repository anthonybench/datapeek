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

```sh
pip install sleepydatapeek
pip install --upgrade sleepydatapeek
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
# pip install sleepydatapeek
# pip install --upgrade sleepydatapeek

from sleepydatapeek import sleepydatapeek
from sys import argv, exit

sleepydatapeek(argv[1:])
exit(0)
```

Presuming you've named said function `emoji`, print the help message:
```sh
sleepydatapeek --help
```

<br />

## **Technologies 🧰**
<hr>

  - [Pandas](https://pandas.pydata.org/docs/)
  - [Tabulate](https://pypi.org/project/tabulate/)
  - [Typer](https://typer.tiangolo.com/)

<br />

## **Contribute 🤝**
<hr>

If you have opinions, submit a PR 😊.

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
See [License](LICENSE) for the full license text.

This package was authored by *Isaac Yep*.