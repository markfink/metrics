""" Miscellaneous path processing tools. """

# Standard
import os


def get_test_file_contents(path_tuple):
    """"""
    script_path = os.path.dirname(os.path.realpath(__file__))
    test_file_path = os.path.join(script_path, *path_tuple)

    with open(test_file_path) as a_file:
        return a_file.read()
