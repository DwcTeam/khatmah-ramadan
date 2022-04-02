import hikari
import logging
import lightbulb
import config

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

