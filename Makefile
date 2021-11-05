fix:
	poetry run black inseminator tests examples
	poetry run isort inseminator tests examples

check:
	poetry run black --check inseminator tests examples
	poetry run isort --check inseminator tests examples
	poetry run mypy inseminator
