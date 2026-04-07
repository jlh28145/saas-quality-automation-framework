# saas-quality-automation-framework TODO

## Project Goal
Build a production-style Python automation framework for a realistic SaaS-style application that demonstrates strong SDET / QA engineering skills through:

- scalable test architecture
- maintainable automation design
- deterministic test execution
- layered validation across UI, API, and system behavior
- CI/CD integration
- interview-ready clarity

---

## Guiding Principles

- Keep the project generic and non-company-specific
- Favor clarity and maintainability over clever abstractions
- Build something explainable in an interview
- Prioritize deterministic test design
- Treat test automation as an engineering system, not a script collection

---

# Phase 0: Repository Setup and Scaffolding

## Repo Initialization
- [x] Create repository `saas-quality-automation-framework`
- [x] Initialize git
- [x] Add `.gitignore`
- [x] Add `README.md`
- [x] Add `requirements.txt`
- [x] Add `pytest.ini`
- [x] Add `Makefile`
- [x] Add `todo.md`
- [x] Add bootstrap script
- [x] Create package-style folder structure

## Base Folder Structure
- [x] Create `app/`
- [x] Create `src/`
- [x] Create `src/pages/`
- [x] Create `src/api/`
- [x] Create `src/api/clients/`
- [x] Create `src/api/schemas/`
- [x] Create `src/api/assertions/`
- [x] Create `src/models/`
- [x] Create `src/utils/`
- [x] Create `src/services/`
- [x] Create `tests/`
- [x] Create `tests/ui/`
- [x] Create `tests/api/`
- [x] Create `tests/system/`
- [x] Create `config/`
- [x] Create `data/`
- [x] Create `reports/`
- [x] Create `.github/workflows/`

## Python Package Setup
- [x] Add `__init__.py` files where needed
- [x] Make imports clean and predictable
- [x] Confirm package structure works with pytest discovery

---

# Phase 1: Tooling and Dependencies

## Python Dependencies
- [x] Add Playwright
- [x] Add Pytest
- [x] Add Requests
- [x] Add PyYAML
- [x] Add pytest-html
- [x] Add pytest-xdist
- [x] Add jsonschema or pydantic for schema validation
- [x] Add black
- [x] Add ruff
- [x] Add pre-commit
- [x] Add optional mypy

## Browser Tooling
- [x] Install Playwright browsers
- [x] Confirm headless local execution works
- [x] Confirm tests can run in CI-friendly mode

## Quality Tooling
- [x] Set up formatting rules
- [x] Set up linting rules
- [x] Add pre-commit config
- [x] Add base make commands

---

# Phase 2: App Under Test

## App Strategy
- [x] Decide whether app will be Flask or FastAPI based
- [x] Keep app intentionally small and deterministic
- [x] Ensure app supports both UI and API testing
- [x] Ensure app produces at least one system artifact

## Core App Features
- [x] Add login page
- [x] Add invalid login handling
- [x] Add dashboard page
- [x] Add profile or account page
- [x] Add form submission flow
- [x] Add validation errors for bad input
- [x] Add successful submission confirmation
- [x] Add export/report generation feature
- [x] Add audit log writing
- [x] Add API endpoints for key flows

## Deterministic App Data
- [x] Define static seed users
- [x] Define invalid credential set
- [x] Define form payloads
- [x] Define export sample data
- [x] Ensure test environment resets reliably

---

# Phase 3: Framework Core

## Config Management
- [x] Create `config/settings.yaml`
- [x] Create `config/dev.yaml`
- [x] Create `config/ci.yaml`
- [x] Implement config loader utility
- [x] Support environment switching with env vars
- [x] Validate missing or invalid config early

## Logging
- [x] Create logger utility
- [x] Add console logging
- [x] Add file logging
- [x] Use structured log formatting where reasonable
- [x] Ensure logs are useful for debugging failures

## Data Handling
- [x] Create test data loader
- [x] Store deterministic test inputs in `data/`
- [x] Separate UI data from API payload data
- [x] Add expected output data for assertions

## Shared Utilities
- [x] Add file/path helper utilities
- [x] Add retry helper for controlled cases only
- [x] Add timestamp helper if needed
- [x] Add environment helper methods

---

# Phase 4: UI Automation Layer

## UI Framework Base
- [x] Create `base_page.py`
- [x] Add common page actions
- [x] Add page load verification helpers
- [x] Add common locator/wait patterns
- [x] Avoid hardcoded sleeps

## Page Objects
- [x] Create `login_page.py`
- [x] Create `dashboard_page.py`
- [x] Create `form_page.py`
- [x] Create `navigation_component.py` if needed
- [x] Keep page objects focused on interaction, not assertions overload

## UI Fixtures
- [x] Create browser fixture
- [x] Create page fixture
- [x] Create authenticated user fixture
- [x] Create test cleanup fixture
- [x] Support environment base URL fixture

## UI Tests
- [x] Add valid login test
- [x] Add invalid login test
- [x] Add navigation validation test
- [x] Add successful form submission test
- [x] Add export initiation from UI test (covered in test_navigation.py)

## UI Test Quality
- [x] Use stable selectors
- [x] Minimize brittle UI assumptions
- [x] Keep assertions meaningful
- [x] Ensure tests are isolated
- [x] Ensure tests pass headless

---

# Phase 5: API Automation Layer

## API Client Design
- [x] Create base API client
- [x] Add auth client
- [x] Add user/profile client
- [x] Add form submission client
- [x] Add export/report client

## API Assertions
- [x] Add response status validation helpers
- [x] Add schema validation helpers
- [x] Add payload integrity helpers
- [x] Add error response validation helpers

## API Fixtures
- [x] Create requests session fixture
- [x] Create auth token fixture
- [x] Create API base URL fixture
- [x] Create teardown/reset fixture if needed

## API Tests
- [x] Add valid login endpoint test
- [x] Add invalid login endpoint test
- [x] Add unauthorized access test
- [x] Add required field validation test (test_api_login_missing_email)
- [x] Add schema validation test (AUTH_LOGIN_RESPONSE_SCHEMA)
- [x] Add data integrity test (test_api_list_users)
- [x] Add export metadata response test (test_exports_api.py)

## API Test Quality
- [x] Separate transport concerns from assertions
- [x] Keep endpoint logic out of test bodies where possible
- [x] Avoid duplicate payload setup
- [x] Ensure negative cases are included

---

# Phase 6: System-Level Validation

## System Targets
- [x] Identify exported file output location (reports/export.csv)
- [x] Identify audit log location (reports/logs/audit.log)
- [x] Identify form submission data location (data/forms.json)

## System Utilities
- [x] Add file existence helper (tests/system utilities)
- [x] Add file content validation helper (CSV/JSON parsing)
- [x] Add log parsing helper (JSON-lines audit log parser)
- [x] Add polling helper for async artifact creation (bounded file wait)

## System Tests
- [x] Add audit log entry verification test
- [x] Add export file creation test
- [x] Add export file header/content validation test
- [x] Add form submission persistence test (covered in export test)

## System Test Quality
- [x] Avoid race conditions (bounded waits, file existence checks)
- [x] Use bounded waits, not lazy retry spam
- [x] Clean generated artifacts between runs
- [x] Keep filesystem assertions deterministic

---

# Phase 7: Test Organization and Execution Strategy

## Markers and Tags
- [x] Add `smoke` marker
- [x] Add `regression` marker
- [x] Add `ui` marker
- [x] Add `api` marker
- [x] Add `system` marker
- [x] Register markers in `pytest.ini`

## Parallel Execution
- [x] Enable `pytest-xdist` (in requirements.txt)
- [x] Confirm tests remain isolated in parallel (async fixtures, fresh page per test)
- [x] Document test parallelization (in README)

## Reporting
- [x] Enable HTML test reports (pytest-html in requirements.txt)
- [x] Store reports in `reports/`
- [x] Configure report generation in Makefile/CI

## Execution Commands
- [x] Add make command for full suite
- [x] Add make command for smoke suite
- [x] Add make command for UI suite
- [x] Add make command for API suite
- [x] Add make command for system suite
- [x] Add make command for lint
- [x] Add make command for format

---

# Phase 8: CI/CD Integration

## GitHub Actions Workflow
- [x] Create `.github/workflows/ci.yml`
- [x] Add checkout step
- [x] Add Python setup step
- [x] Add dependency install step
- [x] Add Playwright browser install step
- [x] Add test execution step
- [x] Fail workflow on test failures

## CI Strategy
- [x] Run on push
- [x] Run on pull request
- [x] Keep CI deterministic and fast

## CI Enhancements
- [x] Add dependency caching
- [x] Add HTML report artifact upload
- [x] Ensure CI config is clearly explained in README
---

# Phase 9: Documentation and Portfolio Polish

## README Core Sections
- [x] Add project problem statement
- [x] Add architecture overview with diagram
- [x] Add folder structure explanation
- [x] Add tech stack explanation with table
- [x] Add test strategy philosophy
- [x] Add local setup steps
- [x] Add run commands (with examples)
- [x] Add CI/CD explanation
- [x] Add test organization by layer
- [x] Add future improvements section
- [x] Add troubleshooting section

## Architecture Explanation
- [x] Explain why Playwright was chosen
- [x] Explain why layered testing matters
- [x] Explain separation of concerns
- [x] Explain how maintainability was prioritized
- [x] Include example login flow across layers

## Interview Readiness
- [x] Explanation for page object design
- [x] Explanation for fixture strategy
- [x] Explanation for API abstraction
- [x] Explanation for system-level validation
- [x] Explanation for CI pipeline choices
- [x] Explanation for handling flaky tests

## Optional Upgrades
- [x] Add Dockerized execution
- [ ] Add seeded database reset flow if app grows
- [x] Add multi-browser execution in CI
- [x] Add screenshot-on-failure support
- [x] Add multi-browser execution in CI (matrix strategy)
- [x] Add contract-testing discussion or example
- [x] Add performance baseline testing
- [x] Add seeded Faker-based data variation tests
- [x] Add Allure reporting for richer test history
- [x] Add mock external service behavior

## Framework Quality
- [x] Repo structure is clean and professional
- [x] Test layers are clearly separated
- [x] Naming is consistent
- [x] Logs and reports are useful
- [x] README is polished and interview-ready
- [x] Tests are deterministic under local and CI execution
- [x] CI is running and understandable

## Portfolio Quality
- [x] Project looks like real engineering work
- [x] Architecture choices are explainable
- [x] Generic enough for broad QA / SDET roles
- [x] No obvious tutorial-clone smell
- [x] Strong enough to discuss in interviews and on resume
