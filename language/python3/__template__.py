#!/usr/bin/env python3
f'''
doc:
  format: yaml
  name: {__name__}:script
  usage:
    bash: &usage env {__name__.upper()}_LOGLEVEL=DEBUG python3 {__name__}
  description: |
  Text in git-flavored markdown
  ```bash
  *usage
  ```
'''

import traceback
import pdb
import sys
import os
import os.path
import fire
import pytest
import logging
import yaml

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
    f'''return the function name of the caller, useful for logging'''
    return sys._getframe(1).f_code.co_name

def help():
    f'''
    Dump the module doc above as a pretty-printed yaml file, currently broken.
    '''
    # TODO mike@carif.io: __name__.__doc__ doesn't get the string above?
    print(yaml.dump(yaml.load(__name__.__doc__)))

def echo(*argv):
    """
    :param argv: tuple or array of argument from poetry or the command line respectively.
    :return: status code 0
    """
    # logger.debug(argv)
    logger.debug(f'in {here()}')
    # logger.debug(f'argv: {sys.argv}')
    argv = argv if argv else sys.argv[1:]
    logger.debug(argv)
    for a in argv: print(a, end=' ')
    print()
    return 0



def say(*argv):
    """
    say.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run say 1 2 3
    say.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner say 1 2 3
    say.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner say 1 2 3

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
    """
    testing.poetry.usage: [RUNNER_LOGLEVEL=debug] poetry run testing [--switch[=value]]*
    testing.python.usage: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner testing [--switch[=value]]*
    testing.python.usage.help: [RUNNER_LOGLEVEL=debug] python -m xonshit.runner testing --help

    :param argv: additional argument to pytest after --roodir, --verbosity and pytest.ini
    :return:
    """
    # logger.debug(f'testing {argv}')
    logger.debug(f'in {here()}')
    logger.debug(argv)
    # run the pytest tests in this file
    return pytest.main(pytest_args)


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
        logger.error(f'message: {e.message}')
        traceback.print_exc()
        pdb.post_mortem()

if __name__ == '__main__':
    main()
