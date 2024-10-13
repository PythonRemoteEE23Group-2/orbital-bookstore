# Orbital Bookstore

Orbital Bookstore is an online bookstore where users can browse, add books to their cart, make purchases, and leave reviews. This application is built using Django, a Python web framework.

## Features

Book Catalog: Users can browse through a collection of books sorted by categories and subcategories.
User Authentication: Users can sign up, log in, and manage their profiles.
Shopping Cart: Users can add books to their cart and proceed with the purchase.
Order History: Users can view their past purchases and order details.
Admin Panel: Admins can manage books, users, and orders through the Django admin interface.
Book Reviews: Registered users can leave reviews and ratings for books.

![homepage.png](static/images/homepage.png)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12 or higher
- DDjango 5.1 or higher
- PostgreSQL 14 (or any other database you plan to use)
- Git

## Installation

Follow the steps below to set up and run the project on your local machine.

### 1. Clone the repository

First, clone the project from the repository:

```bash
git clone https://github.com/your-username/orbital-bookstore.git
cd orbital-bookstore
```

### 2.Set up a virtual environment
Set up a virtual environment to install all the necessary dependencies:

#### On MacOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install dependencies
Install all required packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Configure the database

Instead of hardcoding database credentials in the `settings.py` file, we will use environment variables for better security and flexibility.

#### Step 1: Create a `.env` file
In the root directory of the project, create a `.env` file with the following content:

```
DATABASE_NAME=your-database-name
DATABASE_USER=your-database-user
DATABASE_PASSWORD=your-database-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

Replace the values with your actual database details.

#### Step 2: Configure `settings.py`
Update your `settings.py` file to read from the `.env` file. Install the `python-dotenv` package by adding it to your `requirements.txt` or by running:

```bash
pip install python-dotenv
```

Then, modify the `settings.py` file to load environment variables:

```python
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}
```

By using the `.env` file, you ensure that sensitive information like database credentials is not hardcoded in your codebase, improving security and making it easier to manage configurations in different environments.

### 5. Apply migrations
Run the following command to apply the database migrations:
```bash
python manage.py migrate
```
### 6. Create a superuser
To access the Django admin panel, you need to create a superuser account:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin credentials.

### 7. Start the development server
You can now run the development server using the following command:
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to see the website.

### 8. Testing Setup

Before running the tests, ensure the necessary testing libraries are installed.

#### Install testing packages:

Run the following command to install the required packages for running tests:

```bash
pip install pytest pytest-django python-dotenv
```

### Pytest Configuration

To configure pytest for your Django project, create a `pytest.ini` file in the root directory with the following content:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = your_project_name.settings
python_files = tests.py test_*.py *_tests.py
```

Replace `your_project_name` with the name of your Django project.

This ensures pytest can properly locate your Django settings and tests.

### Running tests:

You can run your tests using the following command:

```bash
pytest
```
This ensures all the tests in your project will be executed.

### 9. Credits

This project was developed as part of a team effort: Merlyn Mey & Tarmo Kõuhkna

