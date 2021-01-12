# Packaging scanprep

## Pip

Prerequisites: `python3 -m pip install --user --upgrade setuptools wheel twine`

1. Make sure the correct versions of the required packages are listed in `setup.py` under `install_requires`.
2. Increment the `version` in `setup.py`.
3. Run `python3 setup.py sdist bdist_wheel` to generate the dist files.
4. Upload to PyPI using `python3 -m twine upload dist/*`. Login using `__token__` as the username and the API token as the password.
5. Create a new release on GitHub.

### References

* <https://stackoverflow.com/a/49684835>
* <https://packaging.python.org/tutorials/packaging-projects/>
* <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html>

## Snap

Updates to the snap are built automatically once pushed to GitHub.
