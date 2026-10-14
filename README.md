# qa-automation-python

[![tests](https://github.com/ukitamakoto/qa-automation-python/actions/workflows/tests.yml/badge.svg)](https://github.com/ukitamakoto/qa-automation-python/actions/workflows/tests.yml)

**[View the latest test report →](https://ukitamakoto.github.io/qa-automation-python/)**

UI, API and data test automation, written to be read: Page Objects, data-driven tests, JSON Schema validation, SQL data checks, a Postman collection, and a bug report for every defect found.
41 pytest tests (23 UI tests run in Chromium and Firefox, 12 API tests, 6 SQL checks) plus a 9-request Postman collection with 17 assertions.

| Layer | Target | Tools |
|---|---|---|
| UI | [SauceDemo](https://www.saucedemo.com), a demo shop by Sauce Labs | Playwright for Python, pytest |
| API | [Restful-Booker](https://restful-booker.herokuapp.com), a hotel-booking API made for test practice | requests, jsonschema, pytest |
| API (Postman) | The same API: auth and booking CRUD as a chained collection | Postman, Newman |
| Data (SQL) | A legacy-to-normalized booking migration ([`sql/`](sql/)) | SQL on SQLite (Python stdlib), pytest |
| CI | GitHub Actions: lint, API + SQL job, Newman job, UI job on Chromium and Firefox, HTML reports published to GitHub Pages | ruff, pytest-html, newman-reporter-htmlextra |

## Run it

```bash
uv sync
uv run playwright install chromium
uv run pytest                      # add --browser firefox to switch browsers
npx -p newman@6.2.1 newman run postman/restful-booker.postman_collection.json
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
| `postman/` collection (9 requests) | Token, refused login, create (schema), read, update without and with a token, partial update, delete, 404 after delete | Chained requests, collection variables, JSON Schema |
| `sql/test_migration.py` (×6) | After the migration: no booking lost, totals kept to the cent, valid stay dates, no orphan rows, one guest per e-mail, deposit flag kept | Data integrity, reconciliation, oracle without floating point |

### SQL checks

[`sql/legacy.sql`](sql/legacy.sql) holds a flat legacy table, and [`sql/migration.sql`](sql/migration.sql) moves it into `guests` and `bookings`, as delivered. Each file in [`sql/checks/`](sql/checks/) is a plain query that returns the rows breaking one rule, so an empty result means the rule holds. The test runs every check against an in-memory database, so no server is needed.

## Bugs found

Each defect is reproduced by a test marked `xfail(strict=True)`. The suite stays green while the bug exists, and it fails loudly the day the bug is fixed, so the report can be closed. The Postman collection does the same for BUG-009 and BUG-010 with tests named *known defect*.

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
| [BUG-013](docs/bugs/BUG-013.md) | The migration drops bookings whose legacy e-mail has capitals (2 of 12) | High |
| [BUG-014](docs/bugs/BUG-014.md) | The migration loses a cent on some prices (`19.99` → `1998`) | High |
| [BUG-015](docs/bugs/BUG-015.md) | Impossible stays are migrated without being flagged | Medium |

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
tests/sql/      runs the SQL checks against the migration
postman/        Postman collection for Restful-Booker (run in CI with Newman)
sql/            legacy table, migration under test, one query per data rule
tests/meta/     consistency checks (bug reports ↔ xfails, unreachable target)
docs/bugs/      one report per defect
config.py       target URLs (overridable with SAUCEDEMO_URL / BOOKER_URL) and the public demo credentials
```
