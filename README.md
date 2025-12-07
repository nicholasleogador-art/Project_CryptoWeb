# 🐍 CrudePy: Flask CRUD Application with MySQL and User Authentication

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange)](https://www.mysql.com/)

A simple Flask application demonstrating basic **CRUD** (Create, Read, Update, Delete) operations on a MySQL database, secured with basic **user authentication** and session management provided by **Flask-Login**.

---

## ✨ Features

* **User Registration (`/signup`):** Create new user accounts.
* **User Login/Logout (`/login`, `/logout`):** Secure session management using Flask-Login.
* **CRUD Operations (`/index`):** View, Insert, Update, and Delete records in the `accs` table.
* **Session Management:** Uses context processors to dynamically display navigation links based on the user's login status.
* **Custom Cipher:** Includes a simple ROT13 encoding function (`enc`) for data demonstration purposes.

---

## ⚠️ Security Warning (CRITICAL)

**DO NOT USE IN PRODUCTION.** The current application code stores user passwords in the database as **plain text** (unhashed). This is a severe security vulnerability.

For any live environment, you **must** implement hashing using a library like **Flask-Bcrypt** or **Werkzeug's security** modules.

---

## 🚀 Setup and Installation

### 1. Database Setup

This application requires a local MySQL server running.

1.  **Create Database:** Create a new MySQL database named `crudeapp`.
2.  **Create the `accs` Table:** Execute the following SQL query in your database tool (e.g., MySQL Workbench, phpMyAdmin):

    ```sql
    CREATE TABLE accs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(100) NOT NULL UNIQUE,
        name VARCHAR(100),
        number VARCHAR(20),
        password VARCHAR(100) NOT NULL
    );
    ```

### 2. Python Environment

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_REPO_URL]
    cd CrudePy
    ```

2.  **Install Dependencies:**
    ```bash
    pip install Flask Flask-MySQLdb Flask-Login
    ```

### 3. Configuration

Open your main application file (`app.py`) and verify that the database connection details match your local environment:

```python
# --- Configuration in app.py ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'      # <-- Check this
app.config['MYSQL_PASSWORD'] = ''      # <-- Update this with your MySQL password
app.config['MYSQL_DB'] = 'crudeapp'
app.secret_key = '1'                   # <-- Update this with a strong, complex key
