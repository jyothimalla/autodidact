# Autodidact Maths Challenge — Frontend (Angular)

This is the Angular frontend for the Maths Challenge app. It talks to the FastAPI backend.

## 1) Prerequisites

- Node.js 18+ (recommended)
- npm
- Angular CLI

Check:
```bash
node -v
npm -v
ng version
```

Install Angular CLI (if missing):
```bash
npm install -g @angular/cli
```

## 2) Install and run

Go to frontend folder:
```bash
cd ~/projects/autodidact/frontend
```

Install packages:
```bash
npm install
```

Run dev server:
```bash
ng serve -o
```

App opens at:
- http://localhost:4200

## 3) Backend API base URL

For local development, backend should be:
- http://127.0.0.1:8000

✅ Make sure your Angular services use `8000` (NOT 4200) for API calls.

Common places where API base URL lives:
- `src/environments/environment.ts`
- `src/app/services/*.ts`
- a config loader service (e.g., `config.service.ts`)

If you see in browser console:
- `Failed to load attempts ... url: http://localhost:8000/progress/1 status: 0`
  it usually means backend is not reachable or CORS blocked.

## 4) Login and registration flow

Typical flow:
1. User registers (username + password)
2. User logs in
3. Frontend stores JWT token (localStorage/sessionStorage)
4. Frontend calls progress endpoints using the token

### How to confirm exact endpoints/fields
Open backend swagger:
- http://127.0.0.1:8000/docs

Search for `auth` and confirm:
- endpoint paths (e.g., `/auth/login`)
- request fields (username/email/password)

## 5) CORS (important)

Backend must allow frontend origin:
- `http://localhost:4200`

If you see a CORS error in browser console, fix backend CORS to include exactly:
- `http://localhost:4200`

(Origins should not include URL paths like `/auth/login`.)

## 6) “Return after break” checklist

1. Start backend: `python -m uvicorn main:app --reload`
2. Confirm swagger loads: `http://127.0.0.1:8000/docs`
3. Start frontend: `ng serve`
4. Open app: `http://localhost:4200`
5. Try register/login
6. If you see errors, check DevTools → Network tab → failing request
