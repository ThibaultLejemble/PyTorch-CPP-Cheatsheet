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
    '**': ['about.html', 'localtoc.html'],
}
html_permalinks_icon = '§'
html_theme_options = {
    'fixed_sidebar': 'true',
    'show_powered_by': 'false',
    'logo': 'logo.png',
    'anchor_hover_bg': '#FFFFFF',
    'gray_2': '#F8F8F8', # Light gray used for code background (default=EEE)
    'link_hover': '#F73C16',
    'link': '#ee4c2c', # oragen
    'pre_bg': '#F8F8F8',
    'code_font_family': 'Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace;',
    'font_family': 'Helvetica Neue, Helvetica, Arial, sans-serif;',
    'head_font_family': 'Helvetica Neue, Helvetica, Arial, sans-serif;',
    'font_size': '15px', # 17px by default
    'page_width': '1200px', # 940px by default
}

pygments_style = 'vs'