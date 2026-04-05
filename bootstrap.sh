#!/usr/bin/env bash

set -euo pipefail

echo "Bootstrapping project structure in current repo..."

# -----------------------------
# Directory Structure
# -----------------------------

mkdir -p app

mkdir -p src/pages
mkdir -p src/api/clients
mkdir -p src/api/schemas
mkdir -p src/api/assertions
mkdir -p src/models
mkdir -p src/utils
mkdir -p src/services

mkdir -p tests/ui
mkdir -p tests/api
mkdir -p tests/system

mkdir -p config
mkdir -p data
mkdir -p reports
mkdir -p scripts
mkdir -p .github/workflows

# -----------------------------
# Python Package Init Files
# -----------------------------

touch src/__init__.py
touch src/pages/__init__.py
touch src/api/__init__.py
touch src/api/clients/__init__.py
touch src/api/schemas/__init__.py
touch src/api/assertions/__init__.py
touch src/models/__init__.py
touch src/utils/__init__.py
touch src/services/__init__.py

touch tests/__init__.py
touch tests/ui/__init__.py
touch tests/api/__init__.py
touch tests/system/__init__.py

touch app/__init__.py

# -----------------------------
# App Placeholders
# -----------------------------

touch app/main.py

# -----------------------------
# Source Layer Placeholders
# -----------------------------

touch src/pages/base_page.py
touch src/pages/login_page.py
touch src/pages/dashboard_page.py
touch src/pages/form_page.py

touch src/api/clients/base_client.py
touch src/api/clients/auth_client.py
touch src/api/clients/users_client.py
touch src/api/clients/forms_client.py
touch src/api/clients/exports_client.py

touch src/api/schemas/auth_schema.py
touch src/api/schemas/user_schema.py
touch src/api/schemas/form_schema.py
touch src/api/schemas/export_schema.py

touch src/api/assertions/response_assertions.py
touch src/api/assertions/schema_assertions.py

touch src/models/test_data_models.py

touch src/utils/config.py
touch src/utils/logger.py
touch src/utils/data_loader.py
touch src/utils/retry.py
touch src/utils/path_helpers.py

touch src/services/auth_service.py
touch src/services/export_service.py
touch src/services/log_service.py

# -----------------------------
# Test Layer Placeholders
# -----------------------------

touch tests/conftest.py

touch tests/ui/test_login.py
touch tests/ui/test_navigation.py
touch tests/ui/test_form_submission.py

touch tests/api/test_auth_api.py
touch tests/api/test_users_api.py
touch tests/api/test_exports_api.py

touch tests/system/test_export_file_creation.py
touch tests/system/test_audit_log_entries.py
touch tests/system/test_background_job_outputs.py

# -----------------------------
# Config / Data
# -----------------------------

touch config/settings.yaml
touch config/dev.yaml
touch config/ci.yaml

touch data/users.json
touch data/forms.json
touch data/expected_exports.json

# -----------------------------
# Root Files (only create if missing)
# -----------------------------

create_if_missing() {
  FILE=$1
  CONTENT=$2

  if [ ! -f "$FILE" ]; then
    echo "Creating $FILE"
    printf "%s\n" "$CONTENT" > "$FILE"
  else
    echo "$FILE already exists, skipping"
  fi
}

create_if_missing ".gitignore" "# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/

# Pytest
.pytest_cache/
reports/
htmlcov/

# Playwright
playwright-report/
test-results/

# IDE
.vscode/
.idea/

# Env
.env
"

create_if_missing "requirements.txt" "playwright
pytest
pytest-html
pytest-xdist
requests
PyYAML
jsonschema
black
ruff
pre-commit
"

create_if_missing "pytest.ini" "[pytest]
addopts = -ra
testpaths = tests
pythonpath = .
markers =
    smoke: critical path tests
    regression: broader validation suite
    ui: UI automation tests
    api: API automation tests
    system: system-level validation tests
"

create_if_missing "Makefile" "PYTHON ?= python3

install:
\t\$(PYTHON) -m pip install -r requirements.txt
\t\$(PYTHON) -m playwright install

test:
\tpytest

test-smoke:
\tpytest -m smoke

test-ui:
\tpytest tests/ui -m ui

test-api:
\tpytest tests/api -m api

test-system:
\tpytest tests/system -m system

lint:
\truff check .
\tblack --check .

format:
\tblack .
"

create_if_missing ".env.example" "TEST_ENV=dev
BASE_URL=http://localhost:8000
API_BASE_URL=http://localhost:8000/api
LOG_LEVEL=INFO
"

create_if_missing "README.md" "# saas-quality-automation-framework

Production-style Python automation framework demonstrating UI, API, and system-level validation for a SaaS-style application.

## Status
Bootstrapped project structure complete.
"

create_if_missing "Dockerfile" "FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [\"pytest\"]
"

create_if_missing ".github/workflows/ci.yml" "name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: \"3.11\"

      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - run: |
          python -m playwright install --with-deps

      - run: pytest
"

# -----------------------------
# Done
# -----------------------------

echo ""
echo "Bootstrap complete."
echo ""
echo "Next steps:"
echo "  python3 -m venv .venv"
echo "  source .venv/bin/activate"
echo "  make install"
echo ""
echo "Then start Phase 1 implementation."