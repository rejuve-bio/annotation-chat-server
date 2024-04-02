### BioChatter MeTTa Server

This repo contains a backend API for the BioChatter MeTTa chat web application.

**Follow these steps to run the API:**
1. Install required dependencies (preferably in a virtual environment):
    ```bash
    pip install -r requirements.txt
    ```
2. Create the database migrations:
    ```bash
    python manage.py makemigrations
    ```
3. Run the migrations:
    ```bash
    python manage.py migrate
    ```
4. Run the API in a dev server:
    ```bash
    python manage.py runserver
    ```
**You can test the api by following this link:**
```bash
http://127.0.0.1:8000/api/<route>
```