'use client';

import { useState, useEffect } from 'react';
import { WeatherAPI } from '@/lib/api';
import type { City, InsightResponse } from '@/types/weather';
import Link from 'next/link';

export default function InsightsPage() {
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<City | null>(null);
  const [query, setQuery] = useState('');
  const [insights, setInsights] = useState<InsightResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'custom' | 'summary' | 'clothing'>('summary');

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const data = await WeatherAPI.getAllCities();
      setCities(data);
      if (data.length > 0) {
        setSelectedCity(data[0]);
      }
    } catch (error) {
      console.error('Failed to load cities:', error);
    }
  };

  const handleCustomQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCity || !query.trim()) return;

    setLoading(true);
    try {
      const insight = await WeatherAPI.getAIInsight(
        selectedCity.city_id,
        selectedCity.name,
        query
      );
      setInsights([insight, ...insights]);
      setQuery('');
    } catch (error) {
      console.error('Failed to get insight:', error);
      alert('Failed to get AI insight. Make sure you have configured your OpenAI API key.');
    } finally {
      setLoading(false);
    }
  };

  const handleDailySummary = async () => {
    if (!selectedCity) return;

    setLoading(true);
    try {
      const insight = await WeatherAPI.getDailySummary(
        selectedCity.city_id,
        selectedCity.name
      );
      setInsights([insight, ...insights]);
    } catch (error) {
      console.error('Failed to get summary:', error);
      alert('Failed to get daily summary. Make sure you have configured your OpenAI API key.');
    } finally {
      setLoading(false);
    }
  };

  const handleClothingRecommendation = async () => {
    if (!selectedCity) return;

    setLoading(true);
    try {
      const insight = await WeatherAPI.getClothingRecommendation(
        selectedCity.city_id,
        selectedCity.name
      );
      setInsights([insight, ...insights]);
    } catch (error) {
      console.error('Failed to get clothing recommendation:', error);
      alert('Failed to get clothing recommendation. Make sure you have configured your OpenAI API key.');
    } finally {
      setLoading(false);
    }
  };

  const suggestedQueries = [
    'What will the weather be like this weekend?',
    'Is it a good day for outdoor activities?',
    'Should I bring an umbrella today?',
    'How does today compare to yesterday?',
    'What are the weather trends this week?',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-purple-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/"
            className="text-purple-600 hover:text-purple-700 mb-4 inline-block"
          >
            ← Back to Dashboard
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Weather Insights
          </h1>
          <p className="text-gray-600">
            Get intelligent weather analysis and personalized recommendations
          </p>
        </div>

        {/* City Selector */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select City
          </label>
          <select
            value={selectedCity?.id || ''}
            onChange={(e) => {
              const city = cities.find((c) => c.id === parseInt(e.target.value));
              if (city) setSelectedCity(city);
            }}
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          >
            {cities.map((city) => (
              <option key={city.id} value={city.id}>
                {city.name}, {city.country}
              </option>
            ))}
          </select>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-t-lg shadow-md">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('summary')}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === 'summary'
                  ? 'border-b-2 border-purple-500 text-purple-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Daily Summary
            </button>
            <button
              onClick={() => setActiveTab('clothing')}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === 'clothing'
                  ? 'border-b-2 border-purple-500 text-purple-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Clothing Advice
            </button>
            <button
              onClick={() => setActiveTab('custom')}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === 'custom'
                  ? 'border-b-2 border-purple-500 text-purple-600'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Custom Query
            </button>
          </div>

          <div className="p-6">
            {/* Daily Summary Tab */}
            {activeTab === 'summary' && (
              <div>
                <p className="text-gray-600 mb-4">
                  Get an AI-powered summary of today's weather conditions and what to expect.
                </p>
                <button
                  onClick={handleDailySummary}
                  disabled={loading || !selectedCity}
                  className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Generating...' : 'Get Daily Summary'}
                </button>
              </div>
            )}

            {/* Clothing Recommendation Tab */}
            {activeTab === 'clothing' && (
              <div>
                <p className="text-gray-600 mb-4">
                  Get personalized clothing recommendations based on current weather conditions.
                </p>
                <button
                  onClick={handleClothingRecommendation}
                  disabled={loading || !selectedCity}
                  className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  {loading ? 'Generating...' : 'Get Clothing Advice'}
                </button>
              </div>
            )}

            {/* Custom Query Tab */}
            {activeTab === 'custom' && (
              <div>
                <form onSubmit={handleCustomQuery} className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ask anything about the weather
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder="e.g., What should I wear today?"
                      className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      disabled={loading}
                    />
                    <button
                      type="submit"
                      disabled={loading || !query.trim() || !selectedCity}
                      className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                    >
                      {loading ? 'Asking...' : 'Ask AI'}
                    </button>
                  </div>
                </form>

                {/* Suggested Queries */}
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">
                    Suggested questions:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {suggestedQueries.map((suggested, index) => (
                      <button
                        key={index}
                        onClick={() => setQuery(suggested)}
                        className="text-sm bg-purple-100 text-purple-700 px-3 py-1 rounded-full hover:bg-purple-200 transition-colors"
                        disabled={loading}
                      >
                        {suggested}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Insights History */}
        <div className="mt-8 space-y-4">
          {insights.map((insight, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-md p-6 animate-fade-in"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {insight.city_name}
                  </h3>
                  {insight.query && (
                    <p className="text-sm text-gray-600 mb-3 italic">
                      "{insight.query}"
                    </p>
                  )}
                </div>
                <span className="text-xs text-gray-500">
                  {new Date().toLocaleTimeString()}
                </span>
              </div>
              <div className="prose prose-sm max-w-none text-gray-700">
                {insight.insight.split('\n').map((line, i) => (
                  <p key={i} className="mb-2">
                    {line}
                  </p>
                ))}
              </div>
            </div>
          ))}

          {insights.length === 0 && (
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <div className="text-6xl mb-4">🤖</div>
              <p className="text-gray-600 text-lg mb-2">
                No insights yet
              </p>
              <p className="text-gray-500">
                Select a tab above to get AI-powered weather insights
              </p>
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Note:</strong> AI insights require an OpenAI API key to be configured
            in your backend .env file. Make sure the OPENAI_API_KEY is set correctly.
          </p>
        </div>
      </div>
    </div>
  );
}
