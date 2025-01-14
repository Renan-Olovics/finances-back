from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from dotenv import load_dotenv
import time

from src.router import transaction, graphs, auth

load_dotenv()

app = FastAPI()


app.include_router(transaction.router)
app.include_router(auth.router)
app.include_router(graphs.router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


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
