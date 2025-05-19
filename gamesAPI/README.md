# Games API

This is a FastAPI-based API for managing information about video games.

## Features

*   **CRUD Operations:** Create, Read, Update, and Delete game entries.
*   **Search:** Find games by title (partial match), category, platform, or year of creation.
*   **Database:** Uses SQLite for data storage.
*   **Initial Data:** The database is initialized with a few sample games upon first run if the database is empty.
*   **Health Check:** A `/health` endpoint to verify API status.

## API Structure

The API follows a controller-service-repository pattern:

*   `controllers/`: Handles incoming HTTP requests and responses.
*   `services/`: Contains the business logic.
*   `repositories/`: Manages data interaction with the database.
*   `models.py`: Defines the SQLAlchemy database models.
*   `schemas.py`: Defines Pydantic models for data validation and serialization.
*   `database.py`: Sets up the database connection and session management.
*   `main.py`: The main application entry point, initializes FastAPI and includes routers.
*   `requirements.txt`: Lists the Python dependencies.

## Setup and Running

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the API:**
    ```bash
    python main.py
    ```
    The API will be available at `http://localhost:8000`.

4.  **Access API Documentation:**
    Open your browser and go to `http://localhost:8000/docs` for Swagger UI documentation or `http://localhost:8000/redoc` for ReDoc documentation.

## Endpoints

*   `GET /health`: Health check for the API.
*   `POST /games/`: Create a new game.
    *   Request Body: Game details (title, year\_of\_creation, platform, category, summary).
*   `GET /games/`: Get a list of games.
    *   Query Parameters:
        *   `title` (optional): Filter by part of the game title.
        *   `category` (optional): Filter by game category.
        *   `platform` (optional): Filter by game platform.
        *   `year_of_creation` (optional): Filter by year of creation.
        *   `skip` (optional, default 0): Number of records to skip.
        *   `limit` (optional, default 100): Maximum number of records to return.
*   `GET /games/{game_id}`: Get a specific game by its ID.
*   `PUT /games/{game_id}`: Update an existing game by its ID.
    *   Request Body: Game details to update.
*   `DELETE /games/{game_id}`: Delete a game by its ID.

## Initial Data

The `main.py` script includes a function `init_db()` that will populate the `games.db` SQLite database with some sample game data if the database is currently empty. This ensures you have some data to work with when you first run the application.
