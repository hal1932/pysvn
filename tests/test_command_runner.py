# coding: utf-8
from __future__ import print_function, unicode_literals
import unittest as ut
import xml.etree.ElementTree as et

from svn.command_runner import CommandRunner


class TestCommandRunner(ut.TestCase):

    def setUp(self):
        self.__runner = CommandRunner()
        self.__runner.current_directory = 'C:/Users/yuta/Desktop/subversion/trunk'

    def tearDown(self):
        pass

    @ut.skip
    def test_run(self):
        result, out, err = self.__runner.run('info', ['--xml'])
        self.assertEqual(result, 0)
        self.assertEqual(err, '')

        root = et.fromstring(out)
        self.assertEqual(root.tag, 'info')

        entry = root.find('entry')
        self.assertEqual(entry.find('url').text, 'https://svn.apache.org/repos/asf/subversion/trunk')
        self.assertEqual(entry.find('wc-info/wcroot-abspath').text, 'C:/Users/yuta/Desktop/subversion/trunk')


if __name__ == '__main__':
    ut.main()
