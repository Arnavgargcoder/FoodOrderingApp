# Food Ordering App

A desktop-based Food Ordering Application developed using Python,
Tkinter and MySQL.

## Technologies Used

- Python
- Tkinter
- MySQL
- MySQL Connector
- Pillow

## Features

### Customer

- Customer Registration
- Customer Login
- Browse Food Menu
- Food Categories
- Search Food
- Add Food to Cart
- Update Cart Quantity
- Remove Food from Cart
- Checkout
- GST Calculation
- Discount
- Payment Method Selection
- Place Order
- View Order History
- Track Order Status

### Admin

- Admin Login
- Dashboard
- Manage Categories
- Add Food
- Update Food
- Delete Food
- Enable/Disable Food
- View Customers
- View Orders
- Update Order Status
- View Sales Information

## Project Structure

FoodOrderingApp/
│
├── main.py
├── database.py
├── config.py
├── requirements.txt
├── README.md
│
├── customer/
│ ├── **init**.py
│ ├── login.py
│ ├── signup.py
│ ├── home.py
│ ├── menu.py
│ ├── cart.py
│ ├── checkout.py
│ └── orders.py
│
├── admin/
│ ├── **init**.py
│ ├── admin_login.py
│ ├── dashboard.py
│ ├── manage_food.py
│ ├── manage_categories.py
│ ├── manage_orders.py
│ └── customers.py
│
├── assets/
│ ├── logo.png
│ ├── food/
│ └── icons/
│
└── sql/
└── food_ordering_app.sql

## Database

Database Name:

food_ordering_app

Tables:

1. users
2. categories
3. foods
4. orders
5. order_items

## Installation

### Step 1: Install Python

Install Python 3.x.

Check Python version:

python --version

### Step 2: Install Required Packages

Open terminal in the project folder and run:

pip install -r requirements.txt

### Step 3: Setup MySQL

Open MySQL Workbench.

Open:

sql/food_ordering_app.sql

Run the complete SQL script.

This will create:

food_ordering_app

and all required tables.

### Step 4: Configure MySQL

Open:

config.py

Set your MySQL username and password.

Example:

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "food_ordering_app"

### Step 5: Run the Application

Run:

python main.py

## Database Connection

The application uses:

mysql-connector-python

to connect Python with MySQL.

## Food Images

Place food images inside:

assets/food/

Example:

assets/food/margherita.jpg
assets/food/farmhouse.jpg
assets/food/veg_burger.jpg
assets/food/veg_biryani.jpg

The image filename should match the value stored in the
foods.image column.

## Logo

Place the application logo at:

assets/logo.png

## GST

The default GST rate is:

18%

This can be changed in:

config.py

Example:

GST_RATE = 18

## Running the Project

Use:

python main.py

## Author

Food Ordering App Project

## Version

1.0.0
