### BioChatter MeTTa Server

This repo contains a backend API for the BioChatter MeTTa chat web application.

*Supported OS:* **Linux & Mac**

**Follow these steps to run the API:**
1. Install required dependencies (preferably in a virtual environment):
    ```bash
    pip install -r requirements.txt
    ```
2. Add your OpenAI API Key to env:
    ```bash
    export OPENAI_API_KEY=*****
    ```
3. Create the database migrations:
    ```bash
    python manage.py makemigrations
    ```
4. Run the migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the API in a dev server:
    ```bash
    python manage.py runserver
    ```
**You can view the available routes in the [urls.py](https://github.com/iCog-Labs-Dev/biochatter-metta-server/blob/main/api/urls.py) module.**
**You can test the api using the *URL* below:**
```bash
http://127.0.0.1:8000/api/<route>
```