-- CUSTOMER sample data.
INSERT INTO customer VALUES
  (1, 'Juana', 'Smith', 'juana.smith@example.com', 'Home', '9735555555', 3),
  (2, 'Joseph', 'Cowen', 'joseph.cowen@example.com', NULL, '2015555555', 0),
  (3, 'Anita', 'Boudreaux', 'anita.bourdreaux@example.com', NULL, '8625555555', 1);

-- SILVER_AND_ABOVE sample data.
INSERT INTO silver_and_above VALUES
  (3, '10000');

-- SHIPPING_ADDRESS sample data.
INSERT INTO shipping_address VALUES
  (1, 'Home', 'J. Smith', 'N. First Street.', 149, 'Newark', '07104', 'NJ', 'USA'),
  (1, 'Work', 'ATTN: Juana Smith', 'Washington St.', 12, 'Newark', '07102', 'NJ', 'USA');

-- CREDIT_CARD sample data.
INSERT INTO credit_card VALUES
  ('234567890123', '234', 'Joseph Cowen', 'MasterCard', '07109', '01/2021'),
  ('123456789012', '123', 'Juana Smith', 'Visa', '07104', '02/2021');

-- STORED_CARD sample data.
INSERT INTO stored_card VALUES
  ('123456789012', 1);

-- CART sample data.
INSERT INTO cart VALUES
  (1, 1, 'Home', '123456789012', 'Open', NULL);

-- PRODUCT sample data.
INSERT INTO product VALUES
  (1, 'Laptop', 'Dell Inspiron 15 3567 15.6"', 379.99, 'What you need. For all you do. The Inspiron 15 3567 15.6" laptop computer for all your basic computing needs. Featuring an Intel Core i3-7130U processor, 8GB RAM, and 1TB hard drive.', 10),
  (2, 'Desktop', 'Acer Aspire TC-780-UR1A', 529.99, 'Free your creativity! Even demanding tasks like video editing and compiling photo albums are easy with the Aspire TC-780-UR1A desktop providing multitasking performance and easy expandability. The progressive black chassis with hairline finish offers front-panel media access so you can easily connect to your digital devices.', 10),
  (3, 'Printer', 'Cannon PIXMA TS6020', 49.99, 'Need to print term papers, concert tickets, or fun family photos and have them all look great? The Canon PIXMA TS6020 Wireless Inkjet All-In-One Printer is up to the task. Need a versatile printer that will fit into a tight space? This one fits the bill. Want the convenience of printing from just about any device from just about anywhere? No problem, because the PIXMA TS6020 printer can connect to all your devices through Wi-Fi, AirPrint, Google Cloud Print, USB and even directly from the Cloud. Plus, there`s no question about quality because it uses a five-ink system to print detailed photos and documents, sports fast output speeds, and even prints beautiful borderless photos. For compact, quality printing at home, choose the Canon PIXMA TS6020 Wireless Inkjet All-In-One Printer.', 10),
  (4, 'Printer', 'HP ENVY 7645 e-All-in-One', 59.99, 'HP`s premium home e-all-in-one for printing low-cost lab-quality photo, creative products and laser-quality documents. Advanced mobile printing features make it easy to print from your smartphone, tablet and connected-PC`s at home or on-the-go.', 10);

-- APPEARS_IN sample data.

-- OFFER_PRODUCT sample data.
INSERT INTO offer_product VALUES
  (1, 299.99),
  (2, 399.99),
  (3, 39.99);

-- COMPUTER sample data.
INSERT INTO computer VALUES
  (1, 'Intel Core i3-7130U (2.7 GHz)'),
  (2, 'Intel Core i5-7400 (3.0 GHz)');

-- LAPTOP sample data.
INSERT INTO laptop VALUES
  (1, '40 Wh', 4.96);

-- PRINTER sample data.
INSERT INTO printer VALUES
  (3, 'Inkjet', '4800 x 1200 dpi'),
  (4, 'Inkjet', '4800 x 1200 dpi');
