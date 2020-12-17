![CI](https://github.com/nrgeil/programming_assignment/workflows/CI/badge.svg)

# Overview

This program will take two file inputs: A file to parse and a file with a set of words to exclude. It reads through the
provided input file line by line, strips out any special or numerical characters, stems words into their base form
using the [Porter Stemmer Algorithm](https://tartarus.org/martin/PorterStemmer/), and prints out the top `n` words
found.

## Requirements

- The file with the set of words to exclude is expected to have one word per line.
- Python >=3.6. This was developed and tested on 3.8.5, but should work on 3.6 and later. CI job set up to test all
three versions.

## Development Requirements

- [Poetry](https://python-poetry.org/docs/#installation)

## Installation

```shell
pythom -m venv .venv
source .venv/bin/activate
pip install dist/word_parser-0.1.0-py3-none-any.whl
```

## How to run

```shell
Usage: parse_file [OPTIONS]

Options:
  -i, --input-file TEXT           The full path to the source file to parse
                                  [required]

  -r, --rules-file TEXT           The full path to the file with words to
                                  exclude  [required]

  -n, --number-of-results INTEGER
                                  The number of words to return. Defaults to
                                  20

  -c, --use-collections-counter   Use the Counter class from the collections
                                  module instead of custom method

  --help                          Show this message and exit.
```

### Example

```shell
# From the root of the project
parse_file -i $(pwd)/Text1.txt -r $(pwd)/stopwords.txt
```

## Assumptions

- Word frequency based on root form
- Non-alphabetical means anything not covered by the regex pattern '[A-Za-z]'
- Apply stemmer algorithm using Porter Stemmer means use the code provided in the language of choice

## Results

### Text1.txt

| Word         | Occurrences |
|--------------|-------------|
| he           |          18 |
| us           |          11 |
| govern       |          10 |
| peopl        |          10 |
| right        |          10 |
| for          |           9 |
| law          |           9 |
| state        |           9 |
| power        |           8 |
| we           |           8 |
| time         |           6 |
| among        |           5 |
| declar       |           5 |
| establish    |           5 |
| refus        |           5 |
| abolish      |           4 |
| assent       |           4 |
| coloni       |           4 |
| form         |           4 |
| free         |           4 |

### Text2.txt

| Word         | Occurrences |
|--------------|-------------|
| said         |         462 |
| alic         |         401 |
| i            |         400 |
| it           |         208 |
| on           |         158 |
| and          |         130 |
| littl        |         128 |
| the          |         124 |
| you          |         110 |
| look         |         104 |
| like         |          97 |
| know         |          90 |
| that         |          83 |
| went         |          83 |
| go           |          77 |
| thing        |          77 |
| queen        |          76 |
| thought      |          76 |
| time         |          74 |
| sai          |          70 |

## Developing

```shell
# Install python dependencies
poetry install

# Building the package
poetry build
```
