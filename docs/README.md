
# Readthedocs Sphinx Files

These are the files for Readthedocs to use for generating documentation pages based on Sphinx. This was setup by
running the commands:

```bash
sphinx-quickstart
sphinx-apidoc -o . ../randomdataset
``` 

The generated `conf.py` file was modified to add the current and parent directories to `sys.path`, add `'sphinx.ext.autodoc'`
to the list of used extensions, and changing the html theme.

Readthedocs additionally depends on the `.readthedocs.yaml` file in the project root. 
