"""
This test script tests the output of different formats available to
Metrics.
"""

# Standard
import collections
# Project
from metrics import output_formats

TEST_LANGUAGE_DICTIONARY = {
    'headers': ["Language", "SLOC", "Comments", "McCabe"],
    'results': [["C", 5, 3, 1], ["Python", 7, 23, 2]],
    'totals': ['', 12, 36, 3],
}

TEST_FILE_DICTIONARY = {
    'headers': ["Filename", "Language", "SLOC", "Comments", "McCabe"],
    'results': [["test_file_1.c", "C", 5, 3, 1],
              ["test_file_2.py", "Python", 7, 23, 2]],
    'totals': ['', '', 12, 36, 3],
}


def test_csv():
    """ Test CSV output. """
    expected = """Filename,Language,SLOC,Comments,McCabe
test_file_1.c,C,5,3,1
test_file_2.py,Python,7,23,2"""
    results = output_formats.format_csv(TEST_FILE_DICTIONARY)

    assert results == expected


def test_json_file():
    """ Test JSON output. """
    expected = """{
  "test_file_1.c": {
    "Language": "C",
    "SLOC": 5,
    "Comments": 3,
    "McCabe": 1
  },
  "test_file_2.py": {
    "Language": "Python",
    "SLOC": 7,
    "Comments": 23,
    "McCabe": 2
  }
}"""
    results = output_formats.format_json(TEST_FILE_DICTIONARY)
    print(results)
    assert results == expected


def test_json_language():
    """ Test JSON output of language results. """
    expected = """{
  "C": {
    "SLOC": 5,
    "Comments": 3,
    "McCabe": 1
  },
  "Python": {
    "SLOC": 7,
    "Comments": 23,
    "McCabe": 2
  }
}"""
    results = output_formats.format_json(TEST_LANGUAGE_DICTIONARY)
    print(results)
    assert results == expected


def test_xml_file():
    """ Test XML output of file results. """
    expected ="""<files>
  <file language="C" name="test_file_1.c">
    <metric name="SLOC" value="5" />
    <metric name="Comments" value="3" />
    <metric name="McCabe" value="1" />
  </file>
  <file language="Python" name="test_file_2.py">
    <metric name="SLOC" value="7" />
    <metric name="Comments" value="23" />
    <metric name="McCabe" value="2" />
  </file>
</files>
"""
    config = {
        'item_offset': 2,
        'item_name': "file",
        'item_attrs': {
            'name': 0,
            'language': 1,
        },
        'root_name': "files",
    }

    assert output_formats.format_xml(config, TEST_FILE_DICTIONARY).decode() == expected


def test_table_file():
    """ Test printing a table sorted by language. """
    expected = """Filename        Language  SLOC  Comments  McCabe
--------------- --------- ----- --------- -------
test_file_1.c   C         5     3         1     
test_file_2.py  Python    7     23        2     
--------------- --------- ----- --------- -------
                          12    36        3     """
    print(expected)
    result = output_formats.format_table(TEST_FILE_DICTIONARY)
    print(result)
    assert result == expected


def test_table_language():
    """ Test printing a table sorted by language. """
    expected = """Language  SLOC  Comments  McCabe
--------- ----- --------- -------
C         5     3         1     
Python    7     23        2     
--------- ----- --------- -------
          12    36        3     """
    print(expected)
    result = output_formats.format_table(TEST_LANGUAGE_DICTIONARY)
    print(result)
    assert result == expected
