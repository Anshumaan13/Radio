from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Country(BaseModel):
    code: str
    name: str
    flag: str
    station_count: int = 0

class RadioStation(BaseModel):
    id: str
    name: str
    frequency: str
    genre: str
    url: str
    listeners: str
    description: str
    favicon: Optional[str] = None
    homepage: Optional[str] = None
    country: str
    countrycode: str
    language: Optional[str] = None
    bitrate: Optional[int] = None
    codec: Optional[str] = None
    votes: int = 0
    clickcount: int = 0
    lastcheckok: int = 0

class RadioBrowserStation(BaseModel):
    """Raw station data from Radio Browser API"""
    stationuuid: str
    name: str
    url: str
    homepage: Optional[str] = None
    favicon: Optional[str] = None
    country: str
    countrycode: str
    state: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[str] = None
    codec: Optional[str] = None
    bitrate: Optional[int] = None
    votes: int = 0
    clickcount: int = 0
    lastcheckok: int = 0

class RadioBrowserCountry(BaseModel):
    """Raw country data from Radio Browser API"""
    name: str
    iso_3166_1: str
    stationcount: int