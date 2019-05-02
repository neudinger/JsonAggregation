# Metrics

`Python 3 library for merge json metrics.`
`Ready to be consumed by kibana and elasticsearch.`

## Getting Started

### Requirement

```sh
pip install pybuilder
```

### Running Example

```sh
python main.py
```

## Setup

```python
# please use conf logger
LOGGER
# example logger.conf
```

### Build

```sh
pyb
pyb clean
```

### Install

```sh
(env) > pip install dist/metrics-{version}/dist/metrics-{version}.{ext}
```

## Usage

- see main.py

```Python
file_directory = opath.dirname(opath.abspath(__file__))
SEARCH_PATHS = [
    opjoin(file_directory, "raw"),
    opjoin(file_directory, "raw", "_archive", "indexes")
]
FILE_NAME = "INDEX"
OUTPUT_PATH = opjoin(file_directory, "raw")
OUTPUT_NAME = "OUTPUT.json"
LOGGER = opjoin(file_directory, "logger.conf")
logging.config.fileConfig(fname=LOGGER, disable_existing_loggers=False)

if __name__ == '__main__':
    do_agregate_files_paths = partial(agregate_files_paths, filename=FILE_NAME + "*")
    make_agregation = compose(merge_jsons, do_agregate_files_paths)
    agregated = make_agregation(SEARCH_PATHS)
    with open(opjoin(OUTPUT_PATH, OUTPUT_NAME),'w') as outfile:
        json.dump(agregated, outfile)
        outfile.close()
    pass
```

## Authors

- **Barre Kevin** - *Initial work*