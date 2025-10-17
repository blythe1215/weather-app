export interface Coordinates {
  lat: number;
  lon: number;
}

export interface WeatherCondition {
  id: number;
  main: string;
  description: string;
  icon: string;
}

export interface MainWeatherData {
  temp: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  pressure: number;
  humidity: number;
}

export interface Wind {
  speed: number;
  deg: number;
  gust?: number;
}

export interface Clouds {
  all: number;
}

export interface CurrentWeather {
  coord: Coordinates;
  weather: WeatherCondition[];
  main: MainWeatherData;
  visibility: number;
  wind: Wind;
  clouds: Clouds;
  dt: number;
  sys: {
    country: string;
    sunrise: number;
    sunset: number;
  };
  timezone: number;
  id: number;
  name: string;
}

export interface WeatherRecord {
  id: number;
  city_id: number;
  city_name: string;
  country: string;
  latitude: number;
  longitude: number;
  temperature: number;
  feels_like: number;
  temp_min: number;
  temp_max: number;
  pressure: number;
  humidity: number;
  wind_speed: number;
  wind_direction: number;
  cloudiness: number;
  visibility: number;
  weather_main: string;
  weather_description: string;
  weather_icon: string;
  recorded_at: string;
  created_at: string;
}

export interface City {
  id: number;
  city_id: number;
  name: string;
  country: string;
  latitude: number;
  longitude: number;
  timezone: number;
  created_at: string;
}

export interface WeatherAnalytics {
  city_name: string;
  country: string;
  period_start: string;
  period_end: string;
  avg_temperature: number;
  max_temperature: number;
  min_temperature: number;
  avg_humidity: number;
  avg_wind_speed: number;
  most_common_condition: string;
  total_records: number;
}

export interface InsightResponse {
  city_id: number;
  city_name: string;
  query: string;
  insight: string;
}

export interface ForecastItem {
  dt: number;
  main: MainWeatherData;
  weather: WeatherCondition[];
  clouds: Clouds;
  wind: Wind;
  visibility: number;
  pop: number;
  dt_txt: string;
}

export interface ForecastResponse {
  list: ForecastItem[];
  city: {
    id: number;
    name: string;
    coord: Coordinates;
    country: string;
    timezone: number;
    sunrise: number;
    sunset: number;
  };
}
