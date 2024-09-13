# Flask Application Setup with Docker Compose

This Flask application demonstrates a simple user registration and login process using JWT for authentication. The application uses SQLAlchemy as the ORM and PostgreSQL as the database, managed with Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Setting Up and Running the Application

Configure the Environment
Create a .env file in the project root directory and add the necessary environment variables:

FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@db:5432/mydatabase
JWT_SECRET_KEY=your_jwt_secret_key

## Build and run with Docker Compose
To build and run the application using Docker Compose, execute:
```bash
docker-compose up --build
```
This command builds the Docker image for the Flask application and starts all services defined in the docker-compose.yml file.

## Using the API
Register a New User
To register a new user, send a POST request to /register with a JSON body containing the username, password, and email:

** POST: /register

** POST: /login


Customer API
** GET: /customers -> Returns all customers, with ability to filter by name and state via query params: `?name=`, `?state=`

** POST: /customers -> Create Customer. Expected params:
`name: string, state: string, phone: int`

** GET: 
