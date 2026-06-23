# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'hofa'
copyright = '2026, CSIC, CNRS, Rényi AI Ltd.'
author = 'Pablo Candela, Diego Gonzalez-Sanchez, and Balazs Szegedy'
release = '0.1.0'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Extensions
#####################################
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "autoapi.extension",
    "myst_nb",
    "sphinx_design",
]

# Enable useful MyST extensions
myst_enable_extensions = [
    "amsmath",
    "dollarmath",
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
]

# Optional: Do not execute notebooks automatically
nb_execution_mode = "off"
###########################################

templates_path = ['_templates']
exclude_patterns = ['**.ipynb_checkpoints', "**/_output/*"]

from sphinx.highlighting import lexers
from pygments.lexers import PythonLexer

lexers['ipython3'] = PythonLexer()

# The next line is to not have a warning about cached objects
suppress_warnings = ["config.cache", "myst.xref_missing"]

autoapi_dirs = ['../../src']
autoapi_keep_files = True

autoapi_ignore = [
    "*/.ipynb_checkpoints/*",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme' 

html_static_path = ['_static']

html_css_files = [
    'footer.css',
    'custom.css',
]

html_theme_options = {
  "secondary_sidebar_items": {
    "**": ["localtoc.html",  "relations", "searchbox","sourcelink",], # "page-toc",
  },
  "footer_start": ["copyright","footer_license", "sphinx-version"],
  "footer_center": ["footer_funders"],
  "navigation_depth": 4,
  "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            # URL where the link will redirect
            "url": "https://github.com/CandelaCSIC/hofa",  # required
            # Icon class (if "type": "fontawesome"), or path to local image (if
            # "type": "local")
            "icon": "fa-brands fa-square-github",
            # The type of image to be used
            "type": "fontawesome",
        }
  ],
  "navbar_align": "left",
}

html_logo = "_static/logo_hof.png"

mathjax_path = "mathjax/tex-mml-chtml.js"


autosummary_generate = True

autosectionlabel_prefix_document = True

html_show_sourcelink = True

html_sourcelink_suffix = '.rst'

source_suffix = ".rst"

html_context = {
    'source_url_prefix': '',  # Leave empty if source files are in the same directory as conf.py
}
