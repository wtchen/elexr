from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import elections

app = FastAPI()

app.include_router(elections.router)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
        <html>
            <head>
                <title>Elexr</title>
            </head>
            <body>
                <h1>Elexr</h1>
            </body>
        </html>
        """