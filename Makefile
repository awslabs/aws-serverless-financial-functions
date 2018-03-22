SHELL := /bin/sh
PY_VERSION := 3.6

export PYTHONUNBUFFERED := 1

BUILD_DIR := dist
TEMPLATES_DIR := templates
PACKAGED_TEMPLATES_DIR := $(BUILD_DIR)/packaged_templates

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))

.DEFAULT_GOAL := build

init:
	$(PYTHON) -m pip install pipenv --user

test: init
	pipenv sync --dev
	pipenv run py.test -v test/unit

build: test

package: init
	mkdir -p $(BUILD_DIR)
	pipenv lock --requirements > $(BUILD_DIR)/requirements.txt
	pipenv run pip install -t code/lib -r $(BUILD_DIR)/requirements.txt
	mkdir -p $(PACKAGED_TEMPLATES_DIR)
	for template in $(TEMPLATES_DIR)/* ; do echo "Packaging $$template..."; aws cloudformation package --template-file $$template --s3-bucket $(PACKAGE_BUCKET) --output-template-file $(PACKAGED_TEMPLATES_DIR)/$$(basename $$template); done

deploy: package
	for template in $(PACKAGED_TEMPLATES_DIR)/* ; do echo "Deploying $$template..."; aws cloudformation deploy --template-file $$template --stack-name FinancialFunctions-$$(basename $$template .yaml) --capabilities CAPABILITY_IAM; done

clean:
	rm -rf $(BUILD_DIR)
