# Autodidact Maths Challenge — Backend (FastAPI)

This backend powers the Maths Challenge learning app (login/register, quiz endpoints, progress, admin panel, paper generation, and answer-sheet upload).

## 1) Prerequisites (Mac)

**System tools (Homebrew):**
```bash
brew update
brew install mysql poppler tesseract
```

Why these?
- **mysql**: your app connects to MySQL on `localhost:3306`
- **poppler**: required by `pdf2image` to convert PDF pages
- **tesseract**: required by `pytesseract` if you OCR answers

## 2) Setup Python environment

Go to backend folder (where `main.py` exists):
```bash
cd ~/projects/autodidact/backend
```

Create and activate a virtualenv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

> Tip: Always start uvicorn like this (so it uses the venv packages):
```bash
python -m uvicorn main:app --reload
```

## 3) Start MySQL

Start MySQL service:
```bash
brew services start mysql
```

Check MySQL is running:
```bash
mysqladmin ping
```

## 4) Create DB + user (if not already created)

Login to MySQL as root:
```bash
mysql -u root -p
```

Create DB:
```sql
CREATE DATABASE IF NOT EXISTS autodidact_db;
```

Create user (only if you haven't already):
```sql
CREATE USER IF NOT EXISTS 'autodidact_user'@'localhost' IDENTIFIED BY 'Root@1234';
GRANT ALL PRIVILEGES ON autodidact_db.* TO 'autodidact_user'@'localhost';
FLUSH PRIVILEGES;
```

Exit:
```sql
exit
```

## 5) Configure DB URL

Your backend prints a line like:
`Connecting to DB: mysql+pymysql://...@localhost:3306/autodidact_db`

If you are using an environment variable, create `.env` in backend root:
```env
DATABASE_URL=mysql+pymysql://autodidact_user:Root%401234@localhost:3306/autodidact_db
```

Notes:
- `%40` is URL-encoding for `@`.
- If your password has special characters, URL-encode them.

## 6) Run the backend

Start server:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open:
- Swagger docs: http://127.0.0.1:8000/docs
- Admin panel link page: http://127.0.0.1:8000/
- Admin UI: http://127.0.0.1:8000/admin

## 7) Login + Registration (how to test)

**Step 1:** open Swagger → http://127.0.0.1:8000/docs

In the search box type: `auth`

You should see endpoints like (names can vary based on your router):
- `POST /auth/register`
- `POST /auth/login`

Use **Try it out** and send JSON.

Typical payloads are one of these patterns:
```json
{
  "username": "jyothi",
  "password": "StrongPassword123"
}
```

or sometimes:
```json
{
  "email": "you@example.com",
  "username": "jyothi",
  "password": "StrongPassword123"
}
```

**How to know the exact fields?**
- Swagger shows the request schema for your project.
- If you get `422 Unprocessable Entity`, it means you missed a required field or field name.

**After login**
- You should receive either a JWT token (common) or a session response.
- If your frontend uses JWT, it usually sends:
  `Authorization: Bearer <token>` on later calls.

## 8) Common endpoints you’ll use while debugging

- `GET /docs` → API list
- `GET /progress/{user_id}` → user attempts/progress (your frontend calls this)
- `POST /upload-paper/` → upload PDF answer sheet

## 9) Upload paper (PDF) — system dependencies

Upload route uses PDF/image tools. If you face errors:
- `pdf2image` missing → `pip install pdf2image`
- poppler missing → `brew install poppler`
- opencv missing → `pip install opencv-python`
- tesseract missing → `brew install tesseract`

## 10) Troubleshooting

### A) Browser shows `status: 0` / “Unknown Error” from Angular
Usually means backend is down or blocked. Confirm:
- http://127.0.0.1:8000/docs opens

### B) MySQL error: Connection refused
Start MySQL:
```bash
brew services start mysql
```

### C) Missing module errors on startup
Install the missing module shown in the last line of the traceback, then restart uvicorn.

## 11) Recommended “return after break” checklist

1. `cd ~/projects/autodidact/backend`
2. `source .venv/bin/activate`
3. `brew services start mysql`
4. `python -m uvicorn main:app --reload`
5. open `http://127.0.0.1:8000/docs`
