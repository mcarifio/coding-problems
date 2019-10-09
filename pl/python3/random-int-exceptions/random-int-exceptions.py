#!/usr/bin/env python3
f"""
---
doc:
  format: yaml
  name: {__name__}:script
  usage:
    bash: &usage env {__name__.upper()}_LOGLEVEL=DEBUG python3 {__name__} demo
  description: |
  Daily Coding Problem: Problem #90 [Medium]
  
  This question was asked by Google.
  
  Given an integer n and a list of integers l, write a function that randomly generates a number from 0 to n-1 that isn't in l (uniform).

  ```bash
  python random-int-exceptions.py demo
  ```
---
"""

import inspect
import traceback
import pdb
import sys
import os
import os.path
import fire
import pytest
import logging
import yaml
from typing import Set
from random import randint

# magic stanza unfortunately
script = os.path.realpath(__file__)
me = os.path.basename(script).split('.')[0].upper()
level = (os.environ.get(me + '_LOGLEVEL') or os.environ.get('LOGLEVEL') or 'INFO').upper()
logging.basicConfig(format='%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level=level)
logger.debug(f'file {__file__}')
logger.debug(f'module {__name__}')


def here():
    f"""return the function name of the caller, useful for logging"""
    (filename, lineno, fname) = inspect.getframeinfo(sys._getframe(1))[0:3]
    return f"{filename}:{lineno}:{fname or ''}"

def help():
    f"""
    Dump the module doc above as a pretty-printed yaml file, currently broken.
    """
    # TODO mike@carif.io: __name__.__doc__ doesn't get the string above?
    print(yaml.dump(yaml.load(__name__.__doc__)))

def echo(*argv):
    f"""
    :param argv: tuple or array of argument from poetry or the command line respectively.
    :return: status code 0
    """    # logger.debug(argv)
    logger.debug(f'in {here()}')
    # logger.debug(f'argv: {sys.argv}')
    argv = argv if argv else sys.argv[1:]
    logger.debug(argv)
    for a in argv: print(a, end=' ')
    print()
    return 0

def say(*argv):
    f"""
    say.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run say 1 2 3
    say.python.usage: [RUNNER_LOGLEVEL=debug] python -m __name__.runner say 1 2 3
    say.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m __name__.runner say 1 2 3

    :param argv: tuple or array of argument from poetry or the command line respectively.
    :return: status code 0
    """
    logger.debug(f'in {here()}')
    argv = argv if argv else sys.argv[1:]
    logger.debug(argv)
    # for a in argv: print(a, end=' ')
    print(' '.join(argv))  # creates a new string, little wasteful
    return 0



def testing(*argv):
    f"""
    testing.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run testing [--switch[=value]]*
    testing.python.usage: [RUNNER_LOGLEVEL=debug] python -m __name__.runner testing [--switch[=value]]*
    testing.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m __name__.runner testing --help

    :param argv: additional argument to pytest after --roodir, --verbosity and pytest.ini
    :return:
    """
    # logger.debug(f'testing {argv}')
    logger.debug(f'in {here()}')
    logger.debug(argv)
    # run the pytest tests in this file
    return pytest.main(argv)



## random-int-exceptions

class RunawayIterationError(Exception):
    f"""
    Signal that an iteration took longer than it should have. Relies on the caller to know what that is.
    """
    def __init__(self, tries):
        super()
        self.tries = tries


def gen_range_with_exceptions(_range:range, _exceptions: Set[int])->int:
    f"""
    Generate an int in [ _range.start, _range.stop ) that isn't in the set of exceptions _exceptions.
    
    All elements in _exceptions are assumed to be ints and also in the range _range. But the implementation still works
    if they are outside the range.
    """
    
    def candidate()->int:
        return randint(_range.start, _range.stop)

    tries = starting_tries = 1000
    next = candidate()
    while (next in _exceptions):
        next = candidate()
        tries -= 1
        if not tries: raise RunawayIterationError(starting_tries)

    return next

def start():
    ten = range(10)  # 0 to 9 inclusive
    exclusions = set([1, 3, 5])
    generated = gen_range_with_exceptions(ten, exclusions)
    assert generated not in exclusions
    assert ten.start <= generated < ten.stop
    logger.info(f'{generated}')



def demo():
    f"""
    Demonstrate the implementation above in some tutorial way. Different from testing, which is more systematic.
    """
    start()


def dispatch(*argv):
    logger.debug(sys.argv)
    logger.debug(f'{here()} {argv}')
    sys.exit(fire.Fire())


# You can call main directly and get a trace and debugging on an unhandled exception.
# See https://news.ycombinator.com/item?id=19075325
def main():
    try:
        dispatch()
    except SystemExit as se:
        logger.debug(f'exit status: {se.code}')
    except Exception as e:
        # print(e)
        logger.error(e)
        # traceback.print_exc()
        # pdb.post_mortem()

if __name__ == '__main__':
    main()
