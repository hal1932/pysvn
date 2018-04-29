# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import glob
import importlib
import unittest as ut


def main():
    suite = ut.TestSuite()

    for file_path in glob.glob(os.path.join(os.path.dirname(__file__), 'tests', 'test_*.py')):
        module_name, _ = os.path.splitext(os.path.basename(file_path))
        module = importlib.import_module('tests.{}'.format(module_name))
        for _, value in module.__dict__.items():
            if isinstance(value, type) and issubclass(value, ut.TestCase):
                suite.addTest(ut.makeSuite(value))

    runner = ut.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
