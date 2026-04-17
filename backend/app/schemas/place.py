from pydantic import BaseModel


class PlaceResponse(BaseModel):
    name: str
    lat: float
    lng: float
