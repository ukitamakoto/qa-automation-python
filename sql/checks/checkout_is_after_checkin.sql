-- No stay ends on or before the day it starts.
SELECT id, legacy_id, checkin, checkout
FROM bookings
WHERE checkout <= checkin;
