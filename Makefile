SHELL := /bin/sh

.DEFAULT_GOAL := build

init:
	pip install pipenv --user
	pipenv sync

test: init
	pipenv run py.test -v test/unit

build: test
