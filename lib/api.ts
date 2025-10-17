import type {
  CurrentWeather,
  ForecastResponse,
  WeatherRecord,
  WeatherAnalytics,
  City,
  InsightResponse
} from '@/types/weather';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class WeatherAPI {
  static async getCurrentWeather(city: string): Promise<CurrentWeather> {
    // Try real API first, fall back to demo if it fails
    try {
      const response = await fetch(
        `${API_BASE_URL}/weather/current?city=${encodeURIComponent(city)}`
      );

      if (response.ok) {
        return response.json();
      }
    } catch (error) {
      console.warn('Real API failed, using demo data:', error);
    }

    // Use demo endpoint as fallback
    const demoResponse = await fetch(
      `${API_BASE_URL}/demo/weather/current?city=${encodeURIComponent(city)}`
    );

    if (!demoResponse.ok) {
      throw new Error('Failed to fetch weather data');
    }

    return demoResponse.json();
  }

  static async getForecast(city: string): Promise<ForecastResponse> {
    const response = await fetch(
      `${API_BASE_URL}/weather/forecast?city=${encodeURIComponent(city)}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch forecast');
    }

    return response.json();
  }

  static async getHistoricalWeather(
    cityId: number,
    limit: number = 100
  ): Promise<WeatherRecord[]> {
    const response = await fetch(
      `${API_BASE_URL}/weather/historical/${cityId}?limit=${limit}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch historical weather');
    }

    return response.json();
  }

  static async getWeatherAnalytics(
    cityId: number,
    days: number = 7
  ): Promise<WeatherAnalytics> {
    const response = await fetch(
      `${API_BASE_URL}/weather/analytics/${cityId}?days=${days}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch weather analytics');
    }

    return response.json();
  }

  static async getLatestWeather(cityId: number): Promise<WeatherRecord> {
    const response = await fetch(
      `${API_BASE_URL}/weather/latest/${cityId}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch latest weather');
    }

    return response.json();
  }

  static async getAllCities(): Promise<City[]> {
    const response = await fetch(`${API_BASE_URL}/cities/`);

    if (!response.ok) {
      throw new Error('Failed to fetch cities');
    }

    return response.json();
  }

  static async searchCities(query: string): Promise<City[]> {
    const response = await fetch(
      `${API_BASE_URL}/cities/search?q=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      throw new Error('Failed to search cities');
    }

    return response.json();
  }

  static async getAIInsight(
    cityId: number,
    cityName: string,
    query: string
  ): Promise<InsightResponse> {
    const response = await fetch(`${API_BASE_URL}/insights/ai`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        city_id: cityId,
        city_name: cityName,
        query: query,
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to get AI insight');
    }

    return response.json();
  }

  static async getDailySummary(
    cityId: number,
    cityName: string
  ): Promise<InsightResponse> {
    const response = await fetch(
      `${API_BASE_URL}/insights/summary/${cityId}?city_name=${encodeURIComponent(cityName)}`
    );

    if (!response.ok) {
      throw new Error('Failed to get daily summary');
    }

    return response.json();
  }

  static async getClothingRecommendation(
    cityId: number,
    cityName: string
  ): Promise<InsightResponse> {
    const response = await fetch(
      `${API_BASE_URL}/insights/clothing/${cityId}?city_name=${encodeURIComponent(cityName)}`
    );

    if (!response.ok) {
      throw new Error('Failed to get clothing recommendation');
    }

    return response.json();
  }
}
