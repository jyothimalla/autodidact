from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-strong-secret-key")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "letmein"

@app.get("/", response_class=HTMLResponse)
async def login_page():
    return """
    <html>
    <head>
        <title>Admin Login</title>
        <style>
            body { font-family: Arial; background: #f4f4f4; display: flex; justify-content: center; align-items: center; height: 100vh; }
            form { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            input { display: block; width: 100%; margin-bottom: 15px; padding: 10px; }
            button { padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #135ba1; }
        </style>
    </head>
    <body>
        <form method="post" action="/admin-login">
            <h2>🔐 Admin Login</h2>
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """

@app.post("/admin-login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["admin"] = True
        return RedirectResponse(url="/admin", status_code=302)
    return HTMLResponse("<h3>Invalid credentials</h3><a href='/'>Try again</a>", status_code=401)
