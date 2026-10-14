-- Legacy bookings: one flat table, shaped like the Restful-Booker payload.
-- Prices are stored as text with two decimals and the deposit flag as 'true'/'false'.
CREATE TABLE legacy_bookings (
  id              INTEGER PRIMARY KEY,
  firstname       TEXT NOT NULL,
  lastname        TEXT NOT NULL,
  email           TEXT NOT NULL,
  totalprice      TEXT NOT NULL,
  depositpaid     TEXT NOT NULL,
  checkin         TEXT NOT NULL,
  checkout        TEXT NOT NULL,
  additionalneeds TEXT
);

INSERT INTO legacy_bookings VALUES
  (1,  'Ana',     'Souza',    'ana.souza@example.com',     '150.00', 'true',  '2026-11-01', '2026-11-05', 'Breakfast'),
  (2,  'Bruno',   'Lima',     'bruno.lima@example.com',    '19.99',  'false', '2026-11-02', '2026-11-03', NULL),
  (3,  'Carla',   'Mendes',   'carla.mendes@example.com',  '220.50', 'true',  '2026-11-03', '2026-11-07', 'Late check-out'),
  (4,  'Rafael',  'Costa',    'Rafael.Costa@Example.com',  '310.00', 'true',  '2026-11-04', '2026-11-08', 'Parking'),
  (5,  'Ana',     'Souza',    'ana.souza@example.com',     '64.10',  'false', '2026-12-10', '2026-12-11', NULL),
  (6,  'Diego',   'Alves',    'diego.alves@example.com',   '8.20',   'true',  '2026-11-06', '2026-11-07', NULL),
  (7,  'Elisa',   'Ramos',    'ELISA.RAMOS@EXAMPLE.COM',   '95.00',  'false', '2026-11-07', '2026-11-09', 'Crib'),
  (8,  'Felipe',  'Nunes',    'felipe.nunes@example.com',  '120.00', 'true',  '2026-11-12', '2026-11-08', NULL),
  (9,  'Gabriela','Rocha',    'gabriela.rocha@example.com','75.25',  'false', '2026-11-09', '2026-11-10', 'Breakfast'),
  (10, 'Hugo',    'Teixeira', 'hugo.teixeira@example.com', '400.00', 'true',  '2026-11-10', '2026-11-15', NULL),
  (11, 'Bruno',   'Lima',     'bruno.lima@example.com',    '45.00',  'true',  '2026-12-01', '2026-12-02', 'Parking'),
  (12, 'Isabel',  'Martins',  'isabel.martins@example.com','132.40', 'false', '2026-11-20', '2026-11-22', NULL);
