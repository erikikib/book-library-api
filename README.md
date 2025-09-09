# Book Library API (Flask + SQLite)
Small REST API for books: list/create/update/delete.

## Endpoints
GET /books  
POST /books           { "title": "...", "author": "..." }  
PUT /books/<id>       { "title": "...", "author": "...", "read": true }  
DELETE /books/<id>

## Run
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
