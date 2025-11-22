----------------------------------------------------
-- USERS (10 ROWS) – all use password: admin234
----------------------------------------------------
INSERT INTO users (name, email, password, role) VALUES
('Admin User', 'admin@example.com', 'admin234', 'admin'),
('John Snow', 'john.snow@example.com', 'admin234', 'staff'),
('Emma Watson', 'emma.watson@example.com', 'admin234', 'staff'),
('Liam Brown', 'liam.brown@example.com', 'admin234', 'staff'),
('Sophia Green', 'sophia.green@example.com', 'admin234', 'staff'),
('Oliver King', 'oliver.king@example.com', 'admin234', 'staff'),
('Ava Patel', 'ava.patel@example.com', 'admin234', 'staff'),
('Noah Wilson', 'noah.wilson@example.com', 'admin234', 'staff'),
('Mia Lopez', 'mia.lopez@example.com', 'admin234', 'staff'),
('William Lee', 'william.lee@example.com', 'admin234', 'staff');

----------------------------------------------------
-- CARS (10 ROWS)
----------------------------------------------------
INSERT INTO cars (brand, model, year, rate, status) VALUES
('Toyota', 'Camry', 2020, 50, 'Available'),
('Honda', 'Civic', 2019, 45, 'Rented'),
('Ford', 'Mustang', 2021, 120, 'Available'),
('Tesla', 'Model 3', 2022, 150, 'Available'),
('BMW', 'X5', 2018, 110, 'Rented'),
('Audi', 'A4', 2020, 95, 'Available'),
('Kia', 'Seltos', 2021, 60, 'Available'),
('Hyundai', 'Elantra', 2019, 40, 'Rented'),
('Mercedes', 'C-Class', 2022, 140, 'Available'),
('Nissan', 'Altima', 2017, 35, 'Available');

----------------------------------------------------
-- CUSTOMERS (10 ROWS)
----------------------------------------------------
INSERT INTO customers (name, email, phone) VALUES
('John Doe', 'john@example.com', '9876543210'),
('Rithika', 'rithika@example.com', '5551112222'),
('Michael Smith', 'michael@example.com', '7778889999'),
('Emma Johnson', 'emmaj@example.com', '9993331111'),
('David White', 'davidw@example.com', '8884442222'),
('Sophia Brown', 'sophiab@example.com', '6667778888'),
('Daniel Miller', 'danielm@example.com', '4445556666'),
('Olivia Davis', 'oliviad@example.com', '2223334444'),
('Ava Taylor', 'avat@example.com', '1112223333'),
('Chris Wilson', 'chrisw@example.com', '3334445555');

----------------------------------------------------
-- RENTALS (10 ROWS)
----------------------------------------------------
INSERT INTO rentals (car_id, customer_id, start_date, end_date, total_cost, status) VALUES
(1, 1, '2025-01-01', '2025-01-05', 250, 'Completed'),
(2, 2, '2025-01-03', '2025-01-04', 45, 'Completed'),
(3, 3, '2025-02-10', '2025-02-12', 240, 'Completed'),
(4, 4, '2025-02-15', '2025-02-20', 750, 'Active'),
(5, 5, '2025-03-01', '2025-03-05', 440, 'Completed'),
(6, 6, '2025-03-10', '2025-03-15', 475, 'Active'),
(7, 7, '2025-04-01', '2025-04-03', 120, 'Completed'),
(8, 8, '2025-04-05', '2025-04-07', 80, 'Active'),
(9, 9, '2025-04-10', '2025-04-14', 560, 'Completed'),
(10, 10, '2025-04-15', '2025-04-17', 70, 'Active');

----------------------------------------------------
-- PAYMENTS (10 ROWS)
----------------------------------------------------
INSERT INTO payments (rental_id, amount, date) VALUES
(1, 250, '2025-01-05'),
(2, 45, '2025-01-04'),
(3, 240, '2025-02-12'),
(4, 300, '2025-02-17'),
(5, 440, '2025-03-05'),
(6, 250, '2025-03-12'),
(7, 120, '2025-04-03'),
(8, 80, '2025-04-06'),
(9, 560, '2025-04-14'),
(10, 70, '2025-04-17');
-- Seed file verified by Rithika
