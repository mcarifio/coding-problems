#!/usr/bin/env python3
f'''
doc:
  format: yaml
  name: {__name__}:script
  usage:
    bash: &usage env {__name__.upper()}_LOGLEVEL=DEBUG python3 {__name__}
  description: |
  
  A tree is "superbalanced" if the difference between the depths of any two leaf nodes is no greater than one.
  

'''

import traceback
import pdb
import sys
import os.path
import fire
import pytest
import logging
from typing import List, Set
from contextlib import AbstractContextManager


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
    print(yaml.dump(yaml.load(__name__.__doc__ or '')))



def echo(*argv):
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
    return pytest.main(sys.argv)



## superbalanced

# TODO mike@carif.io: https://docs.python.org/2.5/whatsnew/pep-343.html is an alternative implementation
# TODO mike@carif.io: https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers
#   which only works in async functions? Ugh

class RecursionLimit(AbstractContextManager):
    """
    Modify (usually increase) the recursion limit for functions inside a block.
    Sets the value "interpreter-wide" (?) so may confuse async functions.
    """
    current_recursive_limit = sys.getrecursionlimit()
    def __init__(self, limit):
        sys.setrecursionlimit(limit)
    def __exit__(self, exc_type, exc_value, traceback):
        sys.setrecursionlimit(self.current_recursive_limit)
    def limit(self):
        return sys.getrecursionlimit()

class BinaryTreeNode:

    def __init__(self, value):
        self.value = value
        self.left  = None
        self.right = None

    def insert_left(self, value):
        self.left = BinaryTreeNode(value)
        return self.left

    def insert_right(self, value):
        self.right = BinaryTreeNode(value)
        return self.right

    def is_leaf(self):
        return self.left == None and self.right == None

    # This should suffice, but python3 doesn't do tail recursion elimination (http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html)
    # and the python3 call stack defaults(?) to 1000 calls. More at https://www.geeksforgeeks.org/python-handling-recursion-limit/
    def _frontier_depth(self, depth = 0):
        if self.is_leaf():
            return [(self.value, depth)]
        else:
            if self.left:
                left_frontier = self.left._frontier_depth(depth + 1)
            else:
                left_frontier = []
            if self.right:
                right_frontier = self.right._frontier_depth(depth + 1)
            else:
                right_frontier = []
            return left_frontier + right_frontier

    def frontier_depth(self):
        with RecursionLimit(10**6) as rl:
            return self._frontier_depth()




    def is_superbalanced_loop(self):
        frontier = self.frontier_depth()
        first = frontier[0][1]
        for (_, d) in frontier[1:]:
            if abs(d - first) > 1:
                return False
        return True

    def is_superbalanced(self):
        frontier = self.frontier_depth()
        d0 = frontier[0][1]
        result = all ( abs(d - d0) < 2 for (_, d) in frontier[1:] )  # for debugger
        return result

    def frontier_depth_iterative(self):
        """
        Manage the traversal stack explicitly returning the frontier and depth for each node in the frontier.
        Still think the recursive approach is easier to understand.
        :return:
        """
        frontier = []
        interior = [ self ]
        counter = 0
        while len(interior) > 0:
            node = interior.pop()
            if node.is_leaf():
                frontier.append( (node.value, counter) )
                interior.pop()
                continue
            counter += 1
            if node.left:
                interior.append(node.left)
            if node.right:
                interior.append(node.right)

        return frontier

    def is_superbalanced_iterative(self):
        frontier = self.frontier_depth_iterative()
        d0 = frontier[0][1]
        result = all(abs(d - d0) < 2 for (_, d) in frontier[1:])  # for debugger
        return result


def demo():

    # RecursionLimit
    print(sys.getrecursionlimit())
    with RecursionLimit(10**6) as rl:
        print(rl.limit())
    print(sys.getrecursionlimit())

    # Built up a tree making it superbalanced or not and testing for it.
    root = BinaryTreeNode(0)
    root.insert_left(BinaryTreeNode(1))
    root.insert_right(BinaryTreeNode(2))
    assert root.is_superbalanced() == True
    assert root.is_superbalanced_iterative() == root.is_superbalanced()
    print(root.frontier_depth())
    root.left.insert_left(BinaryTreeNode(3))
    assert root.is_superbalanced() == True
    assert root.is_superbalanced_iterative() == root.is_superbalanced()
    print(root.frontier_depth())
    root.left.left.insert_left(BinaryTreeNode(4))

    # not superbalanced
    assert root.is_superbalanced() == False
    print(root.frontier_depth())

    # superbalanced again
    root.right.insert_left(BinaryTreeNode(5))
    root.right.insert_right(BinaryTreeNode(6))
    assert root.is_superbalanced() == True
    print(root.frontier_depth())


# dispatching and error handling here
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
