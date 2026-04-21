from fastapi import FastAPI

from api.app.api.router import router

app = FastAPI(title="Users API")

app.include_router(router)
