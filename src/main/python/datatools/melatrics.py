import os
import json
from sys import path
import itertools
from functools import reduce, partial
from collections import defaultdict, OrderedDict, Callable
import glob
import logging

logger = logging.getLogger(__name__)
FILESYSTEM = "LFS"

class DefaultOrderedDict(OrderedDict):
    """
    DefaultOrderedDict class
    """
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None
                and not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))


def findfiles(pathname: str = "", filename: str = "") -> list:
    """ Return a list of paths matching a pathname pattern.
    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.
    """
    if FILESYSTEM == "LFS":
        return (glob.glob(os.path.join(pathname, filename)))


def agregate_files_paths(paths: list, filename: str = "") -> list:
    """
    Recieve path list and filename.
    Search all file in paths.
    Add * at the end or begin
    However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    Args:
        
        paths (list):   list of path.
        filename (str):   name of document.

    Returns:
        Return an iterable with all path agregated in one.

    Examples:
        paths = [
            "/metrics/raw/",
            "/raw/_archive/indexes/"
        ]
        filename = "foo.bar"
        >>> agregate_files_paths(paths, filename + "*")
        /metrics/raw/foo.bar.1.json
        /metrics/raw/INDEX2.json
        /raw/_archive/indexes/foo.bar-20190318T165256
        /raw/_archive/indexes/foo.bar-20190308T080456
        /raw/_archive/indexes/foo.bar-20190402T180115
        /raw/_archive/indexes/foo.bar-20190402T213232
        /raw/_archive/indexes/foo.bar-20190330T080431
        /raw/_archive/indexes/foo.bar-20190219T080155
        /raw/_archive/indexes/foo.bar-20190224T080132
    """
    return itertools.chain(*(findfiles(path, filename)
                             for path in paths))


def read_json(file: str = "") -> dict:
    """
    Recieve path of json file.
    return 

    Args:
        file (str):   file.

    Returns:
        Return an '{}' if json file is not reachable, non readable.

    Examples:
        path = "/place/of/document.json"
        >>> read_json(path)
        {}
    
    Raises:
        except json.JSONDecodeError :
            do not raise an exception
            log in error
    """
    exist = os.path.isfile(file)
    logging.debug("file is = %r" % (file))
    idx = {}
    if exist:
        with open(file) as idx_file:
            try:
                idx = json.load(idx_file)
                logging.debug("%r opened" % (file))
            except json.JSONDecodeError as JSONErrorMsg:
                logging.error("Impossible to read document %r" % (file))
                logging.error("%r" % (JSONErrorMsg))
            finally:
                idx_file.close()
                logging.debug("%r closed" % (file))
    else:
        logging.error("file %r doesn't exist" % (file))
    return idx


def agregate(values: dict,
             agregated: DefaultOrderedDict = DefaultOrderedDict(list)
             ) -> DefaultOrderedDict(list):
    """
    Recieve path of json file.
    return 

    Args:
        
        values (list):   old occurrences.
        agregated (DefaultOrderedDict):   DefaultOrderedDict(list) by default.

    Returns:
        Return an '{}' if json file is not reachable, non readable.

    Examples:
        >>> first = agregate({
                "keyone": 1,
                "keytwo": 2,
                "key3": {
                    "bad": "bitch"
                },
                "jerome": "est"
            })

        key = 'keyone', value = [1]
        key = 'keytwo', value = [2]
        key = 'key3', value = [{'bad': 'bitch'}]
        key = 'jerome', value = ['est']

        >>> for key, value in first.items():
                print("key = %r, value = %r" % (key, value))
        >>> second = agregate(
                {
                    "keyone": 21,
                    "keytwo": 2,
                    "key3": {
                        "bad": "bitch"
                    },
                    "jerome": "pd"
                }, first)
        >>> for key, value in first.items():
                print("key = %r, value = %r" % (key, value))
        key = 'keyone', value = [1, 21]
        key = 'keytwo', value = [2]
        key = 'key3', value = [{'bad': 'bitch'}]
        key = 'jerome', value = ['est', 'pd']
    """
    for k, v in values.items():
        if v not in agregated[k]:
            agregated[k].append(v)
    return agregated


def merge_jsons(files_paths: list = []) -> dict:
    """
    Recieve path of json file.
    return dict

    Args:
        files_paths (list):  json locations. 

    Returns:
        Return a dict with all json file merged.

    """
    return reduce(
        lambda prev, nex: OrderedDict(itertools.chain(prev.items(), nex.items())),
        map(lambda file: agregate(read_json(file)), files_paths))


def compose(*F):
    return reduce(lambda f, g: lambda x: f(g(x)), F)
