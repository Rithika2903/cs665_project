DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS rentals;
DROP TABLE IF EXISTS payments;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    year INTEGER,
    rate REAL,
    status TEXT
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER,
    customer_id INTEGER,
    start_date TEXT,
    end_date TEXT,
    total_cost REAL,
    status TEXT,
    FOREIGN KEY(car_id) REFERENCES cars(id),
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rental_id INTEGER,
    amount REAL,
    date TEXT,
    FOREIGN KEY(rental_id) REFERENCES rentals(id)
);
