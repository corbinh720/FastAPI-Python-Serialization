# FastAPI Book Management Mini-Lab

## Project Description
This project uses FastAPI to create a REST API for managing books. A Python command-line client communicates with the server using HTTP requests and JSON serialization.

The application allows users to create, retrieve, update, and delete books. Each book contains an ID, title, author information, publication year, genre, and ratings.

## Technologies Used
- Python
- FastAPI
- Uvicorn
- Requests
- Pydantic
- JSON

## Project Structure

```text
fastapi_lab/
├── server/
│   └── main.py
├── client/
│   └── client.py
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

From the `fastapi_lab` folder:

```bash
cd server
python main.py
```

The server runs at `http://localhost:8000`.

API documentation is available at `http://localhost:8000/docs`.

## Running the Client

Open a second terminal, navigate to the `client` folder, and run:

```bash
python client.py list
```

## Available Commands

```bash
python client.py list
python client.py get 1
python client.py count
python client.py search-genre Fiction
python client.py average-rating 1
python client.py patch 1 --title "Updated Book"
python client.py create "Test Book" "Test Author" "test@example.com" 2026 Fiction --ratings 4,5,3
python client.py update 1 "Updated Book" "Test Author" "test@example.com" 2026 Fiction --ratings 5,4,5
python client.py delete 3
```

## Additional Exercises Completed

**Exercise 1: Search by Genre**

Added an endpoint that searches for books by genre without case sensitivity