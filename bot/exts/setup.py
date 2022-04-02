import hikari
import lightbulb


setup = lightbulb.Plugin(__name__)

@setup.command()
@lightbulb.command(name="setup", description="بداء تثبيت البوت")
@lightbulb.implements(lightbulb.commands.SlashCommandGroup)
async def setup_command(ctx: lightbulb.context.SlashContext) -> None:
    ...

@setup_command.child()
@lightbulb.option(
    name="channel", 
    description="الرجاء اختيار القناة الذي تريد تثبيت البوت", 
    type=hikari.OptionType.CHANNEL,
    required=False
)
@lightbulb.command(name="channel", description="بداء تثبيت القناة")
@lightbulb.implements(lightbulb.commands.SlashSubCommand)
async def setup_command(ctx: lightbulb.context.SlashContext) -> None:
    channel = ctx.options.channel
    data = ctx.bot.db.find_one({"_id": ctx.guild_id})
    if not data:
        data = {"_id": ctx.guild_id, "channel": None, "role": None}
        ctx.bot.db.insert_one(data)
    
    if channel and (data["channel"] and data["channel"] == channel.id):
        await ctx.respond("نعتذر منك البوت مثبت مسبقاً في هذه القناة", flags=hikari.MessageFlag.EPHEMERAL)
        return
    if not channel:
        try:
            channel = await ctx.bot.rest.create_guild_text_channel(
                ctx.guild_id, 
                "ختمة رمضان", 
                topic="رمضان كريم تم انشاء هاذه القناة بواسطة بوت الختمه\nالبوت يقوم بأرسال 4 صفحات بعد الصلاوات المفروضة بمعدل جزئ يومياٌ و ختمة القرآن الكريم خلال الشهر الفضيل",
                reason="تثبيت البوت ختمة القرآن الكريم",
                permission_overwrites=[
                    hikari.PermissionOverwrite(
                        id=list(ctx.bot.cache.get_roles_view_for_guild(ctx.guild_id).values())[0].id,
                        type=hikari.PermissionOverwriteType.ROLE,
                        deny=hikari.Permissions.SEND_MESSAGES
                    ),
                ]
            )
        except hikari.errors.ForbiddenError:
            await ctx.respond("البوت لا يمتلك صلاحيات لصنع القناة", flags=hikari.MessageFlag.EPHEMERAL)
            return
    ctx.bot.db.update_one({"_id": ctx.guild_id}, {"$set": {"channel": channel.id}})
    await ctx.respond("الله يجزيك الخير تم تثبيت القناة بنجاح, ملاحظه سيتم الإرسال حسب توقيت مكة المكرمه")
    


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(setup)
