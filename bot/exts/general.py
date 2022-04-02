import hikari
import lightbulb

general = lightbulb.Plugin(__name__)


@general.command()
@lightbulb.command(name="help",  description="الحصول على أوامر المساعده")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def help_command(ctx: lightbulb.context.SlashContext) -> None:
    await ctx.respond(embed=hikari.Embed(
        description="""
`/setup channel` - لتثبيت القناة المراد أرسال الختمه بها
`/setup role` - لتثبيت الرتبة المراد أرسال اشغار لها
`/setup message` - لصنع رساله لأضافة الرتبه منها بشكل أختياري للأعضاء
`/unsetup` - للإقاف الختمة من الخادم
`/source` - الحصول على مصدر برمجة البوت
"""
    ))

@general.command()
@lightbulb.command(name="source", description="الحصول على مصدر برمجة البوت")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def source_command(ctx: lightbulb.context.SlashContext) -> None:
    await ctx.respond("https://github.com/DwcTeam/seal_bot", flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(general)
