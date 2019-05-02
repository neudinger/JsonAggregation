import unittest
from mockito import mock, verify


def helloworld(out):
    out.write("Hello world of Python\n")


class HelloWorldTest(unittest.TestCase):
    def test_should_issue_hello_world_message(self):
        out = mock()
        helloworld(out)
        verify(out).write("Hello world of Python\n")


# unittest

# unitest
# from tools.convertools import str_replace
# class StringTest(unittest.TestCase):
#     string_test = "|H|e|l|l|o  Wo|rl|||d||"

#     def test_basic(self):
#         results = str_replace(self.string_test, '|', '')
#         expected_results = self.string_test.replace('|', '')
#         self.assertEqual(string_test, expected_results)
from os import path as opath
from os.path import join as opjoin
from datatools.melatrics import findfiles, agregate_files_paths, read_json


class FilePathTest(unittest.TestCase):

    file_directory = opath.dirname(opath.abspath(__file__))
    file_directories = [
        file_directory,
        opjoin(file_directory, "__pycache__"),
    ]

    def test_findfiles(self):
        results = findfiles(pathname=self.file_directory, filename="*tests*")
        expected_results = [
            opjoin(self.file_directory, "melatrics_tests.py")
        ]
        self.assertEqual(results, expected_results)

    def test_agregate_files_paths(self):
        results = agregate_files_paths(paths=self.file_directories,
                                       filename="*tests*")
        expected_results = [
            opjoin(self.file_directory, "melatrics_tests.py"),
            opjoin(self.file_directory, "__pycache__", "melatrics_tests.cpython-36.pyc")
        ]
        self.assertEqual(list(results), expected_results)
