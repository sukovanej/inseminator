fix:
	poetry run black inseminator tests examples docs
	poetry run isort inseminator tests examples docs

check:
	poetry run black --check inseminator tests examples docs
	poetry run isort --check inseminator tests examples docs
	poetry run mypy inseminator

test:
	poetry run pytest tests


build-sphinx:
	poetry run sphinx-build -b html docs/ docs/build/html