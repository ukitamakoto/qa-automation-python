-- The deposit flag keeps its meaning: 'true' -> 1, 'false' -> 0.
SELECT l.id, l.depositpaid, b.deposit_paid
FROM legacy_bookings AS l
JOIN bookings AS b ON b.legacy_id = l.id
WHERE b.deposit_paid <> CASE l.depositpaid WHEN 'true' THEN 1 WHEN 'false' THEN 0 END;
