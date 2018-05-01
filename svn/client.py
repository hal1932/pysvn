# coding: utf-8
from __future__ import print_function, unicode_literals
import xml.etree.ElementTree as et

from command_runner import CommandRunner
from log import Log
from status import Status


class Client(object):

    @property
    def repogitory_root(self): return self.__runner.current_directory

    def __init__(self, runner=CommandRunner()):
        self.__runner = runner

    def set_repogitory_root(self, path):
        self.__runner.current_directory = path

    def get_logs(self, revision=None, limit=None, path=None):
        args = ['--xml']
        if revision is not None:
            args.extend(['--revision', str(revision)])
        if limit is not None:
            args.extend(['--limit', str(limit)])
        if path is not None:
            args.append(path)

        result, stdout, stderr = self.__runner.run('log', args)

        if result != 0:
            raise RuntimeError(stderr)

        return [Log(x) for x in et.fromstring(stdout).findall('logentry')]

    def get_statuses(self, contains_remote_updates=False, paths=None, verbose=False):
        args = ['--xml']
        if contains_remote_updates:
            args.append('--show-updates')
        if paths is not None:
            args.extend(paths)
        if verbose:
            args.append('--verbose')

        result, stdout, stderr = self.__runner.run('status', args)
        if result != 0:
            raise RuntimeError(stderr)

        return [Status(x) for x in et.fromstring(stdout).findall('target/entry')]

    def cleanup(self):
        result, _, stderr = self.__runner.run('cleanup', [])
        if result != 0:
            raise RuntimeError(stderr)
        return True

    def revert(self, paths=['.'], recursive=False):
        args = []
        if paths:
            args.extend(paths)
        if recursive:
            args.append('--recursive')

        result, _, stderr = self.__runner.run('revert', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def update(self, paths=None, revision=None, accept='postpone'):
        args = []
        if paths:
            args.extend(paths)
        if revision:
            args.extend(['--revision', str(revision)])
        if accept:
            args.extend(['--accept', accept])

        result, _, stderr = self.__runner.run('update', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def add(self, paths, force=False):
        args = paths[:]
        if force:
            args.append('--force')

        result, _, stderr = self.__runner.run('add', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def move(self, source, dest):
        args = [source, dest]

        result, _, stderr = self.__runner.run('move', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def delete(self, paths, keep_local=False):
        args = paths[:]
        if keep_local:
            args.append('--keep-local')

        result, _, stderr = self.__runner.run('delete', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def lock(self, paths, force=False):
        args = paths[:]
        if force:
            args.append('--force')

        result, _, stderr = self.__runner.run('lock', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def unlock(self, paths, force=False):
        args = paths[:]
        if force:
            args.append('--force')

        result, _, stderr = self.__runner.run('unlock', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def commit(self, message, paths=None, keep_lock=False):
        args = ['--message', message]
        if keep_lock:
            args.append('--no-unlock')
        if paths:
            args.extend(paths)

        result, _, stderr = self.__runner.run('commit', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True

    def resolve(self, path, accept, recursive=False):
        args = [path, '--accept', accept]
        if recursive:
            args.append('--recursive')

        result, _, stderr = self.__runner.run('resolve', args)
        if result != 0:
            raise RuntimeError(stderr)

        return True
