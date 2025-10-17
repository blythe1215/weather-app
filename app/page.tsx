'use client';

import { useState } from 'react';
import Link from 'next/link';
import CitySearch from './dashboard/components/CitySearch';
import { WeatherAPI } from '@/lib/api';
import { formatTemperature, getWeatherIconUrl, formatTime } from '@/lib/utils';
import type { CurrentWeather } from '@/types/weather';

export default function Home() {
  const [weather, setWeather] = useState<CurrentWeather | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCitySelect = async (city: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await WeatherAPI.getCurrentWeather(city);
      setWeather(data);
    } catch (err) {
      setError('Failed to fetch weather data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Weather App
        </h1>
        <p className="text-xl text-gray-600">
          Real-time weather data with AI-powered insights
        </p>
      </div>

      <div className="max-w-2xl mx-auto mb-12">
        <CitySearch onCitySelect={handleCitySelect} />
      </div>

      {loading && (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      )}

      {error && (
        <div className="max-w-2xl mx-auto bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {weather && !loading && (
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-3xl font-bold text-gray-900">
                  {weather.name}, {weather.sys.country}
                </h2>
                <p className="text-gray-600">
                  {new Date(weather.dt * 1000).toLocaleString()}
                </p>
              </div>
              <img
                src={getWeatherIconUrl(weather.weather[0].icon)}
                alt={weather.weather[0].description}
                className="w-24 h-24"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-5xl font-bold text-blue-600">
                  {formatTemperature(weather.main.temp)}
                </div>
                <div className="text-gray-600 mt-2 capitalize">
                  {weather.weather[0].description}
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Feels like:</span>
                  <span className="font-medium">
                    {formatTemperature(weather.main.feels_like)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Min / Max:</span>
                  <span className="font-medium">
                    {formatTemperature(weather.main.temp_min)} /{' '}
                    {formatTemperature(weather.main.temp_max)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Humidity:</span>
                  <span className="font-medium">{weather.main.humidity}%</span>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Wind Speed:</span>
                  <span className="font-medium">{weather.wind.speed} m/s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Pressure:</span>
                  <span className="font-medium">{weather.main.pressure} hPa</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Visibility:</span>
                  <span className="font-medium">
                    {(weather.visibility / 1000).toFixed(1)} km
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-600 pt-6 border-t">
              <div>
                Sunrise: {formatTime(weather.sys.sunrise)}
              </div>
              <div>
                Sunset: {formatTime(weather.sys.sunset)}
              </div>
            </div>
          </div>

          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link
              href={`/analytics?city=${weather.name}&cityId=${weather.id}`}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg text-center font-medium hover:bg-blue-700 transition-colors"
            >
              View Analytics
            </Link>
            <Link
              href={`/insights?city=${weather.name}&cityId=${weather.id}`}
              className="bg-green-600 text-white px-6 py-3 rounded-lg text-center font-medium hover:bg-green-700 transition-colors"
            >
              AI Insights
            </Link>
          </div>
        </div>
      )}

      {!weather && !loading && !error && (
        <div className="text-center py-12 text-gray-600">
          <p>Search for a city to see weather information</p>
        </div>
      )}
    </div>
  );
}
