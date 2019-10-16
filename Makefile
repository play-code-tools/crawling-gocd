SHELL := /bin/bash

dependencies:
	pipenv sync	--dev
travis:
	pipenv run python -m unittest discover