const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

class RadioAPIError extends Error {
  constructor(message, status) {
    super(message);
    this.name = 'RadioAPIError';
    this.status = status;
  }
}

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorText = await response.text();
    throw new RadioAPIError(`HTTP ${response.status}: ${errorText}`, response.status);
  }
  return response.json();
};

export const radioApi = {
  async getCountries() {
    try {
      const response = await fetch(`${API_BASE}/countries`);
      return await handleResponse(response);
    } catch (error) {
      console.error('Failed to fetch countries:', error);
      throw error;
    }
  },

  async getStationsByCountry(countryCode, limit = 50) {
    try {
      const response = await fetch(`${API_BASE}/stations/${countryCode}?limit=${limit}`);
      return await handleResponse(response);
    } catch (error) {
      console.error(`Failed to fetch stations for ${countryCode}:`, error);
      throw error;
    }
  },

  async validateStation(stationId) {
    try {
      const response = await fetch(`${API_BASE}/stations/${stationId}/validate`);
      return await handleResponse(response);
    } catch (error) {
      console.error(`Failed to validate station ${stationId}:`, error);
      throw error;
    }
  }
};

export { RadioAPIError };