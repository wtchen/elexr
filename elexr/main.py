from fastapi import FastAPI, HTTPException, Depends
from .routers import elections, users
from fastapi.security import OAuth2PasswordRequestForm
from .db import database, User

app = FastAPI()

app.include_router(elections.router)
app.include_router(users.router)


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "william" or form_data.password != "password":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": "william", "token_type": "bearer"}
