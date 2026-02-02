import uvicorn
from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.book.router import router as book_router

app = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=book_router)

if __name__ == "__main__":
    uvicorn.run(app, port=3000, reload=True)
