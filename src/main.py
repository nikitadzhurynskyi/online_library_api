import uvicorn
from fastapi import FastAPI

from src.auth.router import router as auth_router

app = FastAPI()
app.include_router(router=auth_router)

if __name__ == "__main__":
    uvicorn.run(app, port=3000, reload=True)
