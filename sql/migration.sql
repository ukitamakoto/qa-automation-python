-- Migration under test: legacy_bookings -> guests + bookings.
-- Kept exactly as delivered; the queries in checks/ verify it.
CREATE TABLE guests (
  id        INTEGER PRIMARY KEY,
  firstname TEXT NOT NULL,
  lastname  TEXT NOT NULL,
  email     TEXT NOT NULL UNIQUE
);

CREATE TABLE bookings (
  id               INTEGER PRIMARY KEY,
  legacy_id        INTEGER NOT NULL UNIQUE,
  guest_id         INTEGER NOT NULL REFERENCES guests (id),
  total_cents      INTEGER NOT NULL,
  deposit_paid     INTEGER NOT NULL,
  checkin          TEXT NOT NULL,
  checkout         TEXT NOT NULL,
  additional_needs TEXT
);

INSERT INTO guests (firstname, lastname, email)
SELECT firstname, lastname, lower(email)
FROM legacy_bookings
WHERE true
ORDER BY id
ON CONFLICT (email) DO NOTHING;

INSERT INTO bookings (legacy_id, guest_id, total_cents, deposit_paid, checkin, checkout, additional_needs)
SELECT l.id,
       g.id,
       CAST(CAST(l.totalprice AS REAL) * 100 AS INTEGER),
       CASE l.depositpaid WHEN 'true' THEN 1 ELSE 0 END,
       l.checkin,
       l.checkout,
       l.additionalneeds
FROM legacy_bookings AS l
JOIN guests AS g ON g.email = l.email;
