<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/45XhXmG.png" alt="Project logo"></a>
</p>

<h2 align="center">Zalando Scraper</h2>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/notscar/zalando-scraper.svg)](https://github.com/NotScar/zalando-scraper/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/notscar/zalando-scraper.svg)](https://github.com/NotScar/zalando-scraper/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
</div>

---

<p align="center"> As the name says this script is used to fetch all the incoming releases for the popular marketplace <a href="https://zalando.com">Zalando</a>
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>

This project started when I saw simple scripts like this, being sold for over 200€ in the reselling / hypebeast community, and in less than a day the repository started already to attract a lot of people.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will guide you through the installation of the script

## 🧰 Prerequisites

```
Python 3.9
Laster PIP Version
Discord Webhooks
```

## 💻Installing

```
pip install -r requirements.txt
```
Insert your webhook(s) in the first lines of the `main.py` script
```
py main.py
```

## 🎈 Usage <a name="usage"></a>

The script must be used with Python 3.x, preferably Python 3.9

## 🚀 Deployment <a name = "deployment"></a>

The script itself it's very light-weight takes an average of 60 MB of RAM, and less than 2 MBPS

## ⛏️ Built Using <a name = "built_using"></a>

- [Python 3.9](https://www.python.org/) - Main Language
- [CFScrape](https://pypi.org/project/cfscrape/) - Library for headers automation
- [BeautifulSoup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) - Extraction of content from HTML Pages

## 📒 TODO
- [X] Extend Logs to external file and discord webhook
- [ ] Allow the loop to use multiple countries at once without overlapping articles 
- [ ] Extend the script to auto-checkout articles with selenium

## ✍️ Authors <a name = "authors"></a>

- [@NotScar](https://github.com/NotScar) - Idea & Initial work

## 📸 Screenshots

![DWS](https://i.imgur.com/7vnSHfe.png)
![DWS](https://i.imgur.com/RPaGxgQ.png)
![DWS](https://i.imgur.com/cpGlxUd.png)