#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
#sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))
#print(sys.path)
from src.token import Token, CsvTokenReader
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
import toml
class TestToken(unittest.TestCase):
    @patch('src.token.CsvTokenReader')
    def test_init(self, mock_csv):
        Token()
        mock_csv.assert_called_once()
    # https://docs.python.org/ja/3/library/unittest.mock.html#nesting-patch-decorators
    @patch('src.token.CsvTokenReader.get')
    @patch('os.path.isfile', return_value=True)
    def test_get_from_csv(self, mock_path, mock_csv):
        Token().get('', '')
        mock_csv.assert_called_once()
    @patch('src.token.CsvTokenReader.get')
    @patch('os.path.isfile', return_value=False)
    def test_get_none(self, mock_path, mock_csv):
        Token().get('', '')
        mock_csv.assert_called_once()

if __name__ == "__main__":
    unittest.main()
