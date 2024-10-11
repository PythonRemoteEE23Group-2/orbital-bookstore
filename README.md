# Orbital Bookstore

Orbital Bookstore is an online bookstore where users can browse, add books to their cart, make purchases, and leave reviews. This application is built using Django, a Python web framework.

![Project Screenshot](./static/images/screenshot.png)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12 or higher
- Django 4.0
- PostgreSQL 14 (or any other database you plan to use)
- Git
- asgiref==3.8.1
- Django==5.1.1
- mysqlclient==2.2.4
-psycopg2-binary==2.9.9
- python-decouple==3.8
- sqlparse==0.5.1
- pip~=24.0
- wheel~=0.43.0
- utils~=1.0.2
- pillow~=10.3.0
- tornado~=6.4
- numpy~=2.1.0
- requests~=2.32.3
- setuptools~=69.5.1
- packaging~=24.1
- pyparsing~=3.1.2
- pytest~=8.2.0

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
By default, the project is set up to work with PostgreSQL. Update the DATABASES setting in the settings.py file according to your database configuration:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database-name',
        'USER': 'your-database-user',
        'PASSWORD': 'your-database-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Apply migrations
Run the following commands to apply the database migrations:
```bash
python manage.py makemigrations
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

## Features

Book Catalog: Users can browse through a collection of books sorted by categories and subcategories.
User Authentication: Users can sign up, log in, and manage their profiles.
Shopping Cart: Users can add books to their cart and proceed with the purchase.
Order History: Users can view their past purchases and order details.
Admin Panel: Admins can manage books, users, and orders through the Django admin interface.
Book Reviews: Registered users can leave reviews and ratings for books.

## Testing

To run the tests for the project, execute the following command:
```bash
python manage.py test
```
This will run all unit tests for the app, ensuring that the functionality works as expected.

## Deployment

For production deployment, ensure you configure the following settings:

Database: Use a production-level database like PostgreSQL or MySQL.
Static Files: Run python manage.py collectstatic to collect static files.
Server: Use a production-ready web server like Gunicorn or uWSGI along with Nginx.

## Credits

This project was developed as part of a team effort.