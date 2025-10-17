'use client';

import { useState, useEffect } from 'react';
import { WeatherAPI } from '@/lib/api';
import type { City, WeatherRecord, WeatherAnalytics } from '@/types/weather';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import Link from 'next/link';

export default function AnalyticsPage() {
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<City | null>(null);
  const [historicalData, setHistoricalData] = useState<WeatherRecord[]>([]);
  const [analytics, setAnalytics] = useState<WeatherAnalytics | null>(null);
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState(7);

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const data = await WeatherAPI.getAllCities();
      setCities(data);
      if (data.length > 0) {
        handleCitySelect(data[0]);
      }
    } catch (error) {
      console.error('Failed to load cities:', error);
    }
  };

  const handleCitySelect = async (city: City) => {
    setSelectedCity(city);
    setLoading(true);

    try {
      // Load historical data and analytics in parallel
      const [historical, analyticsData] = await Promise.all([
        WeatherAPI.getHistoricalWeather(city.city_id, 100),
        WeatherAPI.getWeatherAnalytics(city.city_id, days),
      ]);

      setHistoricalData(historical);
      setAnalytics(analyticsData);
    } catch (error) {
      console.error('Failed to load analytics:', error);
      setHistoricalData([]);
      setAnalytics(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedCity) {
      handleCitySelect(selectedCity);
    }
  }, [days]);

  // Transform data for charts
  const chartData = historicalData
    .slice()
    .reverse()
    .map((record) => ({
      time: new Date(record.recorded_at).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
      }),
      temperature: record.temperature,
      feels_like: record.feels_like,
      humidity: record.humidity,
      wind_speed: record.wind_speed,
      pressure: record.pressure,
    }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/"
            className="text-blue-600 hover:text-blue-700 mb-4 inline-block"
          >
            ← Back to Dashboard
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Weather Analytics
          </h1>
          <p className="text-gray-600">
            Historical weather data and trends analysis
          </p>
        </div>

        {/* City Selector and Time Range */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-wrap gap-4 items-end">
            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select City
              </label>
              <select
                value={selectedCity?.id || ''}
                onChange={(e) => {
                  const city = cities.find((c) => c.id === parseInt(e.target.value));
                  if (city) handleCitySelect(city);
                }}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {cities.map((city) => (
                  <option key={city.id} value={city.id}>
                    {city.name}, {city.country}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex-1 min-w-[200px]">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Time Period
              </label>
              <select
                value={days}
                onChange={(e) => setDays(parseInt(e.target.value))}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value={1}>Last 24 hours</option>
                <option value={3}>Last 3 days</option>
                <option value={7}>Last 7 days</option>
                <option value={14}>Last 14 days</option>
                <option value={30}>Last 30 days</option>
              </select>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="text-gray-600 mt-4">Loading analytics...</p>
          </div>
        ) : (
          <>
            {/* Analytics Summary */}
            {analytics && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-1">
                    Average Temperature
                  </h3>
                  <p className="text-3xl font-bold text-blue-600">
                    {analytics.avg_temperature.toFixed(1)}°C
                  </p>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-1">
                    Temperature Range
                  </h3>
                  <p className="text-3xl font-bold text-orange-600">
                    {analytics.min_temperature.toFixed(1)}° - {analytics.max_temperature.toFixed(1)}°
                  </p>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-1">
                    Average Humidity
                  </h3>
                  <p className="text-3xl font-bold text-cyan-600">
                    {analytics.avg_humidity.toFixed(0)}%
                  </p>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-sm font-medium text-gray-600 mb-1">
                    Most Common
                  </h3>
                  <p className="text-2xl font-bold text-gray-700">
                    {analytics.most_common_condition}
                  </p>
                </div>
              </div>
            )}

            {/* Temperature Trend Chart */}
            {chartData.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  Temperature Trend
                </h2>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={chartData}>
                    <defs>
                      <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="temperature"
                      stroke="#3b82f6"
                      fillOpacity={1}
                      fill="url(#colorTemp)"
                      name="Temperature (°C)"
                    />
                    <Area
                      type="monotone"
                      dataKey="feels_like"
                      stroke="#f59e0b"
                      fillOpacity={0.3}
                      fill="#f59e0b"
                      name="Feels Like (°C)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Humidity and Wind Chart */}
            {chartData.length > 0 && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">
                    Humidity Levels
                  </h2>
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line
                        type="monotone"
                        dataKey="humidity"
                        stroke="#06b6d4"
                        strokeWidth={2}
                        name="Humidity (%)"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                <div className="bg-white rounded-lg shadow-md p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-4">
                    Wind Speed
                  </h2>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar
                        dataKey="wind_speed"
                        fill="#10b981"
                        name="Wind Speed (m/s)"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Pressure Chart */}
            {chartData.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">
                  Atmospheric Pressure
                </h2>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis domain={['dataMin - 5', 'dataMax + 5']} />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="pressure"
                      stroke="#8b5cf6"
                      strokeWidth={2}
                      name="Pressure (hPa)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* No Data Message */}
            {chartData.length === 0 && !loading && (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <p className="text-gray-600 text-lg mb-4">
                  No historical data available for this city yet.
                </p>
                <p className="text-gray-500">
                  Data will be collected automatically once you start searching for
                  this city, or you can run the data pipeline to collect historical
                  data.
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
