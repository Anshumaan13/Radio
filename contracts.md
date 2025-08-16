# Global Radio Stations - API Contracts & Integration Plan

## Overview
Replace mock data with real radio stations using Radio Browser API (free public API).

## Frontend Mock Data to Replace
Located in `/app/frontend/src/mock.js`:
- `mockCountries` - List of countries with codes and flags
- `mockRadioStations` - Radio stations organized by country code

## API Integration Plan

### External API: Radio Browser API
- **Base URL**: `https://de1.api.radio-browser.info/json`  
- **No API key required** - Free public service
- **Rate limit**: Reasonable usage (1000 requests/day typical)

### Backend API Endpoints to Create

#### 1. Get Countries with Radio Stations
```
GET /api/countries
Response: [
  {
    "code": "US",
    "name": "United States", 
    "flag": "🇺🇸",
    "station_count": 12453
  }
]
```

#### 2. Get Radio Stations by Country
```
GET /api/stations/{country_code}
Response: [
  {
    "id": "station-uuid",
    "name": "NPR News",
    "url": "https://npr-ice.streamguys1.com/live.mp3",
    "homepage": "https://www.npr.org",
    "favicon": "https://media.npr.org/favicon.ico",
    "country": "United States",
    "countrycode": "US",
    "state": "Washington DC",
    "language": "english",
    "tags": "news,talk,public radio",
    "codec": "MP3",
    "bitrate": 128,
    "votes": 3041,
    "clickcount": 51234,
    "lastcheckok": 1
  }
]
```

#### 3. Stream Validation Endpoint
```
GET /api/stations/{station_id}/validate
Response: {
  "valid": true,
  "status": "working",
  "last_checked": "2024-01-15T10:30:00Z"
}
```

## Data Transformation

### Radio Browser API → Frontend Format
Transform API response to match current frontend interface:
```javascript
// Radio Browser API response
{
  "stationuuid": "abc-123",
  "name": "BBC Radio 1",
  "url": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
  "homepage": "https://www.bbc.co.uk/radio1",
  "favicon": "https://...",
  "country": "United Kingdom",
  "countrycode": "GB", 
  "state": "London",
  "language": "english",
  "tags": "pop,chart,music",
  "codec": "MP3",
  "bitrate": 128,
  "votes": 1041,
  "clickcount": 25134
}

// Transform to Frontend Format
{
  "id": "abc-123",
  "name": "BBC Radio 1",
  "frequency": "97.7 FM", // Generate or use generic
  "genre": "Pop/Chart", // Parse from tags
  "url": "http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
  "listeners": "25.1K", // Format clickcount
  "description": "UK's most popular music station", // Generate from name/tags
  "favicon": "https://...",
  "homepage": "https://www.bbc.co.uk/radio1"
}
```

## Backend Implementation Steps

1. **Install HTTP client** - Add `httpx` to requirements.txt
2. **Create models** - Pydantic models for countries and stations  
3. **Create services** - Radio Browser API client service
4. **Create endpoints** - FastAPI routes with caching
5. **Add caching** - Cache API responses (1 hour) to reduce external calls
6. **Error handling** - Handle API failures gracefully

## Frontend Integration Changes

### Files to Update
1. **Remove mock.js** - Delete mock data file
2. **Update App.js** - Replace mock imports with API calls
3. **Add API service** - Create `/frontend/src/services/radioApi.js`
4. **Add loading states** - Show loading while fetching data
5. **Error handling** - Display errors when API fails

### API Service Implementation
```javascript
// /frontend/src/services/radioApi.js
const API_BASE = process.env.REACT_APP_BACKEND_URL + '/api';

export const radioApi = {
  getCountries: () => fetch(`${API_BASE}/countries`).then(r => r.json()),
  getStationsByCountry: (countryCode) => 
    fetch(`${API_BASE}/stations/${countryCode}`).then(r => r.json())
};
```

## Testing Strategy

1. **Backend Testing** - Test API endpoints with curl
2. **Frontend Testing** - Verify data loading and display
3. **Integration Testing** - Test full flow: country selection → stations → audio play
4. **Error Testing** - Test network failures and API timeouts

## Performance Considerations

- **Caching**: Cache API responses server-side
- **Pagination**: Limit stations per country (max 50)
- **Loading**: Show skeleton loaders while fetching
- **Debouncing**: Debounce country selection to avoid excessive API calls

## Fallback Strategy

If Radio Browser API is unavailable:
- Return cached data if available
- Show error message with retry option
- Keep mock data as absolute fallback (optional)