all: help

help:
	@echo "Uso: make upload -- faz upload do módulo para pypi.globoi.com"

clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name '*.pyc' -exec rm -rf {} \;
	@rm -rf .coverage
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./MANIFEST
	@echo "Done!"

upload: clean
	@python2.6 setup.py -q sdist upload --show-response -r ipypiprod
