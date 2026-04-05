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
- [ ] Add valid login test
- [ ] Add invalid login test
- [ ] Add locked/disabled user test if included
- [ ] Add navigation validation test
- [ ] Add required field validation test
- [ ] Add successful form submission test
- [ ] Add export initiation from UI test

## UI Test Quality
- [ ] Use stable selectors
- [ ] Minimize brittle UI assumptions
- [ ] Keep assertions meaningful
- [ ] Ensure tests are isolated
- [ ] Ensure tests pass headless

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
- [ ] Add required field validation test
- [ ] Add schema validation test
- [ ] Add data integrity test
- [ ] Add export metadata response test

## API Test Quality
- [x] Separate transport concerns from assertions
- [x] Keep endpoint logic out of test bodies where possible
- [x] Avoid duplicate payload setup
- [ ] Ensure negative cases are included

---

# Phase 6: System-Level Validation

## System Targets
- [ ] Identify exported file output location
- [ ] Identify audit log location
- [ ] Identify background job signal/output if included

## System Utilities
- [ ] Add file existence helper
- [ ] Add file content validation helper
- [ ] Add log parsing helper
- [ ] Add polling helper for async artifact creation if needed

## System Tests
- [ ] Add export file creation test
- [ ] Add export file header/content validation test
- [ ] Add audit log entry verification test
- [ ] Add background artifact status verification test if included

## System Test Quality
- [ ] Avoid race conditions
- [ ] Use bounded waits, not lazy retry spam
- [ ] Clean generated artifacts between runs
- [ ] Keep filesystem assertions deterministic

---

# Phase 7: Test Organization and Execution Strategy

## Markers and Tags
- [ ] Add `smoke` marker
- [ ] Add `regression` marker
- [ ] Add `ui` marker
- [ ] Add `api` marker
- [ ] Add `system` marker
- [ ] Register markers in `pytest.ini`

## Parallel Execution
- [ ] Enable `pytest-xdist`
- [ ] Confirm tests remain isolated in parallel
- [ ] Document any tests that must remain serial

## Reporting
- [ ] Enable HTML test reports
- [ ] Store reports in `reports/`
- [ ] Include failure screenshots for UI tests if practical
- [ ] Include logs or output artifacts in reports where useful

## Execution Commands
- [ ] Add make command for full suite
- [ ] Add make command for smoke suite
- [ ] Add make command for UI suite
- [ ] Add make command for API suite
- [ ] Add make command for system suite
- [ ] Add make command for lint
- [ ] Add make command for format

---

# Phase 8: CI/CD Integration

## GitHub Actions Workflow
- [ ] Create `.github/workflows/ci.yml`
- [ ] Add checkout step
- [ ] Add Python setup step
- [ ] Add dependency install step
- [ ] Add Playwright browser install step
- [ ] Add lint step
- [ ] Add test execution step
- [ ] Add HTML report artifact upload step
- [ ] Fail workflow on test failures

## CI Strategy
- [ ] Run on push
- [ ] Run on pull request
- [ ] Consider manual workflow dispatch
- [ ] Keep CI deterministic and fast enough to be practical

## CI Enhancements
- [ ] Add dependency caching
- [ ] Add matrix build for Python versions if worthwhile
- [ ] Separate smoke vs full suite if needed
- [ ] Ensure CI config is clearly explained in README

---

# Phase 9: Documentation and Portfolio Polish

## README Core Sections
- [ ] Add project problem statement
- [ ] Add architecture overview
- [ ] Add folder structure explanation
- [ ] Add tech stack explanation
- [ ] Add test strategy philosophy
- [ ] Add local setup steps
- [ ] Add run commands
- [ ] Add CI/CD explanation
- [ ] Add reporting explanation
- [ ] Add sample output/screenshots
- [ ] Add future improvements section

## Architecture Explanation
- [ ] Explain why Playwright was chosen
- [ ] Explain why layered testing matters
- [ ] Explain why deterministic data matters
- [ ] Explain separation of concerns
- [ ] Explain how maintainability was prioritized

## Interview Readiness
- [ ] Prepare explanation for page object design
- [ ] Prepare explanation for fixture strategy
- [ ] Prepare explanation for API abstraction
- [ ] Prepare explanation for system-level validation
- [ ] Prepare explanation for CI pipeline choices
- [ ] Prepare explanation for handling flaky tests responsibly

---

# Phase 10: Stretch Features

## Optional Upgrades
- [ ] Add Dockerized execution
- [ ] Add seeded database reset flow if app grows
- [ ] Add multi-browser execution in CI
- [ ] Add screenshot-on-failure support
- [ ] Add mock external service behavior
- [ ] Add contract-testing discussion or example
- [ ] Add coverage reporting if meaningful
- [ ] Add lightweight dependency injection if helpful but not overbuilt

---

# Definition of Done

## Framework Quality
- [ ] Repo structure is clean and professional
- [ ] Tests are deterministic
- [ ] Test layers are clearly separated
- [ ] Naming is consistent
- [ ] Logs and reports are useful
- [ ] CI is running and understandable
- [ ] README is polished and interview-ready

## Portfolio Quality
- [ ] Project looks like real engineering work
- [ ] Architecture choices are explainable
- [ ] No obvious tutorial-clone smell
- [ ] Generic enough for broad QA / SDET roles
- [ ] Strong enough to discuss in interviews and on resume