# FastAPI Application

This is a FastAPI application that provides a RESTful API. This project is built with FastAPI and can be easily set up and run locally.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.10+ (It is recommended to use a virtual environment)
- pip (Python package installer)

## Installation

Follow these steps to install and run the application:

### 1. Clone the repository
```bash
git clone https://github.com/luzhnyak/prom-concept-fastapi
cd prom-concept-fastapi
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

### 4. Create a .env file in the project root

Create a `.env` file based on `.env.sample` and update the values as needed.

# 🚀 Run the application
Once the dependencies are installed, you can run the application:
```bash
python app/main.py
```

# Docker

This project can be run inside a Docker container.

## 🚀 Running in Docker

### 1. Clone the repository (if needed)
```bash
git clone https://github.com/luzhnyak/prom-concept-fastapi
cd prom-concept-fastapi
```

### 2. Run the container
```bash
docker-compose up --build
```

### 2. Stopping the container
```bash
docker-compose down
```

# Interactive API Docs

You can access the interactive API documentation by navigating to http://localhost:8000/docs in your web browser.

# Database Migrations with Alembic

This guide explains how to manage database migrations using Alembic in a Python project.

## Creating a Migration

To generate a new migration based on the changes in your models, run:

```bash
alembic revision --autogenerate -m "Your migration message"
```

This will create a new migration script in the `alembic/versions` directory.

## Applying Migrations

To apply all pending migrations and bring your database schema up to date, run:

```bash
alembic upgrade head
```

## Rolling Back a Migration

To revert the last migration, use:

```bash
alembic downgrade -1
```

Or specify a particular revision:

```bash
alembic downgrade <revision_id>
```

## Checking Current Migration Status

To see the current state of the migrations, run:

```bash
alembic current
```

## Viewing Migration History

To check the migration history:

```bash
alembic history
```

