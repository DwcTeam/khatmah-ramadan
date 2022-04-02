import hikari
import lightbulb
from lightbulb.ext import tasks
import requests
import schedule
import asyncio
import threading
import time
import typing as t

task = lightbulb.Plugin(__name__)

class Cache:
    def __init__(self):
        self.data: dict = None

cache = Cache()

@tasks.task(h=2)
async def update_prayer_times():
    res = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Mecca&country=saudi%20arabia&method=2")
    cache.data = res.json()["data"]


def fetch_and_send_on_prayer_time():
    global data
    print(data)
    if data:
        prayer_times = data["timings"]
        prayer_times_str = "**Fajr:** {}\n**Dhuhr:** {}\n**Asr:** {}\n**Maghrib:** {}\n**Isha:** {}".format(
            prayer_times["Fajr"],
            prayer_times["Dhuhr"],
            prayer_times["Asr"],
            prayer_times["Maghrib"],
            prayer_times["Isha"]
        )
        print(prayer_times_str)


def run_schedule():
    print("run")
    while True:
        schedule.run_pending()
        time.sleep(1)

def load(bot: lightbulb.BotApp) -> None:
    update_prayer_times.start()
    schedule.every().day.at("12:00").do(fetch_and_send_on_prayer_time)
    threading.Thread(target=run_schedule).start()
    bot.add_plugin(task)
