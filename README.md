# QaBrainsAutomationPythonPlaywright
# QA Brains Automation — Python + Playwright + Behave

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.60-green?logo=playwright)
![Behave](https://img.shields.io/badge/Behave-BDD-orange)
![Allure](https://img.shields.io/badge/Report-Allure-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A **BDD (Behavior Driven Development)** test automation framework built with **Python**, **Playwright**, and **Behave** — converted from the original Java + Playwright + Cucumber project.

---

## 📁 Project Structure

```
qaBrainsAutomation_Python/
├── config/
│   └── config.properties        # App URL, credentials, browser settings
├── features/
│   ├── steps/                   # Step definition files
│   │   ├── common_steps.py
│   │   ├── login_steps.py
│   │   ├── logout_steps.py
│   │   ├── cart_steps.py
│   │   ├── registration_steps.py
│   │   ├── forgot_password_steps.py
│   │   ├── smoke_steps.py
│   │   └── regression_steps.py
│   ├── environment.py           # Hooks (Before/After scenarios)
│   ├── CartCheckout.feature
│   ├── ForgotPassword.feature
│   ├── Login.feature
│   ├── Logout.feature
│   ├── Registration.feature
│   ├── RegressionTests.feature
│   └── SmokeTests.feature
├── pages/                       # Page Object Model (POM)
│   ├── login_page.py
│   ├── logout_page.py
│   ├── cart_page.py
│   ├── registration_page.py
│   ├── forgot_password_page.py
│   ├── home_page.py
│   └── search_page.py
├── utils/                       # Utility classes
│   ├── base_test.py
│   ├── driver_factory.py
│   ├── driver_helper.py
│   └── config_reader.py
├── reports/                     # Test reports & screenshots
│   └── screenshots/
├── behave.ini                   # Behave configuration
└── requirements.txt             # Python dependencies
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Programming language |
| Playwright | Browser automation |
| Behave | BDD framework (Cucumber equivalent) |
| Allure | Test reporting |
| Gherkin | Feature file syntax |

---

## ⚙️ Prerequisites

- Python 3.9 or higher
- pip3
- Node.js (for Allure)
- Homebrew (Mac)

---

## 🚀 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/qaBrainsAutomation_Python.git
cd qaBrainsAutomation_Python
```

**2. Install dependencies:**
```bash
pip3 install -r requirements.txt
```

**3. Install Playwright browser:**
```bash
playwright install chromium
```

**4. Install Allure (for reports):**
```bash
brew install allure
pip3 install allure-behave
```

---

## ▶️ Running Tests

**Run all tests:**
```bash
behave
```

**Run only Smoke tests:**
```bash
behave --tags=@smoke
```

**Run only Regression tests:**
```bash
behave --tags=@regression
```

**Run a specific feature:**
```bash
behave features/Login.feature
```

**Run with Allure report:**
```bash
mkdir -p allure-results
python3 -m behave -f allure_behave.formatter:AllureFormatter -o allure-results --no-capture
allure serve allure-results
```

---

## 📊 Test Results

| Feature | Scenarios | Status |
|---------|-----------|--------|
| Login | 2 | ✅ Pass |
| Logout | 1 | ✅ Pass |
| Registration | 2 | ✅ Pass |
| Forgot Password | 2 | ✅ Pass |
| Smoke Tests | 3 | ✅ Pass |
| Regression R-02, R-03 | 2 | ✅ Pass |
| Cart (R-01, CartCheckout) | 3 | ⚠️ Skip* |

> **\* Known Issue:** The E-Commerce component on `practice.qabrains.com` fails to load (`Failed to fetch component data`). This is a server-side defect on the practice site, not an automation issue. Cart scenarios are tagged `@known_issue` and skipped gracefully.

---

## 🏗️ Framework Architecture

```
Feature Files (.feature)
        ↓
Step Definitions (features/steps/)
        ↓
Page Object Model (pages/)
        ↓
Browser Manager (utils/base_test.py)
        ↓
Playwright → Chrome Browser
```

### Key Design Patterns

- **Page Object Model (POM)** — Each page has its own class with locators and actions
- **BDD (Gherkin)** — Human-readable feature files using Given/When/Then
- **Hooks** — `environment.py` handles browser setup/teardown per scenario
- **Screenshot on Failure** — Auto-captures screenshot when any step fails
- **Known Issue Handling** — `@known_issue` tag skips broken site scenarios gracefully

---

## 🔧 Configuration

Edit `config/config.properties` to change settings:

```properties
url=https://practice.qabrains.com/
browser=chrome
headless=false
valid_email=qa_testers@qabrains.com
valid_password=Password123
```

---

## 📸 Screenshots

Failure screenshots are automatically saved to:
```
reports/screenshots/
```

---

## 🏷️ Tags

| Tag | Description |
|-----|-------------|
| `@smoke` | Critical path tests |
| `@regression` | Full regression suite |
| `@Login` | Login scenarios only |
| `@Logout` | Logout scenarios only |
| `@Registration` | Registration scenarios |
| `@ForgotPassword` | Password reset scenarios |
| `@known_issue` | Known site bugs — skipped |

---

## 📂 Comparison: Java vs Python

| Java | Python |
|------|--------|
| Maven (`pom.xml`) | pip (`requirements.txt`) |
| Playwright for Java | playwright-python |
| Cucumber JVM | Behave |
| TestNG | pytest / assert |
| `@Before / @After` | `before_scenario / after_scenario` |
| `camelCase` | `snake_case` |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Ranajit Baran Chowdhury**
QA Automation Engineer
- Email: chyranajit@gmail.com
- GitHub: [@ranajitchowdhury](https://github.com/ranajitchowdhury)
