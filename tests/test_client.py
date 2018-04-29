# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import unittest as ut
import datetime as dt
import itertools as iter
import xml.etree.ElementTree as et
import subprocess as sp

import pytz

from svn.client import Client


def timestamp(value):
    import time
    return time.mktime(value.timetuple())


def first(seq, predicate=None):
    if predicate is not None:
        return next(iter.ifilter(predicate, seq), None)
    if len(seq) > 0:
        return seq[0]
    return None


def run(cmd):
    sp.Popen(cmd, stdout=sp.PIPE).communicate()


class TestClient(ut.TestCase):

    def setUp(self):
        self.__client = Client()
        self.__client.set_repogitory_root('C:/Users/yuta/Desktop/subversion/branches/1.0.x')

        cwd = os.getcwd()
        os.chdir(self.__client.repogitory_root)

        run('svn cleanup')
        run('svn revert --recursive .')

        p = sp.Popen('svn status --show-updates --xml .', stdout=sp.PIPE)
        current = p.stdout.read()
        p.wait()
        self.__current_rev = int(et.fromstring(current).find('target/against').attrib['revision'])

        run('svn update --revision 851449 CHANGES')
        os.remove('STATUS')
        with open('INSTALL', 'a') as f:
            f.write('hoge')
        open('test', 'w').close()

        os.chdir(cwd)

    def tearDown(self):
        cwd = os.getcwd()
        os.chdir(self.__client.repogitory_root)
        os.remove('test')
        run('svn revert . --recursive')
        os.chdir(cwd)

    @ut.skip
    def test_get_log(self):
        logs = self.__client.get_logs(limit=10)
        self.assertEqual(len(logs), 10)

        jst = pytz.timezone('Asia/Tokyo')

        log = logs[0]
        self.assertEqual(log.revision, 873205)
        self.assertEqual(log.author, 'hwright')
        self.assertEqual(timestamp(log.date.astimezone(jst)), timestamp(dt.datetime(2008, 9, 18, 0, 9, 59, tzinfo=jst)))
        self.assertTrue(log.message.startswith('Merge the 1.0.x-issue-2751 branch:'))

        logs = self.__client.get_logs(path='INSTALL', limit=1)
        self.assertEqual(len(logs), 1)

    @ut.skip
    def test_get_status(self):
        statuses = self.__client.get_statuses()
        self.assertEqual(len(statuses), 3)

        status = first(statuses, lambda x: x.path == 'STATUS')
        self.assertEqual(status.path, 'STATUS')
        self.assertEqual(status.status, 'missing')
        self.assertIsNone(status.remote_status)
        self.assertEqual(status.revision, self.__current_rev)
        self.assertEqual(status.last_commit.revision, 873205)
        self.assertEqual(status.last_commit.author, 'hwright')
        self.assertEqual(timestamp(status.last_commit.date), timestamp(dt.datetime(2008, 9, 17, 15, 9, 59)))
        self.assertEqual(status.last_commit.message, None)

        statuses = self.__client.get_statuses(contains_remote_updates=True)
        self.assertEqual(len(statuses), 4)

        status = first(statuses, lambda x: x.path == 'INSTALL')
        self.assertEqual(status.status, 'modified')
        self.assertEqual(status.remote_status, None)
        self.assertEqual(status.revision, self.__current_rev)
        self.assertEqual(status.last_commit.revision, 849975)
        self.assertEqual(status.last_commit.author, 'sussman')
        self.assertEqual(timestamp(status.last_commit.date), timestamp(dt.datetime(2004, 5, 27, 15, 30, 52)))
        self.assertEqual(status.last_commit.message, None)

        status = first(statuses, lambda x: x.path == 'INSTALL')
        self.assertEqual(status.status, 'modified')
        self.assertIsNone(status.remote_status)

        status = first(statuses, lambda x: x.path == 'test')
        self.assertEqual(status.status, 'unversioned')
        self.assertEqual(status.remote_status, None)

        statuses = self.__client.get_statuses(paths=['CHANGES', 'HACKING'])
        self.assertEqual(len(statuses), 0)

        statuses = self.__client.get_statuses(paths=['CHANGES', 'HACKING'], contains_remote_updates=True)
        self.assertEqual(len(statuses), 1)

    @ut.skip
    def test_revert(self):
        self.__client.revert(paths=['INSTALL'])

        statuses = self.__client.get_statuses(paths=['INSTALL'], contains_remote_updates=True)
        self.assertEqual(len(statuses), 0)

        self.__client.revert(recursive=True)

        statuses = self.__client.get_statuses(contains_remote_updates=True)
        self.assertEqual(len(statuses), 2)
        self.assertIsNotNone(first(statuses, lambda x: x.path == 'CHANGES'))
        self.assertIsNotNone(first(statuses, lambda x: x.path == 'test'))

    @ut.skip
    def test_update(self):
        self.__client.update(paths=['CHANGES'])

        statuses = self.__client.get_statuses(paths=['CHANGES'])
        self.assertEqual(len(statuses), 0)

        self.__client.update()

        statuses = self.__client.get_statuses(contains_remote_updates=True)
        self.assertEqual(len(statuses), 2)
        self.assertIsNotNone(first(statuses, lambda x: x.path == 'INSTALL'))
        self.assertIsNotNone(first(statuses, lambda x: x.path == 'test'))


if __name__ == '__main__':
    ut.main()
