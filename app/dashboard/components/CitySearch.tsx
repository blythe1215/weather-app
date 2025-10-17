'use client';

import { useState, useEffect } from 'react';
import { WeatherAPI } from '@/lib/api';
import type { City } from '@/types/weather';

interface CitySearchProps {
  onCitySelect: (city: string) => void;
}

export default function CitySearch({ onCitySelect }: CitySearchProps) {
  const [query, setQuery] = useState('');
  const [cities, setCities] = useState<City[]>([]);
  const [allCities, setAllCities] = useState<City[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Load all cities on mount
    WeatherAPI.getAllCities()
      .then((data) => setAllCities(data))
      .catch((error) => console.error('Failed to load cities:', error));
  }, []);

  useEffect(() => {
    if (query.length < 2) {
      setCities([]);
      return;
    }

    const searchCities = async () => {
      setIsLoading(true);
      try {
        const results = await WeatherAPI.searchCities(query);
        setCities(results);
      } catch (error) {
        console.error('Failed to search cities:', error);
      } finally {
        setIsLoading(false);
      }
    };

    const debounce = setTimeout(searchCities, 300);
    return () => clearTimeout(debounce);
  }, [query]);

  const handleCityClick = (city: City) => {
    onCitySelect(city.name);
    setQuery('');
    setCities([]);
  };

  return (
    <div className="relative w-full max-w-md">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for a city..."
          className="w-full px-4 py-3 pr-10 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        {isLoading && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
          </div>
        )}
      </div>

      {cities.length > 0 && (
        <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {cities.map((city) => (
            <button
              key={city.id}
              onClick={() => handleCityClick(city)}
              className="w-full px-4 py-3 text-left hover:bg-gray-100 flex justify-between items-center"
            >
              <span className="font-medium">{city.name}</span>
              <span className="text-sm text-gray-500">{city.country}</span>
            </button>
          ))}
        </div>
      )}

      {query.length === 0 && allCities.length > 0 && (
        <div className="mt-4">
          <p className="text-sm text-gray-600 mb-2">Popular cities:</p>
          <div className="flex flex-wrap gap-2">
            {allCities.slice(0, 5).map((city) => (
              <button
                key={city.id}
                onClick={() => onCitySelect(city.name)}
                className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200 transition-colors"
              >
                {city.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
