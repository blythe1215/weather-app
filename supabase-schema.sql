-- Supabase Database Schema for Weather App

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cities table
CREATE TABLE IF NOT EXISTS cities (
    id BIGSERIAL PRIMARY KEY,
    city_id INTEGER UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(10) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    timezone INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_city UNIQUE (city_id, name, country)
);

-- Create index on city_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_cities_city_id ON cities(city_id);
CREATE INDEX IF NOT EXISTS idx_cities_name ON cities(name);

-- Weather records table
CREATE TABLE IF NOT EXISTS weather_records (
    id BIGSERIAL PRIMARY KEY,
    city_id INTEGER NOT NULL REFERENCES cities(city_id) ON DELETE CASCADE,
    city_name VARCHAR(255) NOT NULL,
    country VARCHAR(10) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    feels_like DECIMAL(5, 2) NOT NULL,
    temp_min DECIMAL(5, 2) NOT NULL,
    temp_max DECIMAL(5, 2) NOT NULL,
    pressure INTEGER NOT NULL,
    humidity INTEGER NOT NULL,
    wind_speed DECIMAL(5, 2) NOT NULL,
    wind_direction INTEGER NOT NULL,
    cloudiness INTEGER NOT NULL,
    visibility INTEGER NOT NULL,
    weather_main VARCHAR(50) NOT NULL,
    weather_description VARCHAR(255) NOT NULL,
    weather_icon VARCHAR(10) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for weather_records
CREATE INDEX IF NOT EXISTS idx_weather_records_city_id ON weather_records(city_id);
CREATE INDEX IF NOT EXISTS idx_weather_records_recorded_at ON weather_records(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_weather_records_city_recorded ON weather_records(city_id, recorded_at DESC);

-- User preferences table (for authenticated users)
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    favorite_cities JSONB DEFAULT '[]'::jsonb,
    temperature_unit VARCHAR(10) DEFAULT 'celsius',
    wind_speed_unit VARCHAR(10) DEFAULT 'ms',
    notifications_enabled BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_preferences UNIQUE (user_id)
);

-- Create index on user_id
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_user_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own preferences
CREATE POLICY "Users can view own preferences"
    ON user_preferences FOR SELECT
    USING (auth.uid() = user_id);

-- Policy: Users can only insert their own preferences
CREATE POLICY "Users can insert own preferences"
    ON user_preferences FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only update their own preferences
CREATE POLICY "Users can update own preferences"
    ON user_preferences FOR UPDATE
    USING (auth.uid() = user_id);

-- Policy: Users can only delete their own preferences
CREATE POLICY "Users can delete own preferences"
    ON user_preferences FOR DELETE
    USING (auth.uid() = user_id);

-- Make cities and weather_records readable by everyone (public data)
ALTER TABLE cities ENABLE ROW LEVEL SECURITY;
ALTER TABLE weather_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Cities are viewable by everyone"
    ON cities FOR SELECT
    USING (true);

CREATE POLICY "Weather records are viewable by everyone"
    ON weather_records FOR SELECT
    USING (true);

-- View for latest weather per city
CREATE OR REPLACE VIEW latest_weather AS
SELECT DISTINCT ON (city_id)
    id,
    city_id,
    city_name,
    country,
    latitude,
    longitude,
    temperature,
    feels_like,
    temp_min,
    temp_max,
    pressure,
    humidity,
    wind_speed,
    wind_direction,
    cloudiness,
    visibility,
    weather_main,
    weather_description,
    weather_icon,
    recorded_at,
    created_at
FROM weather_records
ORDER BY city_id, recorded_at DESC;

-- Function to get weather analytics for a city
CREATE OR REPLACE FUNCTION get_weather_analytics(
    p_city_id INTEGER,
    p_start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW() - INTERVAL '7 days',
    p_end_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
)
RETURNS TABLE (
    city_name VARCHAR,
    country VARCHAR,
    period_start TIMESTAMP WITH TIME ZONE,
    period_end TIMESTAMP WITH TIME ZONE,
    avg_temperature DECIMAL,
    max_temperature DECIMAL,
    min_temperature DECIMAL,
    avg_humidity DECIMAL,
    avg_wind_speed DECIMAL,
    most_common_condition VARCHAR,
    total_records BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        wr.city_name,
        wr.country,
        p_start_date,
        p_end_date,
        ROUND(AVG(wr.temperature)::DECIMAL, 2) as avg_temperature,
        MAX(wr.temp_max) as max_temperature,
        MIN(wr.temp_min) as min_temperature,
        ROUND(AVG(wr.humidity)::DECIMAL, 2) as avg_humidity,
        ROUND(AVG(wr.wind_speed)::DECIMAL, 2) as avg_wind_speed,
        MODE() WITHIN GROUP (ORDER BY wr.weather_main) as most_common_condition,
        COUNT(*)::BIGINT as total_records
    FROM weather_records wr
    WHERE wr.city_id = p_city_id
        AND wr.recorded_at BETWEEN p_start_date AND p_end_date
    GROUP BY wr.city_name, wr.country;
END;
$$ LANGUAGE plpgsql;

-- Insert some default cities for testing
INSERT INTO cities (city_id, name, country, latitude, longitude, timezone)
VALUES
    (5128581, 'New York', 'US', 40.7143, -74.0060, -14400),
    (2643743, 'London', 'GB', 51.5085, -0.1257, 0),
    (1850144, 'Tokyo', 'JP', 35.6895, 139.6917, 32400),
    (5368361, 'Los Angeles', 'US', 34.0522, -118.2437, -25200),
    (2988507, 'Paris', 'FR', 48.8534, 2.3488, 3600)
ON CONFLICT (city_id) DO NOTHING;
