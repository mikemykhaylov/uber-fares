.PHONY: clean data features model lint format requirements build

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = data-science-pipeline-f1eb75cd-9d56-4916-a1c9-a1bef6478afa
PROJECT_NAME = uber-fares
PYTHON_INTERPRETER = python3

ifeq (,$(shell which conda))
HAS_CONDA=False
else
	HAS_CONDA=True
	ifeq (,$(shell which mamba))
		HAS_MAMBA=False
	else
		HAS_MAMBA=True
	endif
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Set up python interpreter environment
environment:
ifeq (True,$(HAS_MAMBA))
	@echo ">>> Detected mamba, creating conda environment."
	mamba env create -n $(PROJECT_NAME) -f environment.yml
	@echo ">>> New conda env created. Activate with:\nmamba activate $(PROJECT_NAME)"
else ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
	conda env create -n $(PROJECT_NAME) -f environment.yml
	@echo ">>> New conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Install Python Dependencies
requirements: test_environment
ifeq (True,$(HAS_CONDA))
	@echo ">>> Conda environment already installed, skipping requirements install"
else
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Process dataset
data:
	$(PYTHON_INTERPRETER) -m utils.data pipe

## Format raw data
data-format:
	$(PYTHON_INTERPRETER) -m utils.data format

## Clean formatted data
data-clean:
	$(PYTHON_INTERPRETER) -m utils.data clean

## Enrich clean data
data-enrich:
	$(PYTHON_INTERPRETER) -m utils.data enrich

## Create features
features:
	$(PYTHON_INTERPRETER) -m utils.features build

## Train model
model:
	$(PYTHON_INTERPRETER) -m utils.models train data/processed --output-path=models --mode=train --max_depth=27 --n_estimators=100

## Run custom training job on Google Cloud
vertex_train: gcs_task_push
	CURRTIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
	gcloud ai custom-jobs create --region=us-central1 --display-name="uber-fares-model-${CURRTIME}" --config=gcloud/train_config.yml

## Run hyperparameter tuning job on Google Cloud Vertex AI
vertex_hp_tune: gcs_task_push
	CURRTIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
	gcloud ai hp-tuning-jobs create --region=us-central1 --display-name="uber-fares-model-tuning-${CURRTIME}" \
	--max-trial-count=10 --parallel-trial-count=3 --config=gcloud/hp_config.yml

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Upload data to Google Cloud Storage
gcs_data_push:
	gsutil -m cp -R data/interim gs://$(BUCKET)/data
	gsutil -m cp -R data/processed gs://$(BUCKET)/data

## Download data from Google Cloud Storage
gcs_data_pull:
	gsutil -m cp -R gs://$(BUCKET)/data .

## Download raw data from Google Cloud Storage
gcs_data_pull_raw:
	gsutil -m cp -R gs://$(BUCKET)/data/raw data
	gsutil -m cp -R gs://$(BUCKET)/data/external data

## Download models from Google Cloud Storage
gcs_model_pull:
	gsutil -m cp -R gs://$(BUCKET)/model models

## Upload model task to Google Cloud Storage
gcs_task_push: build
	gsutil -m cp -R dist/uber-fares-0.2.0.tar.gz gs://$(BUCKET)

## Lint using flake8
lint:
	flake8 utils

## Format using yapf
format:
	yapf utils -r -i

## Build source distribution
build:
	flit build --format sdist

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
