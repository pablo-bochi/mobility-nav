from fastapi import FastAPI
from app.api.routes.places import router as places_router

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(places_router)
