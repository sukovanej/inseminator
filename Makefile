lint:
	isort src/**/*.py tests/**/*.py setup.py
	black setup.py src tests
