"""
http://peak.telecommunity.com/DevCenter/setuptools
http://pygments.org/docs/plugins/
http://pygments.org/docs/styles/#getting-a-list-of-available-styles
"""
from setuptools import setup, find_packages
setup(
  name = "C0Pygments",
  version = "0.1",
  py_modules = ["c0lexer","unitue"],
  entry_points = {
    'pygments.styles': [
      'unitue = unitue:UniTue',
    ],
    'pygments.lexers': [
      'c0lexer = c0lexer:C0Lexer',
    ],
  }
)


