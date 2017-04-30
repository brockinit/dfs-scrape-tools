# DFS Scrape Tools
A collection of web scrapers for obtaining NFL stats and fantasy data
* * *

## Documentation

* Can be found [here](https://github.com/brockinit/dfs-scrape-tools/tree/master/docs)

## Basic Usage

* `pip install interscraped`

* By default, `interscraped` will write the files to the CWD
```python
import interscraped

options = {
    'years': [2011, 2015],
    'weeks': [1, 4, 7],
    'game': 'fd'
}

interscraped.daily_fantasy(options)
```