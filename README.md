# LinkJP Scorer

A scorer for [SHINRA2021-LinkJP Task](http://shinra-project.info/shinra2021linkjp/).

## Usage

```
usage: linkjp_scorer [-h] [--format {csv,table}] [--ignore-link-type] [--output OUTPUT] {airport,city,company,compound,conference,lake,person} gold answer

positional arguments:
  {airport,city,company,compound,conference,lake,person}
                        target category.
  gold                  filepath to gold annotation data.
  answer                filepath to answer data.

optional arguments:
  -h, --help            show this help message and exit
  --format {csv,table}  specify output format.
  --ignore-link-type    ignore link_type on evaluation, and eveluate only with link_page_id.
  --output OUTPUT       write output to the specified path.
```

### Example Usage

Clone this repository into your local working directory.

```
$ git clone https://github.com/usami/linkjp_scorer.git
```

Download a sample data from [the task page](http://shinra-project.info/shinra2021linkjp/),
and run the scorer against the baseline data.

```
$ python linkjp_scorer airport --ignore-link-type path-to-sample-data/link_annotation/Airport.json linkjp_scorer/data/baseline/airport.json
precision  recall  f1-score  attribute
    0.000   0.000     0.000  別名
    0.000   0.000     0.000  旧称
    1.000   0.793     0.885  国
    1.000   0.298     0.459  所在地
    1.000   0.583     0.737  母都市
    1.000   0.464     0.634  近隣空港
    0.929   0.591     0.722  運営者
    1.000   1.000     1.000  名前の謂れ
    0.000   0.000     0.000  名称由来人物の地位職業名
    0.659   0.414     0.509  macro-average
    0.986   0.324     0.488  micro-average
```

## Use as a Python Module

You can use this as a Python module inside your code.

Place the entire directory onto the same layer of your code.

```
linkjp_scorer/
main.py
```

Then you can import the module with the following line:

```
import linkjp_scorer
```

### Example Usage

```Python:main.py
import linkjp_scorer

if __name__ == '__main__':
    scorer = linkjp_scorer.Scorer(linkjp_scorer.Category.AIRPORT,
                                  'linkjp-sample-210315/link_annotation/Airport.json', 'linkjp_scorer/data/baseline/airport.json')
    scorer.calc_score()
    scorer.print_score()
```
