# saas-quality-automation-framework

A production-grade Python QA automation framework demonstrating professional test architecture, maintainability, and deterministic design. Implements layered validation (UI, API, and system) for a realistic SaaS-style Flask application.

## ⚡ At A Glance

- Layered coverage across UI, API, and system tests
- Deterministic default suite with opt-in performance and data-variation lanes
- Browser-matrix CI (`chromium`, `firefox`) with lint gating and artifact uploads
- Dockerized execution path for portable local and CI-style runs
- Recent local run: `33 passed, 1 skipped` with HTML reporting enabled

## 📋 Overview

This project showcases SDET/QA engineering principles through:

- **Scalable test architecture** — Separated concerns across UI (Playwright), API (requests), and system-level tests
- **Maintainable design** — Page objects, reusable fixtures, abstracted assertions
- **Deterministic execution** — Seeded test data, controlled environment setup, no flaky waits
- **Professional CI/CD** — GitHub Actions pipeline with environment-aware headless execution
- **Actionable failure artifacts** — HTML reports, logs, and UI screenshots for fast triage
- **Interview-ready clarity** — Every design choice is explainable and purposeful

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           Test Execution Layer              │
│  ┌──────────┬──────────┬─────────────────┐  │
│  │   UI     │   API    │     System      │  │
│  │ Tests    │  Tests   │      Tests      │  │
│  └──────────┴──────────┴─────────────────┘  │
├─────────────────────────────────────────────┤
│          Abstraction & Fixtures             │
│  ┌──────────┬──────────┬─────────────────┐  │
│  │ Pages &  │ Clients  │ Services &      │  │
│  │ Components│ Schemas │ Utilities       │  │
│  └──────────┴──────────┴─────────────────┘  │
├─────────────────────────────────────────────┤
│     Flask Application Under Test            │
│   (Login, Dashboard, Forms, Exports)        │
└─────────────────────────────────────────────┘
```

### Design Principles

1. **Page Object Model** — Page interaction logic isolated from assertions
2. **Client Abstraction** — HTTP requests abstracted; tests drive behavior, not URLs
3. **Schema Validation** — Responses validated against defined schemas before assertions
4. **Organized Fixtures** — Browser, authentication, and data fixtures cleanliness
5. **Deterministic Data** — Seed data explicitly defined; tests repeatably pass in any environment
6. **Bounded Waits** — Playwright implicit waits; no arbitrary sleeps
7. **Layered Assertions** — Status → schema → content integrity

---

## 📁 Folder Structure

```
.
├── app/                          # Flask application under test
│   └── main.py                   # Login, dashboard, forms, exports, audit logging
├── src/                          # Test automation framework
│   ├── api/
│   │   ├── clients/              # HTTP clients (auth, users, forms, exports)
│   │   ├── schemas/              # Response schema definitions (JSON Schema)
│   │   └── assertions/           # Reusable response assertions
│   ├── pages/                    # Playwright page objects (login, dashboard, form)
│   ├── services/                 # Test helper services (auth, export, logging)
│   ├── models/                   # Test data models
│   └── utils/                    # Config, logging, data loading, path helpers, retry
├── tests/
│   ├── api/                      # API endpoint tests (auth, users, exports)
│   ├── ui/                       # Playwright UI tests (login, navigation, forms)
│   ├── system/                   # System-level validation (audit logs, file creation)
│   └── conftest.py               # Fixtures: browser, page, auth, clients
├── config/                       # Environment configs (dev, ci, settings)
├── data/                         # Test data (users, forms, exports, expected outputs)
├── reports/                      # Test reports and logs
├── pytest.ini                    # Pytest configuration + markers + HTML report output
├── Makefile                      # Build and test commands
└── requirements.txt              # Python dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Browser Automation** | Playwright (async) | Deterministic, fast, cross-browser UI testing |
| **Test Framework** | Pytest + pytest-asyncio | Test discovery, fixtures, async support |
| **HTTP Client** | Requests | RESTful API testing |
| **Validation** | JSON Schema (jsonschema) | Response schema validation |
| **Code Quality** | Black + Ruff | Formatting and linting |
| **CI/CD** | GitHub Actions | Automated test execution and reporting |
| **Configuration** | PyYAML | Environment-specific settings |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Git

### Installation

```bash
git clone <repo-url>
cd saas-quality-automation-framework

# Install dependencies and Playwright browsers
make install
```

This will:
- Install Python packages from `requirements.txt`
- Download Playwright browsers for headless execution

### Configuration

Test behavior is controlled via environment config:

```bash
# Development mode (default)
export ENV=dev

# CI mode (headless, stricter)
export ENV=ci
```

Configs are in [`config/`](config/):
- `settings.yaml` — Shared settings
- `dev.yaml` — Local development (headless: false, browser: chromium, base_url: http://localhost:5000)
- `ci.yaml` — CI environment (headless: true, browser: chromium, base_url: http://localhost:5000)

You can override the browser per run:

```bash
BROWSER=firefox pytest tests/ui -m ui
```

---

## ▶️ Running Tests

### Local Execution

```bash
# Run all tests
make test

# Run by test layer
make test-ui          # Playwright UI tests only
make test-api         # API tests only
make test-system      # System-level validation tests
make test-smoke       # Critical path tests (fastest)

# Run specific test
pytest tests/ui/test_login.py -v
pytest -k "test_login_with_valid" -v

# Parallel execution (pytest-xdist)
pytest -n auto        # Uses all CPU cores

# Run seeded data-variation tests
pytest -m data_variation
```

### Test Output

Each test run generates:
- Console output with pass/fail status
- HTML report in `reports/`
- Test logs in `reports/logs/`
- Failure screenshots in `reports/screenshots/` for UI test failures
- Audit log from Flask app

Example:
```
tests/ui/test_login.py::test_login_with_valid_credentials PASSED
tests/api/test_auth_api.py::test_api_login_valid_credentials PASSED
tests/system/test_audit_log_entries.py::test_successful_login_creates_audit_entry PASSED

========================= 3 passed in 2.15s =========================
HTML test report: reports/pytest-report.html
```

---

## 📊 Test Organization

### Markers

Tests are tagged for selective execution:

```bash
pytest -m smoke           # Critical path (fastest validation)
pytest -m regression      # Broader validation
pytest -m ui              # UI/UI-level tests only
pytest -m api             # API tests only
pytest -m system          # System artifact validation
```

Markers are defined in [`pytest.ini`](pytest.ini).

### Test Layers

#### UI Tests (`tests/ui/`)
- **Technology:** Playwright (async)
- **Scope:** User workflows via browser
- **Examples:**
  - Login with valid/invalid credentials
  - Dashboard navigation
  - Form submission with validation
- **Isolation:** Each test gets a fresh browser page; logout/cleanup on teardown

#### API Tests (`tests/api/`)
- **Technology:** Requests + JSON Schema
- **Scope:** HTTP endpoint contracts and payloads
- **Examples:**
  - Login endpoint returns 200 + valid token
  - User listing returns schema-valid array
  - Unauthorized access returns 401
- **Isolation:** Tests are independent; no shared session state

#### System Tests (`tests/system/`)
- **Technology:** File I/O + log parsing
- **Scope:** Side effects and artifacts (audit logs, exported files)
- **Examples:**
  - Audit log entry created after successful login
  - Export file generated with correct CSV headers
  - Submitted form data persisted to JSON
- **Setup:** The pytest session boots the Flask app automatically; tests clean artifacts and validate expected state

---

## 🧪 Example: Testing a Login Flow

### Test Code (UI Layer)

```python
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_login_with_valid_credentials(login_page):
    """Test login with valid credentials."""
    await login_page.navigate()
    await login_page.login("testuser@example.com", "password123")
    
    current_url = await login_page.get_url()
    assert "/dashboard" in current_url
```

### Abstraction (Page Object)

```python
class LoginPage(BasePage):
    async def login(self, email: str, password: str):
        await self.page.fill('[name="email"]', email)
        await self.page.fill('[name="password"]', password)
        await self.page.click('button[type="submit"]')
        await self.page.wait_for_load_state("networkidle")
```

### API Validation (API Layer)

```python
@pytest.mark.api
@pytest.mark.smoke
def test_api_login_valid_credentials(auth_client):
    """Test API login endpoint."""
    result = auth_client.login("testuser@example.com", "password123")
    
    assert_status_code(result["response"], 200)
    assert_schema_valid(result["response"], AUTH_LOGIN_RESPONSE_SCHEMA)
```

### System Validation (System Layer)

```python
@pytest.mark.system
def test_successful_login_creates_audit_entry(auth_client, audit_log_path):
    """Test that successful login creates audit log entry."""
    auth_client.login("testuser@example.com", "password123")
    
    log_entries = parse_audit_log(audit_log_path)
    assert any(e["action"] == "login_successful" for e in log_entries)
```

---

## 📈 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`):

1. **On Push/PR:** Automatically runs test suite
2. **Setup:** Python 3.11 + dependencies + Playwright browsers
3. **Execution:** Full pytest run in headless mode across a browser matrix
4. **Reporting:** HTML report, logs, and screenshots uploaded as artifacts
5. **Status:** Workflow fails on any test failure

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: python -m playwright install --with-deps chromium firefox
      - run: ENV=ci BROWSER=${{ matrix.browser }} pytest
```

View results: **Actions tab** → relevant commit/PR

---

## 🎯 Key Design Decisions

### Why Playwright?

- **Async support:** Fast, parallel test execution
- **Cross-browser:** Works in Chrome, Firefox, Safari
- **Deterministic:** Implicit waits, no arbitrary sleeps
- **Headless-friendly:** CI-ready out-of-the-box

### Why Layered Testing?

- **UI tests** catch user-visible bugs quickly
- **API tests** validate contracts and payloads (faster than UI)
- **System tests** confirm side effects (audit logs, file generation)
- **Together** they catch integration bugs no single layer can

### Why Fixtures Over Page Classes?

- Fixtures are stateless and composable
- Tests focus on *what* to test, not *how* to manage objects
- Cleaner test code; less fixture boilerplate

### Why Deterministic Data?

- Tests must pass in any environment (local, CI, team machine)
- Flaky tests erode confidence and slow teams down
- Seed data + idempotent setup = reliable tests

---

## 🔍 Running Locally for Development

### Setup

```bash
# Install framework and browsers
make install

# Run tests (pytest starts the Flask app automatically)
make test
```

### Debugging

```bash
# Run single test with verbose output
pytest tests/ui/test_login.py::test_login_with_valid_credentials -vv

# Run with print statement capture
pytest tests/ui/test_login.py -vs

# Run with development config (headful browser)
ENV=dev pytest tests/ui/test_login.py

# Run UI tests in Firefox
BROWSER=firefox pytest tests/ui -m ui

# Run with debugger (pdb)
pytest tests/ui/test_login.py --pdb
```

### Dockerized Execution

```bash
# Build the container image
make docker-build

# Run the full suite in the container
make docker-test
```

### Code Quality

```bash
# Format code
make format

# Check linting/formatting
make lint
```

---

## 📋 Test Data & Fixtures

### Seed Users

Defined in [`data/users.json`](data/users.json):

```json
{
  "users": [
    {
      "email": "testuser@example.com",
      "name": "Test User"
    },
    {
      "email": "admin@example.com",
      "name": "Admin User"
    }
  ]
}
```

### Fixtures (conftest.py)

```python
@pytest.fixture
async def browser():
    """Playwright browser instance."""
    async with async_playwright() as p:
        browser_type = getattr(p, os.getenv("BROWSER", config["browser"]))
        browser = await browser_type.launch(headless=config["headless"])
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    """Fresh browser page per test."""
    page = await browser.new_page()
    yield page
    await page.close()  # Cleanup after test

@pytest.fixture
def auth_client(config):
    """HTTP client for auth endpoints."""
    return AuthClient(config["api_base_url"])
```

---

## 🐛 Troubleshooting

### Tests hang/timeout

- Check the test-started app is reachable: `curl http://localhost:5000/login`
- Run single test to isolate: `pytest tests/ui/test_login.py::test_name -v`
- Temporarily increase the configured timeout in `config/dev.yaml`

### Playwright browser not found

```bash
python -m playwright install chromium
```

### Import errors

```bash
pip install -r requirements.txt
export PYTHONPATH=.
pytest
```

### Tests flaky in CI but pass locally

- Check environment variables: `echo $ENV`
- Check browser selection: `echo $BROWSER`
- Verify seed data is committed
- Ensure no hardcoded local paths
- Use time-bounded waits, not sleeps

### Screenshot support

- UI failures automatically save screenshots to `reports/screenshots/`
- CI uploads screenshots alongside the HTML report and logs

---

## 🚧 Future Enhancements

- [x] Screenshot-on-failure for UI tests
- [x] Multi-browser matrix execution (Chromium and Firefox)
- [x] Mock external service behavior for form notifications
- [x] Lightweight performance baseline lane for API login
- [x] Allure result generation support
- [ ] Database seeding/reset utilities
- [ ] Coverage reporting (for code under test)
- [ ] Extend browser coverage to WebKit/Safari
- [ ] Add a richer contract-testing workflow beyond schema validation

---

## 📦 Additional Quality Hooks

### Contract Testing

This framework already uses JSON Schema validation as a lightweight contract-testing layer. Schemas in `src/api/schemas/` are asserted before content checks so response-shape regressions fail fast and read clearly.

### Performance Baseline

An opt-in performance lane is available for conservative API timing checks:

```bash
make test-performance
```

The baseline is intentionally separate from the main suite so functional stability stays the default priority.

### Seeded Data Variation

Faker-backed tests are available as an opt-in supplemental layer:

```bash
pytest -m data_variation
FAKE_DATA_SEED=12345 pytest -m data_variation
```

These tests use seeded randomness so any failure can be reproduced exactly. The main regression suite stays deterministic by default.

### Allure Reporting

You can generate Allure results locally with:

```bash
make test-allure
```

This writes raw results to `reports/allure-results/` for later visualization or publishing.

---

## 📚 Interview Talking Points

### Architecture & Design

- **Separation of concerns:** Why page objects, clients, and assertions are separate
- **Fixture strategy:** How fixtures simplify test code and improve isolation
- **Deterministic testing:** Why seed data and idempotent setup matter
- **Schema validation:** Catching contract violations before functional assertions

### Quality & Reliability

- **Flaky test prevention:** Bounded waits, idempotent setup, environment independence
- **Parallel execution:** How tests remain isolated despite xdist parallelization
- **CI strategy:** Why deterministic tests enable confident automation
- **Failure analysis:** How screenshots, logs, and HTML reports shorten debugging time
- **Debugging:** How logs, reports, and structured output aid troubleshooting

### Professional Judgment

- **When to add tests:** UI for user workflows, API for contracts, system for side effects
- **When NOT to test:** Trivial UI (button colors), library code, non-deterministic behavior
- **Test maintenance:** Keeping tests readable, avoiding brittle selectors, planned refactors

---

## 📄 License

MIT

---

**Built for portfolio demonstration. Generic, maintainable, and interview-ready.**
