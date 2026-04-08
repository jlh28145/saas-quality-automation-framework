PYTHON ?= python3

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m playwright install chromium firefox

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

test-data-variation:
	pytest -m data_variation

test-performance:
	RUN_PERFORMANCE=true pytest tests/api/test_performance_baseline.py -m performance

test-allure:
	pytest --alluredir=reports/allure-results

docker-build:
	docker build -t saas-quality-automation-framework .

docker-test:
	docker run --rm -e ENV=ci saas-quality-automation-framework

lint:
	ruff check .
	black --check .

format:
	black .
