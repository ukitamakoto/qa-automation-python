-- Every legacy booking has a migrated row.
SELECT l.id, l.email
FROM legacy_bookings AS l
LEFT JOIN bookings AS b ON b.legacy_id = l.id
WHERE b.id IS NULL;
