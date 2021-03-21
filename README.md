# Airline Management System

## Steps to start working

1. Create a virtual environment with python=3.6
2. ```pip install -r requirements.txt```
3. If you've done the setup move to 4. Otherwise do the following to create the database.
    Open a python shell while in the repo. Run the following commands.
    ```from airlinemgmt import db, create_app```
    ```app = create_app()```
    ```app.app_context().add()```
    ```db.create_all()```
4. ```python run.py``` (default debug mode)