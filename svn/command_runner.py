# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import subprocess
import logging

from errors import *


class CommandRunner(object):

    @property
    def executer_path(self): return self.__executer_path

    def __init__(self, executer_path='svn'):
        if sys.platform == 'win32' and not executer_path.endswith('.exe'):
            executer_path += '.exe'

        if not os.path.isfile(executer_path):
            for path in os.environ['PATH'].split(os.pathsep):
                abs_path = os.path.join(path, executer_path)
                if os.path.isfile(abs_path):
                    executer_path = abs_path
                    break

        if not os.path.isfile(executer_path):
            raise FileNotFoundError(executer_path)

        self.__executer_path = executer_path

        self.current_directory = os.getcwd()
        self.environments = os.environ.copy()
        self.logger = logging.getLogger(__name__)

        self.logger.info('svn executable path: {}'.format(self.executer_path))

    def run(self, sub_command, args):
        cmd = [self.executer_path, sub_command]
        cmd.extend(args)
        cmd_str = ' '.join(cmd)

        self.logger.info('svn command: {}'.format(cmd_str))

        p = subprocess.Popen(
            cmd_str,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.current_directory,
            env=self.environments
        )

        stdout, stderr = p.communicate()
        result = p.returncode

        return result, stdout, stderr

