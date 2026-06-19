from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routers.auth import router as auth_router


app = FastAPI(
    lifespan=lifespan
)
app.include_router(auth_router)

if "__main__" == __name__:
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=54321)