from importlib.metadata import version as _pkg_version

project = "nnote"
author = "Agil Mammadov"
copyright = "2026, Agil Mammadov"
release = _pkg_version("nnote")

extensions = []
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
