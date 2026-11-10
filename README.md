<div align="center">

# 🐍 QA Brains Automation — Python · Playwright · Behave (BDD)

### UI test automation for the QA Brains practice site. 15 Gherkin scenarios cover login, logout, registration, forgot password, the e-commerce cart and the demo modules. They run headless on Chromium and Firefox in GitHub Actions.

[![Typing SVG](https://readme-typing-svg.demolab.com/?font=Fira+Code&size=18&pause=1500&color=3776AB&center=true&vCenter=true&width=900&repeat=true&lines=Python+3.12+%C2%B7+Playwright+%C2%B7+Behave;Login+%C2%B7+Registration+%C2%B7+Cart+%C2%B7+Smoke+%C2%B7+Regression;15+%2F+15+scenarios+%C3%97+Chromium+%C2%B7+Firefox)](https://git.io/typing-svg)

<!-- ============ STATUS BAR ============ -->
[![CI](https://github.com/rbchy/QaBrainsAutomationPythonPlawright/actions/workflows/ci.yml/badge.svg)](https://github.com/rbchy/QaBrainsAutomationPythonPlawright/actions/workflows/ci.yml)
![Scenarios](https://img.shields.io/badge/Scenarios-15%20%2F%2015%20passed-22c55e?style=for-the-badge&logo=checkmarx&logoColor=white)
![Browsers](https://img.shields.io/badge/Browsers-Chromium%20%C2%B7%20Firefox-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Unit](https://img.shields.io/badge/pytest-15%20%2F%2015-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-sync%20API-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)
![Behave](https://img.shields.io/badge/Behave-1.2.6-23D96C?style=for-the-badge&logo=cucumber&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

![Last Commit](https://img.shields.io/github/last-commit/rbchy/QaBrainsAutomationPythonPlawright?style=flat-square&color=3776ab&label=Last%20commit)
![Repo Size](https://img.shields.io/github/repo-size/rbchy/QaBrainsAutomationPythonPlawright?style=flat-square&color=155e75&label=Repo%20size)

</div>

---

## 📌 At a Glance

<table>
<tr>
<td width="50%" valign="top">

**🙋 What this is**

A **Behave (Gherkin) + Playwright for Python** framework that tests the live **[QA Brains practice site](https://practice.qabrains.com/)**:

- the login demo: valid and invalid accounts, logout
- registration and forgot password, including the browser's own e-mail validation
- the **e-commerce demo**: adding and removing products, with the cart checked again after a reload
- product cards and details, and the sidebar demo modules

Each scenario gets a fresh browser. The suite runs **headless on Chromium and Firefox** in GitHub Actions on every push and once a week, because the live site can change. A failure saves a screenshot and prints the page text into the log.

</td>
<td width="50%" valign="top">

**📍 Quick facts**

| | |
|---|---|
| 🌐 **Site under test** | practice.qabrains.com (live) |
| 🧪 **Scenarios** | 15 in 7 feature files · 49 steps |
| 🧩 **Unit tests** | 15 (pytest, no browser) |
| 🌍 **Browsers** | Chromium · Firefox (headless in CI) |
| ⏱️ **Run time** | ≈ 51 s (Chromium) · ≈ 54 s (Firefox) |
| 🧱 **Pattern** | Page Object Model, browser per scenario |
| 📊 **Reports** | JUnit XML · Behave JSON · failure screenshots |
| 🔁 **Runs** | push · PR · manual · weekly |

</td>
</tr>
</table>

---

## ✅ Latest Results (GitHub Actions)

| Feature file | Scenarios | What is asserted | Chromium | Firefox |
|---|---:|---|:---:|:---:|
| 🔐 `Login.feature` | 2 | valid → `?logged=true` + success banner · invalid → *"Your email and password both are invalid!"*, no banner | ✅ 2 | ✅ 2 |
| 🚪 `Logout.feature` | 1 | `logged=true` gone, Login button back, no banner | ✅ 1 | ✅ 1 |
| 📝 `Registration.feature` | 2 | unique e-mail → *successfully* · e-mail without `@` blocked by the browser (`typeMismatch`) | ✅ 2 | ✅ 2 |
| 🔑 `ForgotPassword.feature` | 2 | valid → `?forgot=true` + *"Password is reset successfully"* · malformed → browser validation, no banner | ✅ 2 | ✅ 2 |
| 🛒 `CartCheckout.feature` | 2 | starts empty · add → exactly 1, still 1 after reload · remove → 0, still 0 after reload | ✅ 2 | ✅ 2 |
| 🔄 `RegressionTests.feature` | 3 | add 3 → exactly 3 · details page shows name and price · every card has name, price and one *Add to cart* | ✅ 3 | ✅ 3 |
| 💨 `SmokeTests.feature` | 3 | home login form · 5 demo modules open from the sidebar | ✅ 3 | ✅ 3 |
| **Total** | **15** | | **15 / 15** | **15 / 15** |

```mermaid
pie showData
    title 15 scenarios by area
    "Login + Logout (3)" : 3
    "Registration (2)" : 2
    "Forgot password (2)" : 2
    "Cart (2)" : 2
    "Regression shop (3)" : 3
    "Smoke (3)" : 3
```

```mermaid
pie showData
    title 30 scenario runs (15 x 2 browsers)
    "Passed" : 30
    "Failed" : 0
```

```mermaid
xychart-beta
    title "Scenarios per feature file"
    x-axis ["Login", "Logout", "Registration", "ForgotPwd", "Cart", "Regression", "Smoke"]
    y-axis "Scenarios" 0 --> 4
    bar [2, 1, 2, 2, 2, 3, 3]
```

```mermaid
xychart-beta
    title "Before vs after this rework"
    x-axis ["Passed (before, local)", "Errored (before)", "Passed Chromium (now)", "Passed Firefox (now)"]
    y-axis "Scenarios" 0 --> 16
    bar [11, 4, 15, 15]
```

> **Before:** the last local run (`run_output.txt`) had 11 passed and 4 errored, and several of the 11 could not fail (see the Maintenance Log). **Now** every step asserts something concrete. The first CI run caught a real cross-browser difference: Firefox words the invalid-e-mail message differently from Chromium.

---

## 🏗️ Framework Architecture

```mermaid
flowchart LR
    subgraph Gherkin["📝 features/*.feature"]
        F[7 feature files<br/>15 scenarios]
    end
    subgraph Steps["🧩 features/steps"]
        A[auth_steps.py]
        S[shop_steps.py]
        M[smoke_steps.py]
    end
    subgraph Pages["📄 pages (Page Objects)"]
        LP[LoginPage]
        RP[RegistrationPage]
        FP[ForgotPasswordPage]
        SP[ShopPage]
    end
    subgraph Utils["🧰 utils"]
        BT[BaseTest<br/>browser per scenario]
        CR[ConfigReader<br/>properties + env]
    end
    ENV[environment.py<br/>hooks · screenshot on failure]
    F --> Steps --> Pages
    ENV --> BT
    BT --> CR
    Pages --> PW[Playwright<br/>Chromium · Firefox]
    PW --> SITE[(practice.qabrains.com)]
```

### CI pipeline

```mermaid
flowchart TD
    P([push / PR / manual / weekly]) --> U[Job 1: pytest<br/>config · price pattern · tags]
    U --> D[behave --dry-run --strict<br/>no undefined steps]
    D -->|green| M{matrix}
    M --> C[Chromium headless]
    M --> F[Firefox headless]
    C & F --> B[behave → JSON + JUnit XML]
    B --> S[Step summary per feature]
    B --> R[(Artifacts: reports +<br/>failure screenshots)]
```

### One scenario: the cart survives a reload

```mermaid
sequenceDiagram
    autonumber
    participant B as Behave
    participant H as environment.py
    participant S as ShopPage
    participant W as practice.qabrains.com
    H->>W: new browser + page (base_url)
    B->>S: login() as test@qabrains.com
    S->>W: /ecommerce/login → product grid
    B->>S: empty_cart()
    loop while "Remove from cart" buttons exist
        S->>W: click Remove, wait until count − 1
    end
    B->>S: add_one()
    S->>W: click "Add to cart", wait until removes = 1
    B->>S: reload()
    S->>W: GET /ecommerce
    W-->>B: still exactly 1 "Remove from cart"
    H->>W: close browser (screenshot + page text if failed)
```

### Login state

```mermaid
stateDiagram-v2
    [*] --> LoginForm: open /
    LoginForm --> LoggedIn: qa_testers@qabrains.com / Password123
    LoginForm --> Error: wrong e-mail or password
    Error --> LoginForm: try again
    LoggedIn --> LoginForm: Log out
    note right of LoggedIn: URL has ?logged=true, success banner shown
    note right of Error: "Your email and password both are invalid!"
```

---

## 🧪 Test Coverage

```mermaid
mindmap
  root((15 scenarios))
    Login 2
      valid account
      invalid account message
    Logout 1
      banner gone, login back
    Registration 2
      unique e-mail
      missing @ blocked
    Forgot password 2
      reset success banner
      malformed e-mail blocked
    Cart 2
      add 1 survives reload
      remove survives reload
    Regression 3
      add 3 products
      product details
      every card complete
    Smoke 3
      home page
      4 demo modules
      e-commerce site
```

| Tag | Scenarios | Run with |
|---|---:|---|
| `@smoke` | 9 | `behave --tags=@smoke` |
| `@regression` | 12 | `behave --tags=@regression` |
| `@Login` · `@Logout` · `@Registration` · `@ForgotPassword` · `@Cart` · `@Shop` | 2 · 1 · 2 · 2 · 3 · 2 | `behave --tags=@Cart` |

---

## ▶️ Running Locally

**Prerequisites:** Python 3.10+.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium firefox

behave                               # all 15 scenarios, headed Chromium (config.properties)
HEADLESS=true behave                 # headless
BROWSER=firefox HEADLESS=true behave # Firefox
behave --tags=@smoke                 # one tag
python -m pytest                     # unit tests for the helpers
```

| Setting | `config/config.properties` | Env var override |
|---|---|---|
| Site URL | `url` | `BASE_URL` |
| Browser | `browser=chromium` | `BROWSER` (`chromium` · `firefox` · `webkit`) |
| Headless | `headless=false` | `HEADLESS=true` |
| Timeout | `timeout=15000` (ms) | |

The accounts in `config.properties` (`qa_testers@qabrains.com`, `test@qabrains.com`, `Password123`) are the **public practice accounts published by QA Brains**.

---

## 📁 Project Structure

```text
QaBrainsAutomationPythonPlawright/
├── .github/workflows/ci.yml        # pytest → Behave on Chromium + Firefox
├── behave.ini                      # paths, JUnit output
├── config/config.properties        # URL, browser, timeout, practice accounts
├── features/
│   ├── *.feature                   # 7 feature files, 15 scenarios
│   ├── environment.py              # hooks: browser per scenario, failure capture
│   └── steps/                      # auth_steps · shop_steps · smoke_steps
├── pages/                          # LoginPage · RegistrationPage · ForgotPasswordPage · ShopPage
├── utils/                          # BaseTest · ConfigReader
├── tests/test_config_reader.py     # 15 pytest unit tests
└── requirements.txt
```

---

## 🧹 Maintenance Log

| Area | Before | Now |
|---|---|---|
| Last run | 11 passed, **4 errored** (cart × 3, login) | 15 / 15 on Chromium and Firefox |
| R-02 / R-03 | placeholders: `assert True`, quantity set to the expected value | replaced by real checks: product details, every product card |
| Smoke navigation | asserted only that the URL was not empty; jumped to `/catalog`, `/wishlist`, `/refer`, which are not on the site | clicks the real sidebar items and checks each URL |
| Cart | "added" = any element whose class contains *cart* | cart size = number of *Remove from cart* buttons, checked again after a reload |
| Forgot password | passed if the text contained `@` or *success* anywhere | exact banner, `?forgot=true`, browser validity state |
| Browser | always headed, `config.properties` ignored, URL hard-coded in 3 places | one `BaseTest`, config + env overrides, `base_url` |
| Duplicates | `BaseTest`, `DriverFactory` and `DriverHelper` all started browsers | one `BaseTest` |
| Failure evidence | screenshot only | screenshot + URL + page text in the CI log |
| Repo | `allure-results/`, `reports/`, `run_output.txt`, a stray zip of the project (`zi12CsSI`) committed | removed; `.gitignore` |
| CI | none | GitHub Actions: pytest, dry-run for undefined steps, 2-browser matrix, weekly run |

---

## 📈 Roadmap

- [x] Headless CI on Chromium and Firefox
- [x] Every step asserts something that can fail
- [ ] WebKit in the matrix
- [ ] Allure report published to GitHub Pages
- [ ] Form Submission and Drag-and-Drop demo modules covered beyond navigation
- [ ] Run scenarios in parallel (`behavex`)

---

## 🔗 Related Projects

Same site, same scenarios, other stacks:

| Repo | Stack |
|---|---|
| [QaBrainsAutomationTypeScriptPlaywright](https://github.com/rbchy/QaBrainsAutomationTypeScriptPlaywright) | TypeScript · Playwright · Cucumber |
| [QaBrainsAutomationJavaPlaywright](https://github.com/rbchy/QaBrainsAutomationJavaPlaywright) | Java · Playwright · Cucumber · TestNG |
| [QaBrainsAutomationJavaSelenium](https://github.com/rbchy/QaBrainsAutomationJavaSelenium) | Java · Selenium · Cucumber |
| [QaBrainsAutomationCypressJavaScript](https://github.com/rbchy/QaBrainsAutomationCypressJavaScript) | JavaScript · Cypress |
| [rbchy](https://github.com/rbchy/rbchy) | Profile and full project list |

---

## ⚠️ Disclaimer

Educational / portfolio project, not affiliated with QA Brains. The tests run against a public practice site, so a change there can break a scenario. That is why CI also runs weekly.

---

## 👤 Author

<div align="center">

**Ranajit Baran Chowdhury (RB Chowdhury)**
QA Automation Engineer / SDET · West Norriton, Pennsylvania, USA

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rbchy/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rbchy)
[![Website](https://img.shields.io/badge/Website-rbchy.github.io%2Frbchy-0d9488?style=for-the-badge&logo=githubpages&logoColor=white)](https://rbchy.github.io/rbchy/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Website-blueviolet?style=for-the-badge&logo=wix&logoColor=white)](https://rbc6543.wixsite.com/rbc-portfolio)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:chyranajit@gmail.com)

⭐ *If this project helps you, a star on the repo is appreciated.*

</div>
