import environ
import json
from http import client
from pathlib import Path


class MetaSingleton(type):
    """Metaclass to create singleton classes.
    Include 'metaclass=MetaSingleton' keyword to use."""
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def get_nearest_city(lat: float, long: float) -> str:
    """Get the city closest to a given set of coordinates in a radius of 100mi.

    Args:
        lat (float): latitude
        long (float): longitude

    Returns:
        str: Name of the closest city to the given coordinates.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env = environ.Env()
    environ.Env.read_env(str(BASE_DIR / ".env"))

    RAPID_API = env.str("RAPID_API")

    conn = client.HTTPSConnection("wft-geo-db.p.rapidapi.com", timeout=2)
    
    # https://rapidapi.com/blog/how-to-use-geodb-cities-api/
    url = ("/v1/geo/locations/"
           + str(lat)
           + "%2B"
           + str(long)
           + "/nearbyCities?limit=1&radius=100"
    )
    headers = {
        "X-RapidAPI-Key": RAPID_API,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    conn.request("GET", url, headers=headers)
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    try:
        city = data["data"][0]["city"]
    except:
        city = None
        
    return city
