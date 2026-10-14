-- The migrated total equals the legacy price to the cent.
-- The oracle reads the text price without floating point: '19.99' -> 1999.
SELECT l.id, l.totalprice, b.total_cents
FROM legacy_bookings AS l
JOIN bookings AS b ON b.legacy_id = l.id
WHERE b.total_cents <> CAST(replace(l.totalprice, '.', '') AS INTEGER);
