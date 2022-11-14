install:
		poetry install

gendiff:
		poetry run gendiff

build:
		poetry build

publish:
		poetry publish --dry-run

package-install:
		python3 -m pip install --user dist/*.whl

lint:
		poetry run flake8 gendiff

test:
		poetry run pytest

test-cov:
		poetry run pytest --cov=gendiff --cov=formatter --cov-report xml

gendiff-test:
		poetry run gendiff tests/fixtures/json_test_file_1_1.json tests/fixtures/json_test_file_1_2.json