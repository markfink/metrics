# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import fnmatch
import logging
import tempfile
from shutil import copyfile

import pytest

from metrics.metrics_utils import glob_files, load_metrics_from_file
from metrics import METRICS_FILENAME

from . import here


ROOT_DIR = here('./resources/static_files')
log = logging.getLogger(__name__)


def test_find_two_files():
    result = list(glob_files(ROOT_DIR, ['a/**']))
    #assert list(result) == [
    #    (ROOT_DIR + '/a/aa.txt', 'a/aa.txt'),
    #    (ROOT_DIR + '/a/ab.txt', 'a/ab.txt')
    #]
    assert (ROOT_DIR + '/a/aa.txt', 'a/aa.txt') in result
    assert (ROOT_DIR + '/a/ab.txt', 'a/ab.txt') in result


def test_default_include():
    result = list(glob_files(ROOT_DIR))
    assert (ROOT_DIR + '/a/aa.txt', 'a/aa.txt') in result
    assert (ROOT_DIR + '/a/ab.txt', 'a/ab.txt') in result
    assert (ROOT_DIR + '/b/ba.txt', 'b/ba.txt') in result
    assert (ROOT_DIR + '/b/bb.txt', 'b/bb.txt') in result


def test_later_include_has_precedence():
    # note: this testcase is not exactly relevant any more since the tag
    # mechanism has been removed
    result = list(glob_files(ROOT_DIR, ['**', 'a/**']))
    assert (ROOT_DIR + '/b/ba.txt', 'b/ba.txt') in result
    assert (ROOT_DIR + '/b/bb.txt', 'b/bb.txt') in result
    assert (ROOT_DIR + '/a/aa.txt', 'a/aa.txt') in result
    assert (ROOT_DIR + '/a/ab.txt', 'a/ab.txt') in result


def test_exclude_file():
    result = glob_files(ROOT_DIR, ['a/**'], ['a/aa.txt'])
    assert list(result) == [
        (ROOT_DIR + '/a/ab.txt', 'a/ab.txt')
    ]


def test_exclude_file_with_gitignore():
    result = glob_files(ROOT_DIR, ['a/**'],
                        gitignore=['aa.txt'])
    assert list(result) == [
        (ROOT_DIR + '/a/ab.txt', 'a/ab.txt')
    ]


def test_how_crazy_is_it():
    f = '/a/b/c/d.txt'
    p = '/a/**/d.txt'
    assert fnmatch.fnmatchcase(f, p)


@pytest.fixture
def tempfolder():
    """setup tempfolder with .metrics file and cd into it."""
    curr_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as temp:
        os.chdir(temp)
        yield
        os.chdir(curr_dir)


@pytest.fixture
def metrics_info(tempfolder):
    """copy .metrics file to tempfolder."""
    copyfile(here('resources/' + METRICS_FILENAME),
             METRICS_FILENAME)


def test_load_metrics_from_file(metrics_info):
    data = load_metrics_from_file(METRICS_FILENAME)
    assert 'files' in data
    assert 'build' in data
    assert len(data['files'].items()) > 20


def test_load_metrics_from_file_no_file(tempfolder):
    data = load_metrics_from_file(METRICS_FILENAME)
    assert data == {}
