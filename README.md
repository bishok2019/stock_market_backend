# Stock Market Backend

This project is a Django REST API backend for a stock market watchlist application. It provides endpoints for user authentication, stock management, watchlists, and historical price tracking. The API is documented using Swagger and supports JWT authentication.

## Features

- User registration, login, and logout
- JWT-based authentication
- Stock CRUD operations
- Watchlist management for users
- Historical price tracking for stocks
- API documentation via Swagger UI

## Tech Used

- Python 3.13
- Django 5.2.7
- Django REST Framework
- PostgreSQL
- drf-spectacular (API docs)
- SimpleJWT (token authentication)

## Setup Instructions

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd stock_market_backend
```

### 2. Install dependencies 

It’s recommended to use a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or, if using `pyproject.toml`:

```sh
uv sync
```

### 3. Set up PostgreSQL

Install PostgreSQL and create a database and user:

```sh
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```

Inside the psql shell:

```sql
CREATE DATABASE stock_market_db;
CREATE USER admin WITH PASSWORD 'admin123';
GRANT ALL PRIVILEGES ON DATABASE stock_market_db TO admin;
```

### 4. Configure environment variables

Copy `.env_sample` to `.env` and update values as needed:

```sh
cp .env_sample .env
```

### 5. Run migrations

```sh
python manage.py migrate
```

### 6. Create a superuser (optional)

```sh
python manage.py createsuperuser
```

### 7. Start the development server

```sh
python manage.py runserver
```

### 8. Access API Docs

Visit [http://localhost:8000/docs/](http://localhost:8000/docs/) for Swagger UI.