
run:
	python -m ninam --help
	
build:
	rm -Rf dist/ ; python -m build

test:
	python -m pytest

publish:
	python -m twine upload  dist/*
