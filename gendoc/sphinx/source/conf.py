# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyTorch C++ Cheatsheet'
copyright = '2025, Thibault Lejemble'
author = 'Thibault Lejemble'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = '' # empty to not duplicate project name
html_theme = 'alabaster'
html_static_path = ['_static']
html_sidebars = {
    '**': ['localtoc.html'],
}
html_permalinks_icon = '§'