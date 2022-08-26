from typing import TypedDict

class AddressComponent(TypedDict):
    long_name: str
    short_name: str
    types: list[str]

class LatLong(TypedDict):
    lat: float
    lng: float

class Geometry(TypedDict):
    location: LatLong

class LocationResults(TypedDict):
    address_components: list[AddressComponent]
    formatted_address: str 
    geometry: Geometry
    place_id: str 
    types: list[str]

class LocationResponse(TypedDict):
    results: list[LocationResults]

