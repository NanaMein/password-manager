from fastapi import FastAPI
from app.core.lifespan import lifespan


app = FastAPI(
    lifespan=lifespan
)

if "__main__" == __name__:
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=54321)