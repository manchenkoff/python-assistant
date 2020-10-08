.DEFAULT_GOAL := help
.PHONY: help clean build

help: ## Show this message
	@echo "Application management"
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

sync: ## Install dependencies
	@pipenv sync

clean: ## Clean up distributable files
	@rm -Rf ./build ./dist

build: res clean ## Build application
	@pipenv run pyinstaller main.spec

res: ## Package resources into Python file
	@pipenv run pyside2-rcc ./src/data/resources.qrc -o ./src/voice_assistant/interface/resources.py

run: ## Run application
	@cd src/ && pipenv run python -m main