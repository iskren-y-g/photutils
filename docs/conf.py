# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
#
# Astropy documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default. Some values are defined in
# the global Astropy configuration which is loaded here before anything else.
# See astropy.sphinx.conf for which values are set there.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))
# IMPORTANT: the above commented section was generated by sphinx-quickstart, but
# is *NOT* appropriate for astropy or Astropy affiliated packages. It is left
# commented out with this explanation to make it clear why this should not be
# done. If the sys.path entry above is added, when the astropy.sphinx.conf
# import occurs, it will import the *source* version of astropy instead of the
# version installed (if invoked as "make html" or directly with sphinx), or the
# version in the build directory (if "python setup.py build_sphinx" is used).
# Thus, any C-extensions that are needed to build the documentation will *not*
# be accessible, and the documentation will not build correctly.

import datetime
import os
import sys

try:
    import astropy_helpers
except ImportError:
    # Building from inside the docs/ directory?
    if os.path.basename(os.getcwd()) == 'docs':
        a_h_path = os.path.abspath(os.path.join('..', 'astropy_helpers'))
        if os.path.isdir(a_h_path):
            sys.path.insert(1, a_h_path)

# Load all of the global Astropy configuration
from astropy_helpers.sphinx.conf import *
from astropy.extern import six

# Get configuration information from setup.cfg
from distutils import config
conf = config.ConfigParser()
conf.read([os.path.join(os.path.dirname(__file__), '..', 'setup.cfg')])
setup_cfg = dict(conf.items('metadata'))

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.1'

# We don't have references to `h5py` ... no need to load the intersphinx mapping file.
del intersphinx_mapping['h5py']

# We currently want to link to the latest development version of the astropy docs,
# so we override the `intersphinx_mapping` entry pointing to the stable docs version
# that is listed in `astropy/sphinx/conf.py`.
intersphinx_mapping['astropy'] = ('http://docs.astropy.org/en/latest/', None)

# Extend astropy intersphinx_mapping with packages we use here
intersphinx_mapping['skimage'] = ('http://scikit-image.org/docs/stable/', None)


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('_templates')

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog += """
.. _Photutils: high-level_API.html
"""

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = setup_cfg['package_name']
author = setup_cfg['author']
copyright = '{0}, {1}'.format(
    datetime.datetime.now().year, setup_cfg['author'])

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

__import__(setup_cfg['package_name'])
package = sys.modules[setup_cfg['package_name']]

# The short X.Y version.
version = package.__version__.split('-', 1)[0]
# The full version, including alpha/beta/rc tags.
release = package.__version__


# -- Options for HTML output ---------------------------------------------------

# A NOTE ON HTML THEMES
# The global astropy configuration uses a custom theme, 'bootstrap-astropy',
# which is installed along with astropy. A different theme can be used or
# the options for this theme can be modified by overriding some of the
# variables set in the global configuration. The variables set in the
# global configuration are listed below, commented out.

html_theme_options = {
    'logotext1': 'phot',   # white, semi-bold
    'logotext2': 'utils',  # orange, light
    'logotext3': ''        # white, light
}

# Add any paths that contain custom themes here, relative to this directory.
# To use a different custom theme, add the directory containing the theme.
#html_theme_path = []

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes. To override the custom theme, set this to the
# name of a builtin theme or the name of a custom theme in html_theme_path.
#html_theme = None

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
from os.path import join
html_favicon = join('_static', 'favicon.ico')

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = ''

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '{0} v{1}'.format(project, release)

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# Static files to copy after template files
html_static_path = ['_static']
html_style = 'photutils.css'


# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + u' Documentation',
                    author, 'manual')]

latex_logo = '_static/photutils_banner.pdf'


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + u' Documentation',
              [author], 1)]

## -- Options for the edit_on_github extension ----------------------------------------

if eval(setup_cfg.get('edit_on_github')):
    extensions += ['astropy.sphinx.ext.edit_on_github']

    versionmod = __import__(setup_cfg['package_name'] + '.version')
    edit_on_github_project = setup_cfg['github_project']
    if versionmod.release:
        edit_on_github_branch = "v" + versionmod.version
    else:
        edit_on_github_branch = "master"

    edit_on_github_source_root = ""
    edit_on_github_doc_root = "docs"

github_issues_url = 'https://github.com/astropy/photutils/issues/'

autodoc_docstring_signature = True

nitpicky = True
nitpick_ignore = []

for line in open('nitpick-exceptions'):
    if line.strip() == "" or line.startswith("#"):
        continue
    dtype, target = line.split(None, 1)
    target = target.strip()
    nitpick_ignore.append((dtype, six.u(target)))


# a simple non-configurable extension that generates Rst files from jupyter
# notebooks
def notebooks_to_rst(app):
    from glob import glob

    try:
        # post "big-split", nbconvert is a separate namespace
        from nbconvert.nbconvertapp import NbConvertApp
        from nbconvert.writers import FilesWriter
        from nbconvert.preprocessors import Preprocessor, ExecutePreprocessor
        from nbconvert.exporters import RSTExporter
        from nbformat import NotebookNode
    except ImportError:
        try:
            from IPython.nbconvert.nbconvertapp import NbConvertApp
            from IPython.nbconvert.writers import FilesWriter
            from IPython.nbconvert.preprocessors import Preprocessor
            from IPython.nbconvert.exporters import RSTExporter
            from IPython.nbformat import NotebookNode
        except ImportError:
            raise ImportError('Failed to find Jupyter or IPython. Cannot build '
                              'the notebooks embedded in the docs. Proceeding '
                              'the rest of the doc build, but additional '
                              'warnings are likely.')
            return

    class OrphanizerWriter(FilesWriter):
        def write(self, output, resources, **kwargs):
            output = ':orphan:\n\n' + output
            FilesWriter.write(self, output, resources, **kwargs)

    class AddSysPath(Preprocessor):
        """
        Adds the local system path to the top of the notebook.  This makes sure
        when build_sphinx is invoked that the notebook actually runs with the
        current build.
        """
        def preprocess(self, nb, resources):
            syspathstr = 'sys.path = {} + sys.path'.format(str(sys.path))
            cell = {'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'outputs': [],
                    'source': 'import sys\n' + syspathstr}
            nb.cells.insert(0, NotebookNode(cell))
            return nb, resources

    class RemoveSysPath(Preprocessor):
        """
        Removes the sys.path cell added by AddSysPath
        """
        def preprocess(self, nb, resources):
            if 'sys.path' in nb.cells[0].source:
                del nb.cells[0]
            return nb, resources

    olddir = os.path.abspath(os.curdir)
    try:
        srcdir = os.path.abspath(os.path.split(__file__)[0])
        os.chdir(os.path.join(srcdir, 'notebooks'))
        nbs = glob('*.ipynb')

        app.info("Executing and converting these notebooks to sphinx files: " + str(nbs))

        nbc_app = NbConvertApp()
        nbc_app.initialize()

        nbc_app.writer = OrphanizerWriter()

        nbc_app.export_format = 'rst'

        pps = RSTExporter().default_preprocessors
        pps.insert(0, AddSysPath)
        pps.append(RemoveSysPath)
        nbc_app.config.RSTExporter.preprocessors = pps

        nbc_app.notebooks = nbs

        nbc_app.start()
    except:
        e = sys.exc_info()[0]
        app.warn('Failed to convert notebooks to RST (see above): ' + str(e))
    finally:
        os.chdir(olddir)

def setup(app):
    app.connect('builder-inited', notebooks_to_rst)
