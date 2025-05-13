# Use bash (so conda activate works)
SHELL := /usr/bin/env bash

# Declare these names as not real files
.PHONY: help env activate extract clean tokenize train compare test notebook

# Default target: show help
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  env         Recreate the conda environment from environment.yml"
	@echo "  activate    Activate the llm_env in your current shell"
	@echo "  extract     Run the extract step (PDF → raw text)"
	@echo "  clean       Run the clean step (raw text → cleaned text)"
	@echo "  tokenize    Run the tokenize step (cleaned text → tokens/datasets)"
	@echo "  train       Run the training step (fine-tune LLaMA)"
	@echo "  compare     Run the compare step (compare two documents)"
	@echo "  test        Run all unit tests (pytest)"
	@echo "  notebook    Launch JupyterLab in the notebooks/ folder"
	@echo ""

# 1) Rebuild llm_env from your environment.yml
env:
	@echo "Recreating conda environment 'llm_env'..."
	@rm -rf $$(conda info --base)/envs/llm_env
	@conda env create -f environment.yml
	@echo "Environment ready. Run 'make activate' to start using it."

# 2) Activate the llm_env in your current shell
#    Note: you must run this as 'make activate' (POSIX shorthand for 'source')
activate:
	@echo "To activate in this shell, run:"
	@echo ""
	@echo "     conda activate llm_env"
	@echo ""

# 3) Pipeline steps, each calls your single-entry main.py
extract:
	@echo "Running extract step..."
	@python main.py --extract

clean:
	@echo "Running clean step..."
	@python main.py --clean

tokenize:
	@echo "Running tokenize step..."
	@python main.py --tokenize

train:
	@echo "Running train step..."
	@python main.py --train

# compare needs two PDF paths as arguments; example:
#   make compare docs/a.pdf docs/b.pdf
compare:
	@echo "Running compare step with arguments: $(ARGS)"
	@python main.py --compare $(ARGS)

# 4) Run pytest for all tests
test:
	@echo "Running pytest..."
	@pytest -q

# 5) Launch JupyterLab pointing at your notebooks folder
notebook:
	@echo "Launching JupyterLab..."
	@jupyter lab --notebook-dir=notebooks
