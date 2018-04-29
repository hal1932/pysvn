# coding: utf-8
from __future__ import print_function, unicode_literals
from log import Log


class Status(object):

    def __init__(self, elem):
        self.path = elem.attrib['path']

        wc_status = elem.find('wc-status')
        self.status = wc_status.attrib['item']

        if 'revision' in wc_status.attrib:
            self.revision = int(wc_status.attrib['revision'])
        else:
            self.revision = None

        commit = wc_status.find('commit')
        if commit is not None:
            self.last_commit = Log(commit)
        else:
            self.last_commit = None

        rp_status = elem.find('repos-status')
        if rp_status is not None:
            self.remote_status = rp_status.attrib['item']
        else:
            self.remote_status = None
