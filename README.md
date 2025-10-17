# Weather App - Full-Stack Multi-Technology Integration

A comprehensive weather application built with Next.js, Python FastAPI, Supabase, and AI-powered insights using LangGraph.

## Technologies Used

### Frontend
- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization (to be installed)

### Backend
- **Python 3.11+** - Backend language
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation using Python type annotations
- **LangGraph** - AI workflow orchestration
- **LangChain** - LLM integration

### Database
- **Supabase (PostgreSQL)** - Primary database with real-time capabilities
- Row-level security
- Built-in authentication

### Data Pipeline
- **Python asyncio** - Asynchronous data collection
- **APScheduler** - Scheduled data collection jobs
- **httpx** - Async HTTP client

### APIs
- **OpenWeatherMap API** - Weather data source
- **OpenAI API** - AI-powered insights

## Project Structure

```
weather-app/
├── app/                          # Next.js app directory
│   ├── components/              # React components
│   │   └── Navigation.tsx       # App navigation
│   ├── dashboard/               # Dashboard page
│   │   └── components/          # Dashboard components
│   │       └── CitySearch.tsx   # City search component
│   ├── analytics/               # Analytics page (to be created)
│   ├── insights/                # AI insights page (to be created)
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page
│   └── globals.css              # Global styles
├── api-service/                 # Python FastAPI backend
│   ├── app/
│   │   ├── models/              # Pydantic models
│   │   │   └── weather.py       # Weather data models
│   │   ├── services/            # Business logic
│   │   │   ├── weather_api.py   # Weather API integration
│   │   │   ├── database.py      # Database operations
│   │   │   └── ai_insights.py   # LangGraph AI workflows
│   │   ├── routers/             # API endpoints
│   │   │   ├── weather.py       # Weather endpoints
│   │   │   ├── cities.py        # City endpoints
│   │   │   └── insights.py      # AI insights endpoints
│   │   ├── config.py            # Configuration
│   │   └── main.py              # FastAPI app
│   └── requirements.txt         # Python dependencies
├── data-pipeline/               # ETL scripts
│   ├── etl/
│   │   └── weather_collector.py # Weather data collector
│   ├── models/
│   │   └── weather.py           # Shared models
│   ├── config.py                # Pipeline configuration
│   ├── scheduler.py             # Scheduled jobs
│   └── requirements.txt         # Python dependencies
├── lib/                         # Next.js utilities
│   ├── api.ts                   # API client
│   └── utils.ts                 # Helper functions
├── types/                       # TypeScript types
│   └── weather.ts               # Weather types
├── supabase-schema.sql          # Database schema
├── package.json                 # Node dependencies
└── README.md                    # This file
```

## Setup Instructions

### 1. Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Supabase account
- OpenWeatherMap API key
- OpenAI API key

### 2. Fix npm Permissions (if needed)

If you encounter npm permission errors, run:

```bash
sudo chown -R $(id -u):$(id -g) "$HOME/.npm"
```

### 3. Install Frontend Dependencies

```bash
npm install @supabase/supabase-js recharts date-fns clsx tailwind-merge
```

### 4. Set Up Supabase

1. Create a new Supabase project
2. Copy the SQL schema from `supabase-schema.sql`
3. Run it in the Supabase SQL editor
4. Note your Supabase URL and anon key

### 5. Set Up Python Backend

```bash
cd api-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 6. Set Up Data Pipeline

```bash
cd data-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 7. Configure Environment Variables

Create `.env` files in the project root and in both Python directories:

**Root `.env` (for Next.js):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**`api-service/.env`:**
```env
WEATHER_API_KEY=your_openweathermap_api_key
WEATHER_API_BASE_URL=https://api.openweathermap.org/data/2.5
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
OPENAI_API_KEY=your_openai_api_key
DEBUG=true
```

**`data-pipeline/.env`:**
```env
WEATHER_API_KEY=your_openweathermap_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key
COLLECTION_INTERVAL_MINUTES=60
CITIES_TO_TRACK=[5128581,2643743,1850144,5368361,2988507]
```

## Running the Application

### 1. Start the FastAPI Backend

```bash
cd api-service
source venv/bin/activate
python -m app.main
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 2. Start the Data Pipeline (Optional)

```bash
cd data-pipeline
source venv/bin/activate
python scheduler.py
```

This will collect weather data every hour for configured cities.

### 3. Start the Next.js Frontend

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Features

### 1. Real-Time Weather Dashboard
- Search for any city
- Display current weather conditions
- Temperature, humidity, wind speed, etc.
- Weather icons and descriptions

### 2. Historical Analytics
## Note: Historical Analysis currently only works for a single day because we are currently using a free version of the weather api that only allows use to fetch data up to an hour in the past. You can upgrade your api version to get the full working analysis result
- View weather trends over time
- 7-day, 14-day, 30-day analytics
- Average temperature, humidity, wind speed
- Most common weather conditions
- Interactive charts

### 3. AI-Powered Insights 
- Natural language weather queries
- Daily weather summaries
- Clothing recommendations
- Trend analysis and comparisons
- Contextual insights based on historical data

### 4. Data Pipeline
- Automated weather data collection
- Scheduled hourly updates
- ETL process with Pydantic validation
- Data normalization and storage

## API Endpoints

### Weather Endpoints
- `GET /weather/current?city={city}` - Get current weather
- `GET /weather/forecast?city={city}` - Get 5-day forecast
- `GET /weather/historical/{city_id}` - Get historical records
- `GET /weather/analytics/{city_id}?days=7` - Get analytics
- `GET /weather/latest/{city_id}` - Get latest record

### City Endpoints
- `GET /cities/` - Get all cities
- `GET /cities/search?q={query}` - Search cities

### AI Insights Endpoints
- `POST /insights/ai` - Custom AI query
- `GET /insights/summary/{city_id}` - Daily summary
- `GET /insights/clothing/{city_id}` - Clothing recommendation

## Technology Highlights

### Pydantic Models
All data is validated using Pydantic models for type safety and data integrity:
- `CurrentWeatherResponse` - API response validation
- `WeatherRecord` - Database record model
- `WeatherAnalytics` - Analytics data model

### LangGraph Workflows
AI insights use LangGraph for orchestrated workflows:
1. **Fetch Data** - Retrieve weather data from database
2. **Analyze Data** - Compute statistics and trends
3. **Generate Insight** - Use LLM to create natural language insights

### Supabase Features
- Row-level security policies
- Real-time subscriptions (ready for implementation)
- Database functions for analytics
- User authentication (ready for implementation)

## Next Steps

To complete the application, you can:

1. Install missing npm packages:
   ```bash
   npm install clsx tailwind-merge
   ```

2. Create the remaining pages:
   - `/app/analytics/page.tsx` - Analytics dashboard with charts
   - `/app/insights/page.tsx` - AI insights interface

3. Add real-time updates using Supabase subscriptions

4. Implement user authentication

5. Add more visualizations and charts

6. Deploy to production (Vercel for frontend, Railway/Render for backend)

## Database Schema

The Supabase database includes:
- `cities` - City information
- `weather_records` - Historical weather data
- `user_preferences` - User settings (with RLS)
- `latest_weather` view - Latest weather per city
- `get_weather_analytics()` function - Analytics computation

## Development Notes

- Backend uses async/await throughout for performance
- Frontend uses React Server Components where possible
- Type safety with TypeScript and Pydantic
- Modular architecture for easy extension
- Comprehensive error handling

## License

MIT

## Support

For issues or questions, please check:
- FastAPI docs: https://fastapi.tiangolo.com
- Next.js docs: https://nextjs.org/docs
- LangGraph docs: https://langchain-ai.github.io/langgraph
- Supabase docs: https://supabase.com/docs
