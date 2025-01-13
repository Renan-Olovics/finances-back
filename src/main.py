from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from src.router import transaction, graphs, auth

load_dotenv()

app = FastAPI()


app.include_router(transaction.router)
app.include_router(auth.router)
app.include_router(graphs.router)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body>
            <h1>API Documentation</h1>
            <ul>
                <li><a href="/docs">Swagger UI</a></li>
                <li><a href="/redoc">ReDoc</a></li>
            </ul>
        </body>
    </html>
    """
