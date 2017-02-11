# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys

import sphinx_rtd_theme

# Insert project root into the sys-path so that modules can be found by sphinx
sys.path.insert(0, os.path.abspath('../..'))

htmlhelp_basename = project = 'neo-tech-api'

extensions = [
    'sphinx.ext.autodoc',
    'sphinxcontrib.napoleon'
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/3.5', None),
    'setuptools': ('https://pythonhosted.org/setuptools', None)
}

source_suffix = '.rst'
master_doc = 'index'

copyright = '2017, Jaakko Heikela'

pygments_style = 'sphinx'
todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
