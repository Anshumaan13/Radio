import { useState, useEffect } from 'react';
import { radioApi, RadioAPIError } from '../services/radioApi';

export const useCountries = () => {
  const [countries, setCountries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await radioApi.getCountries();
        setCountries(data);
      } catch (err) {
        setError(err.message || 'Failed to load countries');
        console.error('Error fetching countries:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCountries();
  }, []);

  return { countries, loading, error, refetch: () => setLoading(true) };
};

export const useStations = (countryCode) => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!countryCode) {
      setStations([]);
      setLoading(false);
      setError(null);
      return;
    }

    const fetchStations = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await radioApi.getStationsByCountry(countryCode);
        setStations(data);
      } catch (err) {
        setError(err.message || 'Failed to load radio stations');
        console.error('Error fetching stations:', err);
        setStations([]);
      } finally {
        setLoading(false);
      }
    };

    fetchStations();
  }, [countryCode]);

  return { stations, loading, error };
};