# Vendor Management System with Performance Metrics

## Introduction

This is a Django-based Vendor Management System that allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics. The system uses Django REST Framework to provide a RESTful API for interacting with the data.

## Features

- **Vendor Profile Management**
  - Create, read, update, and delete vendor profiles.
  - Track essential vendor information including name, contact details, address, and a unique vendor code.

- **Purchase Order Tracking**
  - Create, read, update, and delete purchase orders.
  - Track details such as PO number, vendor reference, order date, items, quantity, and status.

- **Vendor Performance Evaluation**
  - Calculate and retrieve performance metrics such as on-time delivery rate, quality rating average, average response time, and fulfillment rate.

## Technologies Used

- Django
- Django REST Framework
- Django Signals
- JWT for authentication

## Getting Started

### Prerequisites

- Python 3.8+
- Django 3.2+
- pip

### Installation

1. **Clone the repository**

    ```bash
    git clone <repository_url>
    cd vendor-management-system
    ```

2. **Create and activate a virtual environment**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser (optional, for admin interface)**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**

    ```bash
    python manage.py runserver
    ```

### Configuration

Ensure you have the following settings in your `vendor_management/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'vendors',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

APPEND_SLASH = True
