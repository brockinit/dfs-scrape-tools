# DFS Scrape Tools
A collection of web scrapers for obtaining NFL stats and fantasy data
* * *

## Basic Usage

* `pip install dfs-scrape-tools`

* By default, `dfs-scrape-tools` will write the files to the CWD
```python
import dfs-scrape-tools

options = {
    'years': [2011, 2015],
    'weeks': [1, 4, 7],
    'game': 'fd'
}

dfs-scrape-tools.roto_guru(options)
```
