#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.token import CsvTokenReader
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
import toml
class TestCsvTokenReader(unittest.TestCase):
    def setUp(self):
        self.rows = [
            ['test.com', 'test-user', 'read', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'],
        ]

    def test_path(self):
        self.assertEqual(os.path.basename(CsvTokenReader().Path), 'token.tsv')
    @patch('os.path.isfile', return_value=False)
    def test_get_not_exist_file(self, mock_lib):
        self.assertEqual(CsvTokenReader().get('', ''), None)
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_hit_one_of_one(self, mock_lib):
        mock_lib.return_value = self.rows
        actual = CsvTokenReader().get(self.rows[0][0], self.rows[0][1])
        mock_lib.assert_called_once()
        self.assertEqual(actual, self.rows[0][3])
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_hit_one_of_two(self, mock_lib):
        mock_lib.return_value = [
            self.rows[0],
            [self.rows[0][0]+'2', self.rows[0][1]+'2', self.rows[0][2], self.rows[0][3]+'2'],
        ]
        actual = CsvTokenReader().get(mock_lib.return_value[1][0], mock_lib.return_value[1][1])
        mock_lib.assert_called_once()
        self.assertEqual(actual, mock_lib.return_value[1][3])
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_hit_two_of_two(self, mock_lib):
        mock_lib.return_value = [
            self.rows[0],
            [self.rows[0][0], self.rows[0][1], ['write'], 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'],
        ]
        actual = CsvTokenReader().get(mock_lib.return_value[1][0], mock_lib.return_value[1][1])
        mock_lib.assert_called_once()
        self.assertEqual(actual, mock_lib.return_value[0][3])
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_not_hit_one(self, mock_lib):
        mock_lib.return_value = self.rows
        for case in [
            (([self.rows[0][0]+'2', self.rows[0][1]], None), None),
            (([self.rows[0][0], self.rows[0][1]+'2'], None), None),
            (([self.rows[0][0]+'2', self.rows[0][1]], ['write']), None),
        ]:
            with self.subTest(args=case[0][0], kwargs=case[0][1], expected=case[1]):
                actual = CsvTokenReader().get(*case[0][0], scopes=case[0][1])
                self.assertEqual(actual, None)
    @patch('src.token.CsvTokenReader._CsvTokenReader__get_rows')
    def test_get_not_hit_two(self, mock_lib):
        mock_lib.return_value = [
            self.rows[0],
            [self.rows[0][0], self.rows[0][1], ['write'], 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'],
        ]
        for case in [
            (([self.rows[0][0]+'2', self.rows[0][1]], None), None),
            (([self.rows[0][0], self.rows[0][1]+'2'], None), None),
            (([self.rows[0][0]+'2', self.rows[0][1]], ['follow']), None),
        ]:
            with self.subTest(args=case[0][0], kwargs=case[0][1], expected=case[1]):
                actual = CsvTokenReader().get(*case[0][0], scopes=case[0][1])
                self.assertEqual(actual, None)

if __name__ == "__main__":
    unittest.main()
