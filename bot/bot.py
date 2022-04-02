import hikari
import logging
import lightbulb
import config
import pymongo

log = logging.getLogger(__name__)

class Bot(lightbulb.BotApp):
    def __init__(self) -> None:
        super().__init__(
            config.TOKEN, 
            banner=None, 
            intents=hikari.Intents.ALL, 
            default_enabled_guilds=config.DEFAULT_GUILDS_ENABELS,
        )
        self.print_banner("bot.banner", True, True)
        self.load_extensions_from("bot/exts")
        self.mongodb = pymongo.MongoClient(config.MONGO_DB_URI)
        self.db = self.mongodb.get_database("fa-azcrone").get_collection("seal")

    async def on_ready(self, event: hikari.StartedEvent) -> None:
        log.info("Logged in as %s", self.get_me().username)
    
    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartedEvent, self.on_ready)

        super().run(
            activity=hikari.Activity(
                name="رمضان كريم",
                type=hikari.ActivityType.PLAYING
            ),
            status=hikari.Status.IDLE
        )

