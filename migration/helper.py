# -*- coding: utf-8 -*-
import os

import sys
from bs4 import BeautifulSoup
from importlib import reload


def making_soup(content, doc_type):
    return BeautifulSoup(content, 'lxml' if doc_type is 'html' else 'xml')


def get_fn(path, mode=None):
    """
    :param path: Path of file
    :param mode: See below
    :return: mode: None -> Full file name , mode:0 -> Only file name mode: 1 -> Extension
    """
    if mode is None:
        return os.path.basename(path)
    else:
        if not type(mode) is int:
            raise ValueError
        else:
            return os.path.splitext(os.path.basename(path))[mode]


def get_version(repo_name, title):
    temp = title.upper().replace(repo_name.upper(), '')
    try:
        result = int(temp)
        if result < 0:
            return abs(result)
    except ValueError:
        return temp.replace(' ', '')


def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def set_encoding():
    if sys.version_info[0] == 2:
        reload(sys)
        sys.setdefaultencoding('utf-8')
