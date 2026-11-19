# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from pathlib import Path

import django

# -- Django setup (needed by autodoc to import models and views) -------------

# Root of the project (two levels above this file), so that the Django
# applications can be imported.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
# Throwaway key: only needed to load the settings, the site is not run.
os.environ.setdefault('DJANGO_SECRET_KEY', 'sphinx-build-only')
# Never send anything to Sentry while building the documentation.
os.environ['SENTRY_DSN'] = ''
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OC Lettings'
copyright = '2026, Orange County Lettings'
author = 'Orange County Lettings'
release = '2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Generate the code reference from the docstrings.
    'sphinx.ext.autodoc',
    # Understand the Google style docstrings (Args:, Returns:, Raises:).
    'sphinx.ext.napoleon',
    # Add a "[source]" link to the code of each documented object.
    'sphinx.ext.viewcode',
]

# Keep the order of the source code instead of the alphabetical order.
autodoc_member_order = 'bysource'

exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 3,
}
