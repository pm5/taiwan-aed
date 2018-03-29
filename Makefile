
PYTHON_VERSION=3

.PHONY: all init-project install update freeze start publish

all: init-project install

init-project:
	pipenv --python $(PYTHON_VERSION)

install:
	pipenv install
	make freeze

update:
	pipenv update
	make freeze

freeze:
	pipenv run pip freeze > requirements.txt

start:
	pipenv run bin/get-html      # saves HTML in tmp/
	pipenv run bin/get-data      # extracts JSON in data/

publish:
	pipenv run bin/publish-data  # publish JSON in data/ to remote data branch
