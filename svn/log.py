# coding: utf-8
from __future__ import print_function, unicode_literals
from dateutil.parser import parse


class Log(object):

    def __init__(self, elem):
        self.revision = int(elem.attrib['revision'])
        self.author = elem.find('author').text
        self.date = parse(elem.find('date').text)

        msg = elem.find('msg')
        if msg is not None:
            self.message = msg.text
        else:
            self.message = None
