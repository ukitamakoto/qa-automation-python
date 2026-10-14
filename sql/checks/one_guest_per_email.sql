-- One guest per e-mail address, whatever the letter case.
SELECT lower(email) AS email, count(*) AS guests
FROM guests
GROUP BY lower(email)
HAVING count(*) > 1;
