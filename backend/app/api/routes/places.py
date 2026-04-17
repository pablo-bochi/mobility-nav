from fastapi import APIRouter, Query
from app.schemas.place import PlaceResponse
from app.services.nominatim_service import search_places

router = APIRouter(prefix="/places", tags=["places"])


@router.get("/search", response_model=list[PlaceResponse])
def search_places_route(q: str = Query(..., min_length=2)):
    return search_places(q)
