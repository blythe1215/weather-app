# OpenWeatherMap API Key Instructions

## Current Status

Your app is now working with **DEMO DATA** for testing! You can search for:
- **London**
- **Paris**
- **Tokyo**

The app will show demo weather data for these cities.

## To Use Real Weather Data

### 1. Get a Free API Key

1. Go to https://openweathermap.org/api
2. Click "Sign Up" (Free tier is perfect!)
3. Verify your email
4. Log in and go to "API keys" section
5. Copy your API key

**Note:** New API keys can take up to 2 hours to activate.

### 2. Update Your Configuration

Open the file: `/Users/blytheweng/Desktop/weather-app/api-service/.env`

Replace this line:
```
WEATHER_API_KEY=a55fc535cb0d7888495df8f076298ad3
```

With your new key:
```
WEATHER_API_KEY=your_new_api_key_here
```

### 3. Restart the Backend

```bash
# Stop the current server (Ctrl+C in the terminal where it's running)
# Then restart:
cd api-service
source venv/bin/activate
python -m app.main
```

### 4. Test Real API

Once your key is active, the app will automatically use the real OpenWeatherMap API for ALL cities worldwide!

## How It Works Now

The app uses a **smart fallback system**:

1. **First**: Tries to fetch real weather data from OpenWeatherMap
2. **If that fails**: Uses demo data for London, Paris, or Tokyo
3. **Result**: You can test the UI immediately!

## Demo Data Details

The demo endpoint provides:
- **London**: Clear sky, 15°C
- **Paris**: Few clouds, 17°C
- **Tokyo**: Light rain, 18°C

All with realistic:
- Temperature ranges
- Humidity
- Wind speed
- Sunrise/sunset times
- Weather icons

## Troubleshooting

### "Invalid API key" error
- Your key needs 1-2 hours to activate after signup
- Check you copied the entire key correctly
- Make sure there are no spaces before/after the key

### App still showing demo data
- Restart the backend server after updating the key
- Check the `.env` file was saved correctly
- Wait for key activation (can take up to 2 hours)

### Need help?
Check the logs in the terminal where the backend is running for detailed error messages.

## Free Tier Limits

OpenWeatherMap free tier includes:
- 60 calls per minute
- 1,000,000 calls per month
- Current weather data
- 5-day forecast
- More than enough for development!

## Current Setup

✅ Demo mode working
⏳ Waiting for your real API key
🚀 Ready to test the UI now!

Try it at: **http://localhost:3000**
