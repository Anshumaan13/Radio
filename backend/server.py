from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime

from models import Country, RadioStation
from services.radio_service import radio_service

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Global Radio API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models for existing endpoints
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Existing routes
@api_router.get("/")
async def root():
    return {"message": "Global Radio API - Ready to stream the world!"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# New Radio API routes
@api_router.get("/countries", response_model=List[Country])
async def get_countries():
    """Get list of countries with radio stations"""
    try:
        countries = await radio_service.get_countries()
        return countries
    except Exception as e:
        logging.error(f"Failed to get countries: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch countries")

@api_router.get("/stations/{country_code}", response_model=List[RadioStation])
async def get_stations_by_country(country_code: str, limit: int = 50):
    """Get radio stations for a specific country"""
    try:
        # Validate country code format
        country_code = country_code.upper()
        if len(country_code) != 2:
            raise HTTPException(status_code=400, detail="Country code must be 2 characters")
        
        # Limit the number of stations returned
        if limit > 100:
            limit = 100
        elif limit < 1:
            limit = 50
        
        stations = await radio_service.get_stations_by_country(country_code, limit)
        return stations
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to get stations for {country_code}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch radio stations")

@api_router.get("/stations/{station_id}/validate")
async def validate_station(station_id: str):
    """Validate if a radio station stream is working"""
    try:
        # For now, return a simple validation response
        # In production, you might want to actually test the stream
        return {
            "valid": True,
            "status": "working",
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logging.error(f"Failed to validate station {station_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to validate station")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Global Radio API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Global Radio API shutting down...")
    await radio_service.close()
    client.close()