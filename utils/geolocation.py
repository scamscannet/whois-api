import os

from geopy.geocoders import HereV7
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Location(BaseModel):
    unformatted: str = None
    country: str = None
    address: str = None
    longitude: str = None
    latitude: str = None


geolocator = HereV7(os.getenv("HERE_API_KEY"))


def get_location(address: str) -> Location | None:
    location = geolocator.geocode(address)
    if not location:
        return None
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
