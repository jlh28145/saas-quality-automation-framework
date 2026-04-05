PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m playwright install

test:
	pytest

test-smoke:
	pytest -m smoke

test-ui:
	pytest tests/ui -m ui

test-api:
	pytest tests/api -m api

test-system:
	pytest tests/system -m system

lint:
	ruff check .
	black --check .

format:
	black .