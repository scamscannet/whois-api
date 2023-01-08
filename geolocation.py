import os

from geopy.geocoders import HereV7
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Location(BaseModel):
    unformatted: str
    country: str = ""
    address: str
    longitude: str
    latitude: str


geolocator = HereV7(os.getenv("HERE_API_KEY"))


def get_location(address: str) -> Location:
    location = geolocator.geocode(address)
    loc_obj = Location(
        unformatted=address,
        address=location.address,
        longitude=location.longitude,
        latitude=location.latitude,

    )
    try:
        loc_obj.country = location.raw["address"]["countryCode"]
    except:
        pass

    return loc_obj
