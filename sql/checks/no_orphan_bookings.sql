-- Every booking points to an existing guest.
-- SQLite only enforces foreign keys when asked to, so the rule is checked here.
SELECT b.id, b.guest_id
FROM bookings AS b
LEFT JOIN guests AS g ON g.id = b.guest_id
WHERE g.id IS NULL;
