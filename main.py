#   author: Barre kevin
import os
import json
import sys
import logging.config
from os import path as opath
from os.path import join as opjoin
from sys import path
from functools import partial

try:
    import datatools
except ModuleNotFoundError:
    if os.path.exists('datatools.zip'):
        path.insert(0, 'datatools.zip')
    elif os.path.exists('./src/main/python'):
        path.insert(0, './src/main/python')

from datatools.melatrics import compose, agregate_files_paths, merge_jsons

# FILESYSTEM = "HDFS"
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
