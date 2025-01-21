# FastAPI PostgreSQL Demo

This project demonstrates how to use FastAPI with PostgreSQL. It includes a basic FastAPI app that fetches holiday data from an external API and inserts it into a PostgreSQL database. The app also exposes two endpoints to query holiday data:

1. `/` - Returns a list of all holidays.
2. `/holiday/{date}` - Returns holiday information for a specific date.

## Requirements

- Docker
- Python 3.9+
- PostgreSQL (handled via Docker)
- FastAPI
- SQLAlchemy
- Uvicorn

## Setup Instructions

### Clone the Repository

Clone this repository to your local machine:

```
git clone git@github.com:sbstnzcr/holidays.git
cd holidays
```

### Create a `.env` File

Create a `.env` file in the root of the project with the following content:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=db
POSTGRES_HOST=localhost
```

### Spin Up Docker Containers

The project includes a `docker-compose.yml` file to spin up a PostgreSQL container. In the root of the project, run the following command to start the services:

```
docker-compose up
```

This will start PostgreSQL and the necessary volumes for persistent data.

### Run Database Creation Script

Once the PostgreSQL container is up, you can run the database creation script to set up the required table. The script will fetch holiday data and insert it into the database.

Run the following command to execute the script:

```
python create_tables.py
```

This script will:
- Create the `feriados` table in your PostgreSQL database.
- Fetch holiday data for the year 2024 from the external API and insert it into the table.

### Spin Up the FastAPI Application

After setting up the database, start the FastAPI app with the following command:

```
uvicorn app:app --reload
```

The FastAPI app will be accessible at [http://localhost:8000](http://localhost:8000).

### API Endpoints

Once the FastAPI app is running, you can access the interactive Swagger [docs](http://localhost:8000/docs).

You can now access the following endpoints:

- **GET `/`** - Returns a list of all holidays stored in the database.
- **GET `/holiday/{date}`** - Returns the holiday information for a specific date (in `yyyy-mm-dd` format).

Example request for a specific date:
```
curl http://localhost:8000/holiday/2024-12-25
```

### Stopping the Services

Once you're done, you can stop the services by running:

```
docker-compose down
```

## Project Structure

```
├── app.py              # FastAPI app
├── create_tables.py    # Script for setting up the database and inserting holiday data
├── docker-compose.yml  # Docker Compose file for PostgreSQL
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Dependencies

To install Python dependencies, create a virtual environment and install them:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
