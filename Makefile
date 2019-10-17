SHELL := /bin/bash

dependencies:
	pipenv sync	--dev
travis:
	pipenv run python -m unittest discover
publish:
	rm -rf dist
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*