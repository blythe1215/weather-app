import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from etl.weather_collector import WeatherDataCollector
from config import settings


class WeatherDataScheduler:
    """Scheduler for automated weather data collection"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.collector = WeatherDataCollector()

    async def collect_weather_job(self):
        """Job to collect weather data"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled weather collection...")
        try:
            await self.collector.run_collection()
        except Exception as e:
            print(f"Error in scheduled job: {str(e)}")

    def start(self):
        """Start the scheduler"""
        # Schedule weather collection at configured interval
        self.scheduler.add_job(
            self.collect_weather_job,
            trigger=IntervalTrigger(minutes=settings.collection_interval_minutes),
            id="weather_collection",
            name="Weather Data Collection",
            replace_existing=True
        )

        print(f"Weather data scheduler started!")
        print(f"Collection interval: {settings.collection_interval_minutes} minutes")
        print(f"Tracking {len(settings.cities_to_track)} cities")
        print(f"Next run will start in {settings.collection_interval_minutes} minutes\n")

        self.scheduler.start()

    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        print("Scheduler stopped")


async def main():
    """Main entry point for the scheduler"""
    scheduler = WeatherDataScheduler()

    # Run initial collection immediately
    print("Running initial data collection...")
    await scheduler.collector.run_collection()

    # Start scheduled collections
    scheduler.start()

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("\nShutting down scheduler...")
        scheduler.stop()


if __name__ == "__main__":
    asyncio.run(main())
