Simple task tracker app

Swagger: http://127.0.0.1:8000/docs

Run project in Git Bash (the system must have python 3.12): 
   ```shell
    pip install poetry
    poetry config virtualenvs.in-project true
    poetry lock && poetry install --no-root
    source .venv/Scripts/activate
    alembic upgrade head && fastapi dev project/app/main.py
   ```

After starting the server, a database will be created with the necessary tables 
and data to test the application: two users with different roles and one task.


Run after changes in db models: 
   ```shell
    alembic revision --autogenerate -m "Change text"
   ```

Ruff:
   ```shell
    ruff check --fix && ruff format
   ```

Create initial user: 
   ```shell
    python -m project.manage -f add_user
   ```

Request examples:
 - Obtain token:
   ```shell
    curl --location 'http://127.0.0.1:8000/token' \
    --form 'username="Performer"' \
    --form 'password="some-password"'
   ```
 - Create task:
    ```shell
    curl --location 'http://127.0.0.1:8000/tasks/' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Bearer <token>' \
   --data '{
      "title": "Some task",
      "description": "Some description",
      "priority": "high",
      "performers": [2]
   }'
   ```
 - Update task status:
     ```shell
      curl --location 'http://127.0.0.1:8000/tasks/<task_id>/' \
       --header 'Content-Type: application/json' \
       --header 'Authorization: Bearer <token>' \
       --data '{"status": "in_progress"}'
   ```
