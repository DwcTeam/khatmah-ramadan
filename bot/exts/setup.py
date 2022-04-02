import hikari
import lightbulb


setup = lightbulb.Plugin(__name__)


@setup.command()
@lightbulb.option(
    name="channel", 
    description="الرجاء اختيار الروم الذي تريد تثبيت البوت", 
    type=hikari.OptionType.CHANNEL,
    required=False
)
@lightbulb.command(name="setup", description="بداء تثبيت البوت")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def setup_command(ctx: lightbulb.context.SlashContext) -> None:
    channel = ctx.raw_options.get("channel", None)
    


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(setup)
