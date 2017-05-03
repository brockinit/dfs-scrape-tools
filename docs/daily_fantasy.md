## daily_fantasy

### Source
* This function obtains data from [Roto Guru](http://rotoguru1.com/)
* The possible data options include Fanduel, Draft Kings, and Yahoo

### Arguments
* `options` :: `(required)` :: `{Dict}` :: The keys dictate which data is scraped.
Defaults to:
```python
{
  years: [2011, 2012, 2013, 2014, 2015, 2016],
  weeks: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
  game: 'fd'  # other options include 'dk' and 'yh'
}
```

### Example

```python
from interscraped import daily_fantasy

'''

Scrapes **all Fanduel data** from the 2012 and 2014 season, weeks 1, 2, and 3

'''

daily_fantasy({ 'years': [2012, 2014], 'weeks': [1, 2, 3], 'game': 'fd' })
```
