SHELL := /bin/sh
BUILD_DIR := dist
TEMPLATES_DIR := templates
PACKAGED_TEMPLATES_DIR := $(BUILD_DIR)/packaged_templates

.DEFAULT_GOAL := build

init:
	pip install pipenv --user
	pipenv sync

test: init
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
