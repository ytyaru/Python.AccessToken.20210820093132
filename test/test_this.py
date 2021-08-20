#!/usr/bin/env python3
# coding: utf8
import os, sys, pathlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.token import This
import unittest
from unittest.mock import MagicMock, patch, mock_open
import copy
class TestThis(unittest.TestCase):
    def test_names(self):
        self.assertTrue(hasattr(This.Names, 'parent'))
        self.assertTrue(hasattr(This.Names, 'name'))
        self.assertTrue(hasattr(This.Names, 'ext'))
        self.assertEqual(This.Names.parent, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))
        self.assertEqual(This.Names.name, 'token')
        self.assertEqual(This.Names.ext, '.py')

if __name__ == "__main__":
    unittest.main()
