import httpx
import logging
from typing import List, Dict, Optional
from cachetools import TTLCache
from ..models import Country, RadioStation, RadioBrowserStation, RadioBrowserCountry

logger = logging.getLogger(__name__)

class RadioBrowserService:
    def __init__(self):
        self.base_url = "https://de1.api.radio-browser.info/json"
        self.client = httpx.AsyncClient(timeout=30.0)
        # Cache for 1 hour (3600 seconds)
        self.cache = TTLCache(maxsize=100, ttl=3600)
        
        # Country flag mapping
        self.country_flags = {
            'US': '🇺🇸', 'GB': '🇬🇧', 'FR': '🇫🇷', 'DE': '🇩🇪', 'JP': '🇯🇵',
            'AU': '🇦🇺', 'CA': '🇨🇦', 'BR': '🇧🇷', 'IN': '🇮🇳', 'IT': '🇮🇹',
            'ES': '🇪🇸', 'RU': '🇷🇺', 'NL': '🇳🇱', 'CH': '🇨🇭', 'SE': '🇸🇪',
            'NO': '🇳🇴', 'DK': '🇩🇰', 'FI': '🇫🇮', 'AT': '🇦🇹', 'BE': '🇧🇪',
            'PL': '🇵🇱', 'PT': '🇵🇹', 'IE': '🇮🇪', 'MX': '🇲🇽', 'AR': '🇦🇷',
            'KR': '🇰🇷', 'CN': '🇨🇳', 'TH': '🇹🇭', 'SG': '🇸🇬', 'MY': '🇲🇾',
            'ID': '🇮🇩', 'PH': '🇵🇭', 'VN': '🇻🇳', 'TW': '🇹🇼', 'HK': '🇭🇰',
            'NZ': '🇳🇿', 'ZA': '🇿🇦', 'EG': '🇪🇬', 'IL': '🇮🇱', 'TR': '🇹🇷',
            'GR': '🇬🇷', 'CZ': '🇨🇿', 'HU': '🇭🇺', 'RO': '🇷🇴', 'BG': '🇧🇬',
            'HR': '🇭🇷', 'SI': '🇸🇮', 'SK': '🇸🇰', 'LT': '🇱🇹', 'LV': '🇱🇻',
            'EE': '🇪🇪', 'IS': '🇮🇸', 'MT': '🇲🇹', 'CY': '🇨🇾', 'LU': '🇱🇺'
        }

    async def get_countries(self) -> List[Country]:
        """Get list of countries with radio stations"""
        cache_key = "countries"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            response = await self.client.get(f"{self.base_url}/countries")
            response.raise_for_status()
            data = response.json()
            
            countries = []
            for item in data:
                try:
                    country_data = RadioBrowserCountry(**item)
                    # Only include countries with reasonable number of stations
                    if country_data.stationcount >= 10:
                        country = Country(
                            code=country_data.iso_3166_1,
                            name=country_data.name,
                            flag=self.country_flags.get(country_data.iso_3166_1, '🌍'),
                            station_count=country_data.stationcount
                        )
                        countries.append(country)
                except Exception as e:
                    logger.warning(f"Skipping invalid country data: {e}")
                    continue
            
            # Sort by station count (descending) and take top 50
            countries.sort(key=lambda x: x.station_count, reverse=True)
            countries = countries[:50]
            
            self.cache[cache_key] = countries
            return countries
            
        except Exception as e:
            logger.error(f"Failed to fetch countries: {e}")
            return self._get_fallback_countries()

    async def get_stations_by_country(self, country_code: str, limit: int = 50) -> List[RadioStation]:
        """Get radio stations for a specific country"""
        cache_key = f"stations_{country_code}_{limit}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            response = await self.client.get(
                f"{self.base_url}/stations/bycountrycodeexact/{country_code}?hidebroken=true&order=clickcount&reverse=true&limit={limit}"
            )
            response.raise_for_status()
            data = response.json()
            
            stations = []
            for item in data:
                try:
                    raw_station = RadioBrowserStation(**item)
                    station = self._transform_station(raw_station)
                    stations.append(station)
                except Exception as e:
                    logger.warning(f"Skipping invalid station data: {e}")
                    continue
            
            self.cache[cache_key] = stations
            return stations
            
        except Exception as e:
            logger.error(f"Failed to fetch stations for {country_code}: {e}")
            return []

    def _transform_station(self, raw: RadioBrowserStation) -> RadioStation:
        """Transform Radio Browser station to our format"""
        # Parse genre from tags
        genre = self._parse_genre(raw.tags)
        
        # Generate frequency (since most APIs don't provide it)
        frequency = self._generate_frequency(raw.name, raw.stationuuid)
        
        # Format listener count
        listeners = self._format_listeners(raw.clickcount)
        
        # Generate description
        description = self._generate_description(raw.name, raw.tags, raw.country)
        
        return RadioStation(
            id=raw.stationuuid,
            name=raw.name,
            frequency=frequency,
            genre=genre,
            url=raw.url,
            listeners=listeners,
            description=description,
            favicon=raw.favicon,
            homepage=raw.homepage,
            country=raw.country,
            countrycode=raw.countrycode,
            language=raw.language,
            bitrate=raw.bitrate,
            codec=raw.codec,
            votes=raw.votes,
            clickcount=raw.clickcount,
            lastcheckok=raw.lastcheckok
        )

    def _parse_genre(self, tags: Optional[str]) -> str:
        """Parse genre from tags"""
        if not tags:
            return "Music"
        
        tags_lower = tags.lower()
        
        # Genre mapping
        genre_map = {
            'news': 'News/Talk',
            'talk': 'News/Talk', 
            'pop': 'Pop',
            'rock': 'Rock',
            'classical': 'Classical',
            'jazz': 'Jazz',
            'country': 'Country',
            'hip hop': 'Hip Hop',
            'electronic': 'Electronic',
            'dance': 'Dance',
            'folk': 'Folk',
            'alternative': 'Alternative',
            'indie': 'Indie',
            'metal': 'Metal',
            'punk': 'Punk',
            'reggae': 'Reggae',
            'blues': 'Blues',
            'oldies': 'Oldies',
            'world': 'World Music',
            'latin': 'Latin',
            'christian': 'Christian',
            'sports': 'Sports',
            'variety': 'Variety'
        }
        
        for key, genre in genre_map.items():
            if key in tags_lower:
                return genre
        
        # If no match, return capitalized first tag
        first_tag = tags.split(',')[0].strip().title()
        return first_tag if first_tag else "Music"

    def _generate_frequency(self, name: str, station_id: str) -> str:
        """Generate a plausible frequency based on station name and ID"""
        # Use hash of station ID to generate consistent frequency
        hash_val = hash(station_id) % 1000
        
        # FM range: 88.1 - 107.9
        fm_freq = 88.1 + (hash_val / 1000) * 19.8
        
        return f"{fm_freq:.1f} FM"

    def _format_listeners(self, clickcount: int) -> str:
        """Format listener count in a readable format"""
        if clickcount >= 1000000:
            return f"{clickcount / 1000000:.1f}M"
        elif clickcount >= 1000:
            return f"{clickcount / 1000:.0f}K"
        else:
            return str(clickcount)

    def _generate_description(self, name: str, tags: Optional[str], country: str) -> str:
        """Generate a description for the station"""
        if not tags:
            return f"Radio station from {country}"
        
        # Clean up tags
        tag_list = [tag.strip().title() for tag in tags.split(',')[:3]]
        tag_str = ", ".join(tag_list)
        
        return f"{tag_str} from {country}"

    def _get_fallback_countries(self) -> List[Country]:
        """Fallback countries if API fails"""
        return [
            Country(code='US', name='United States', flag='🇺🇸', station_count=12000),
            Country(code='GB', name='United Kingdom', flag='🇬🇧', station_count=8000),
            Country(code='DE', name='Germany', flag='🇩🇪', station_count=6000),
            Country(code='FR', name='France', flag='🇫🇷', station_count=5000),
            Country(code='CA', name='Canada', flag='🇨🇦', station_count=4000),
            Country(code='AU', name='Australia', flag='🇦🇺', station_count=3000),
            Country(code='IT', name='Italy', flag='🇮🇹', station_count=2500),
            Country(code='ES', name='Spain', flag='🇪🇸', station_count=2000),
            Country(code='NL', name='Netherlands', flag='🇳🇱', station_count=1800),
            Country(code='BR', name='Brazil', flag='🇧🇷', station_count=1500),
        ]

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Global service instance
radio_service = RadioBrowserService()