import uvicorn

from fastapi import FastAPI

from src.api_v1 import router


app = FastAPI(
    title="AviaTicketsVictory"
)


app.include_router(
    router=router,
    prefix="/api_v1"
)


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        reload=True
    )
