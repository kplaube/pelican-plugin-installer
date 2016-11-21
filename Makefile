help:
	@echo ''
	@echo 'Pelican Plugin Installer'
	@echo ''
	@echo 'help ........................ This screen'
	@echo 'lint ........................ Execute code quality tests'
	@echo 'release ..................... Send the package to Pypi'
	@echo 'setup ....................... Setup the project for development'
	@echo 'test ........................ Run py.test tests'
	@echo 'tox ......................... Run tox tests'
	@echo ''

lint:
	flake8 pelican_plugin_installer/

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*

setup:
	python setup.py develop

test:
	python setup.py test

tox:
	tox
