-- =========================================================
-- FOOD ORDERING APP
-- Complete MySQL Database
-- =========================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS food_ordering_app;

USE food_ordering_app;


-- =========================================================
-- DROP VIEW AND TABLES
-- =========================================================

DROP VIEW IF EXISTS food_menu;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS foods;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS users;


-- =========================================================
-- USERS TABLE
-- =========================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    phone VARCHAR(15) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    address VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- ADMIN TABLE
-- =========================================================

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    phone VARCHAR(15) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- CATEGORIES TABLE
-- =========================================================

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,

    category_name VARCHAR(100) NOT NULL UNIQUE
);


-- =========================================================
-- FOODS TABLE
-- =========================================================

CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,

    category_id INT NOT NULL,

    food_name VARCHAR(150) NOT NULL,

    description TEXT,

    price DECIMAL(10,2) NOT NULL,

    image VARCHAR(255),

    available BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =========================================================
-- ORDERS TABLE
-- =========================================================

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00,

    gst DECIMAL(10,2) NOT NULL DEFAULT 0.00,

    discount DECIMAL(10,2) NOT NULL DEFAULT 0.00,

    total DECIMAL(10,2) NOT NULL DEFAULT 0.00,

    payment_method VARCHAR(50) NOT NULL,

    status ENUM(
        'Pending',
        'Confirmed',
        'Preparing',
        'Out for Delivery',
        'Delivered',
        'Cancelled'
    ) DEFAULT 'Pending',

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =========================================================
-- ORDER ITEMS TABLE
-- =========================================================

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    food_id INT NOT NULL,

    quantity INT NOT NULL DEFAULT 1,

    price DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (food_id)
        REFERENCES foods(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =========================================================
-- INSERT CATEGORIES
-- =========================================================

INSERT INTO categories (category_name)
VALUES
('Pizza'),
('Burger'),
('Biryani'),
('Chinese'),
('South Indian'),
('Snacks'),
('Desserts'),
('Drinks');


-- =========================================================
-- INSERT FOOD ITEMS
-- =========================================================

INSERT INTO foods
(
    category_id,
    food_name,
    description,
    price,
    image,
    available
)
VALUES

-- Pizza

(1, 'Margherita Pizza',
 'Classic cheese and tomato pizza',
 199.00, 'pizza.png', TRUE),

(1, 'Farmhouse Pizza',
 'Onion, capsicum and tomato pizza',
 299.00, 'pizza.png', TRUE),

(1, 'Paneer Pizza',
 'Pizza topped with paneer and vegetables',
 329.00, 'pizza.png', TRUE),


-- Burger

(2, 'Veg Burger',
 'Crispy vegetable burger',
 99.00, 'burger.png', TRUE),

(2, 'Cheese Burger',
 'Burger with cheese and vegetables',
 149.00, 'burger.png', TRUE),

(2, 'Paneer Burger',
 'Spicy paneer burger',
 179.00, 'burger.png', TRUE),


-- Biryani

(3, 'Veg Biryani',
 'Aromatic vegetable biryani',
 179.00, 'biryani.png', TRUE),

(3, 'Paneer Biryani',
 'Paneer and vegetable biryani',
 229.00, 'biryani.png', TRUE),

(3, 'Chicken Biryani',
 'Traditional chicken biryani',
 279.00, 'biryani.png', TRUE),


-- Chinese

(4, 'Veg Noodles',
 'Chinese style vegetable noodles',
 149.00, 'noodles.png', TRUE),

(4, 'Fried Rice',
 'Chinese style fried rice',
 159.00, 'fried_rice.png', TRUE),

(4, 'Chilli Paneer',
 'Spicy chilli paneer',
 199.00, 'manchurian.png', TRUE),


-- South Indian

(5, 'Masala Dosa',
 'Crispy dosa with potato masala',
 129.00, 'dosa.png', TRUE),

(5, 'Idli Sambar',
 'Soft idli served with sambar',
 99.00, 'dosa.png', TRUE),

(5, 'Paneer Dosa',
 'Dosa stuffed with paneer',
 169.00, 'dosa.png', TRUE),


-- Snacks

(6, 'French Fries',
 'Crispy golden french fries',
 99.00, 'french_fries.png', TRUE),

(6, 'Veg Sandwich',
 'Fresh vegetable sandwich',
 119.00, 'sandwich.png', TRUE),

(6, 'Garlic Bread',
 'Cheesy garlic bread',
 149.00, 'pizza.png', TRUE),


-- Desserts

(7, 'Chocolate Cake',
 'Chocolate cake slice',
 129.00, 'brownie.png', TRUE),

(7, 'Brownie',
 'Chocolate brownie',
 99.00, 'brownie.png', TRUE),

(7, 'Ice Cream',
 'Vanilla ice cream',
 79.00, 'ice_cream.png', TRUE),


-- Drinks

(8, 'Coca Cola',
 'Cold soft drink',
 50.00, 'cold_drink.png', TRUE),

(8, 'Cold Coffee',
 'Chilled creamy coffee',
 119.00, 'coffee.png', TRUE),

(8, 'Fresh Lime Soda',
 'Refreshing lime soda',
 89.00, 'cold_drink.png', TRUE);


-- =========================================================
-- TEST ADMIN
-- =========================================================

INSERT INTO admin
(
    name,
    email,
    phone,
    password
)
VALUES
(
    'Administrator',
    'admin@gmail.com',
    '9999999999',
    'admin123'
);


-- =========================================================
-- TEST CUSTOMER
-- =========================================================

INSERT INTO users
(
    name,
    email,
    phone,
    password,
    address
)
VALUES
(
    'Test Customer',
    'customer@gmail.com',
    '9876543210',
    '123456',
    'Muzaffarnagar, Uttar Pradesh'
);


-- =========================================================
-- FOOD MENU VIEW
-- =========================================================

CREATE VIEW food_menu AS
SELECT
    f.id,
    c.category_name,
    f.food_name,
    f.description,
    f.price,
    f.image,
    f.available
FROM foods f
JOIN categories c
    ON f.category_id = c.id;


-- =========================================================
-- VERIFY DATABASE
-- =========================================================

SELECT * FROM admin;

SELECT * FROM users;

SELECT * FROM categories;

SELECT * FROM foods;

SELECT * FROM orders;

SELECT * FROM order_items;

SELECT * FROM food_menu;
