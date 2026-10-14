# qa-automation-python

[![tests](https://github.com/ukitamakoto/qa-automation-python/actions/workflows/tests.yml/badge.svg)](https://github.com/ukitamakoto/qa-automation-python/actions/workflows/tests.yml)

**[View the latest test report →](https://ukitamakoto.github.io/qa-automation-python/)**

UI and API test automation in Python, written to be read: Page Objects, data-driven tests, JSON Schema validation, and a bug report for every defect the suite found.
35 tests: 23 UI tests (run in Chromium and Firefox) and 12 API tests.

| Layer | Target | Tools |
|---|---|---|
| UI | [SauceDemo](https://www.saucedemo.com), a demo shop by Sauce Labs | Playwright for Python, pytest |
| API | [Restful-Booker](https://restful-booker.herokuapp.com), a hotel-booking API made for test practice | requests, jsonschema, pytest |
| CI | GitHub Actions: lint, API job, UI job on Chromium and Firefox, HTML report published to GitHub Pages | ruff, pytest-html |

## Run it

```bash
uv sync
uv run playwright install chromium
uv run pytest                      # add --browser firefox to switch browsers
```

## What is tested

| Test | What it checks | Technique |
|---|---|---|
| `ui/test_login.py` · valid credentials | Login opens the inventory | Happy path |
| `ui/test_login.py` · invalid login (×4) | Exact error for a locked-out user, a wrong password, an empty username and an empty password | Equivalence partitioning |
| `ui/test_inventory.py` · sorting (×3) | Name Z→A, price low→high and price high→low reorder the list | Data-driven |
| `ui/test_inventory.py` · cart badge | The badge goes 0 → 2 → 1 → 0 as items are added and removed | State transition |
| `ui/test_inventory.py` · seeded users (×5) | Images, add-to-cart, sorting and listing prices for the users that ship with defects | Negative / exploratory follow-up |
| `ui/test_checkout.py` · end to end | Login → cart → checkout → overview → confirmation, with exact amounts | E2E happy path |
| `ui/test_checkout.py` · required fields (×3) | Each empty field blocks Continue with its own message | Field validation |
| `ui/test_checkout.py` · order total | Item total + 8% tax = total for the whole catalogue, computed with `Decimal` | Oracle from data |
| `ui/test_checkout.py` · seeded defects (×4) | Rounding, form fields and Finish | Negative |
| `api/test_auth.py` (×2) | A token for valid credentials; the status code for wrong ones | Positive / negative |
| `api/test_booking.py` (×10) | Create (schema-validated), read, full and partial update, delete, filter, authorization, invalid and impossible payloads | CRUD, schema validation, authorization, negative |

## Bugs found

Each defect is reproduced by a test marked `xfail(strict=True)`. The suite stays green while the bug exists, and it fails loudly the day the bug is fixed, so the report can be closed.

| ID | Summary | Severity |
|---|---|---|
| [BUG-001](docs/bugs/BUG-001.md) | Item total shows floating-point noise (`$113.94999999999999`) for some add orders | Medium |
| [BUG-002](docs/bugs/BUG-002.md) | `problem_user` sees the same image for every product | Low |
| [BUG-003](docs/bugs/BUG-003.md) | Add to cart does nothing for 3 of the 6 products (`problem_user`, `error_user`) | High |
| [BUG-004](docs/bugs/BUG-004.md) | Typing in Last Name overwrites First Name (`problem_user`) | High |
| [BUG-005](docs/bugs/BUG-005.md) | Sorting raises an error alert and does not sort (`error_user`) | Medium |
| [BUG-006](docs/bugs/BUG-006.md) | Last Name ignores typing and checkout continues without it (`error_user`) | High |
| [BUG-007](docs/bugs/BUG-007.md) | Finish does not complete the order (`error_user`) | High |
| [BUG-008](docs/bugs/BUG-008.md) | Listing prices differ from the price charged in the cart (`visual_user`) | High |
| [BUG-009](docs/bugs/BUG-009.md) | `POST /auth` with wrong credentials returns 200 instead of 401 | Medium |
| [BUG-010](docs/bugs/BUG-010.md) | `DELETE /booking/{id}` answers 201 Created | Low |
| [BUG-011](docs/bugs/BUG-011.md) | A booking without `firstname` crashes the server (500) | Medium |
| [BUG-012](docs/bugs/BUG-012.md) | Check-out before check-in and a negative price are accepted | Medium |

`tests/meta/` keeps this honest: every xfail must name an existing report and every report must be reproduced by a test. A second check proves that the API tests say "target unreachable" instead of failing obscurely when Restful-Booker is down.

## Design notes

- **Page Objects** live in `pages/`; tests talk only to them.
- **Locators** use the app's `data-test` attributes.
- **No sleeps.** Waiting relies on Playwright's auto-waiting `expect`. SauceDemo is a single-page app, so navigation waits for an element of the next screen, not for the URL.
- **API tests own their data.** Each test creates its own booking and deletes it (the public instance also resets every 10 minutes).
- **Money is compared as text and `Decimal`**, so formatting defects stay visible.

## Layout

```
pages/          Page Objects: login, inventory, cart, checkout
api/            Restful-Booker client and JSON Schemas
tests/ui/       SauceDemo tests
tests/api/      Restful-Booker tests
tests/meta/     consistency checks (bug reports ↔ xfails, unreachable target)
docs/bugs/      one report per defect
config.py       target URLs (overridable with SAUCEDEMO_URL / BOOKER_URL) and the public demo credentials
```
