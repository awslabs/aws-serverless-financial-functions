SHELL := /bin/sh
PY_VERSION := 3.6

export PYTHONUNBUFFERED := 1

BUILD_DIR := dist
TEMPLATES_BUILD_DIR := $(BUILD_DIR)/templates
PACKAGED_TEMPLATES_DIR := $(BUILD_DIR)/packaged_templates

# user needs to set PACKAGE_BUCKET as env variable
PACKAGE_BUCKET ?= <bucket>
AWS_DEFAULT_REGION ?= us-east-1

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))

.DEFAULT_GOAL := build

init:
	$(PYTHON) -m pip install pipenv --user

test: init
	pipenv sync --dev
	pipenv run py.test -v test/unit

build: test

pre-package: init
	mkdir -p $(BUILD_DIR) $(TEMPLATES_BUILD_DIR)
	cp -r financial_functions $(BUILD_DIR)
	cp templates/*.yaml $(TEMPLATES_BUILD_DIR)
	
	pipenv lock --requirements > $(BUILD_DIR)/requirements.txt
	pipenv run pip install -t $(BUILD_DIR)/financial_functions/lib -r $(BUILD_DIR)/requirements.txt
	
package: pre-package
	mkdir -p $(PACKAGED_TEMPLATES_DIR)
	aws cloudformation package --template-file $(SOURCE_TEMPLATE) --s3-bucket $(PACKAGE_BUCKET) --output-template-file $(PACKAGED_TEMPLATES_DIR)/$$(basename $(SOURCE_TEMPLATE))
	
deploy:
	aws cloudformation deploy --template-file $(PACKAGED_TEMPLATE) --stack-name $$(basename $(PACKAGED_TEMPLATE) .yaml) --capabilities CAPABILITY_IAM

set-fv-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/fv.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/fv.yaml)
package-fv: set-fv-template package
deploy-fv: set-fv-template package-fv deploy
	
set-fvschedule-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/fvschedule.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/fvschedule.yaml)
package-fvschedule: set-fvschedule-template package
deploy-fvschedule: set-fvschedule-template package-fvschedule deploy
	
set-irr-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/irr.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/irr.yaml)
package-irr: set-irr-template package
deploy-irr: set-irr-template package-irr deploy
	
set-mirr-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/mirr.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/mirr.yaml)
package-mirr: set-mirr-template package
deploy-mirr: set-mirr-template package-mirr deploy
	
set-xirr-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/xirr.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/xirr.yaml)
package-xirr: set-xirr-template package
deploy-xirr: set-xirr-template package-xirr deploy
	
set-nper-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/nper.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/nper.yaml)
package-nper: set-nper-template package
deploy-nper: set-nper-template package-nper deploy
	
set-npv-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/npv.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/npv.yaml)
package-npv: set-npv-template package
deploy-npv: set-npv-template package-npv deploy
	
set-xnpv-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/xnpv.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/xnpv.yaml)
package-xnpv: set-xnpv-template package
deploy-xnpv: set-xnpv-template package-xnpv deploy
	
set-pmt-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/pmt.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/pmt.yaml)
package-pmt: set-pmt-template package
deploy-pmt: set-pmt-template package-pmt deploy
	
set-ppmt-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/ppmt.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/ppmt.yaml)
package-ppmt: set-ppmt-template package
deploy-ppmt: set-ppmt-template package-ppmt deploy
	
set-pv-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/pv.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/pv.yaml)
package-pv: set-pv-template package
deploy-pv: set-pv-template package-pv deploy
	
set-rate-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/rate.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/rate.yaml)
package-rate: set-rate-template package
deploy-rate: set-rate-template package-rate deploy
	
set-effect-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/effect.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/effect.yaml)
package-effect: set-effect-template package
deploy-effect: set-effect-template package-effect deploy
	
set-nominal-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/nominal.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/nominal.yaml)
package-nominal: set-nominal-template package
deploy-nominal: set-nominal-template package-nominal deploy
	
set-sln-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/sln.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/sln.yaml)
package-sln: set-sln-template package
deploy-sln: set-sln-template package-sln deploy

set-wrapper-template:
	$(eval SOURCE_TEMPLATE := $(TEMPLATES_BUILD_DIR)/wrapper.yaml)
	$(eval PACKAGED_TEMPLATE := $(PACKAGED_TEMPLATES_DIR)/wrapper.yaml)
package-wrapper: set-wrapper-template package
deploy-wrapper: set-wrapper-template package-wrapper deploy

clean:
	rm -rf $(BUILD_DIR)
