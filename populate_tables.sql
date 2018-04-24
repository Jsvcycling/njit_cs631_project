-- CUSTOMER sample data.
INSERT INTO customer VALUES
  (1, 'Juana', 'Smith', 'juana.smith@example.com', '862-555-1234', 'R'),
  (2, 'Joseph', 'Cowen', 'joseph.cowen@example.com', '973-555-5678', 'R'),
  (3, 'Anita', 'Boudreaux', 'anita.bourdreaux@example.com', '201-555-9012', 'S');

-- SILVER_AND_ABOVE sample data.
INSERT INTO customer VALUES
  (3, '10000');

-- SHIPPING_ADDRESS sample data.
INSERT INTO shipping_address VALUES
  (1, 'Home', 'J. Smith', 'N. First Street.', 149, 'Newark', 'NJ', 07104, 'USA'),
  (1, 'Work', 'ATTN: Juana Smith', 'Washington St.', 12, 'Newark', 'NJ', 07102, 'USA');

-- CREDIT_CARD sample data.
INSERT INTO credit_card VALUES
  (123456789012, 123, 'Juana Smith', 'Visa', 1587686400);

-- STORED_CARD sample data.
INSERT INTO stored_card VALUES
  (123456789012, 1);
