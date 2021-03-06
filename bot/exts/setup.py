import hikari
import lightbulb
import config

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
async def setup_channel(ctx: lightbulb.context.SlashContext) -> None:
    channel = ctx.options.channel
    data = ctx.bot.db.find_one({"_id": ctx.guild_id})
    if not data:
        data = {"_id": ctx.guild_id, "channel": None, "role": None, "count": 0}
        ctx.bot.db.insert_one(data)
    
    if channel and (data["channel"] and data["channel"] == channel.id):
        await ctx.respond("نعتذر منك البوت مثبت مسبقاً في هذه القناة", flags=hikari.MessageFlag.EPHEMERAL)
        return
    if channel and channel.type != hikari.ChannelType.GUILD_TEXT:
        await ctx.respond("الرجاء التحقق من نوع القناة المحدده انها كتابيه", flags=hikari.MessageFlag.EPHEMERAL)
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
        except hikari.ForbiddenError:
            await ctx.respond("البوت لا يمتلك صلاحيات لصنع القناة", flags=hikari.MessageFlag.EPHEMERAL)
            return
    ctx.bot.db.update_one({"_id": ctx.guild_id}, {"$set": {"channel": channel.id}})
    await ctx.respond("الله يجزيك الخير تم تثبيت القناة بنجاح, ملاحظه سيتم الإرسال حسب توقيت مكة المكرمه")
    
@setup_command.child()
@lightbulb.option(
    name="role",
    description="الرجاء اختيار الرتبة الذي تريد تثبيت البوت",
    type=hikari.OptionType.ROLE,
    required=False
)
@lightbulb.command(name="role", description="بداء تثبيت الرول")
@lightbulb.implements(lightbulb.commands.SlashSubCommand)
async def setup_role(ctx: lightbulb.context.SlashContext) -> None:
    role = ctx.options.role
    data = ctx.bot.db.find_one({"_id": ctx.guild_id})
    if not data:
        data = {"_id": ctx.guild_id, "channel": None, "role": None, "count": 0}
        ctx.bot.db.insert_one(data)
    if role and (data["role"] and data["role"] == role.id):
        await ctx.respond("نعتذر منك البوت مثبت مسبقاً في هذه الرتبة", flags=hikari.MessageFlag.EPHEMERAL)
        return
    if not role:
        try:
            role = await ctx.bot.rest.create_role(
                ctx.guild_id, 
                name="ختمة", 
                reason="تثبيت البوت ختمة القرآن الكريم",
                color=0xffd430,
            )
        except hikari.ForbiddenError:
            await ctx.respond("البوت لا يمتلك صلاحيات لصنع الرتبة", flags=hikari.MessageFlag.EPHEMERAL)
            return
    ctx.bot.db.update_one({"_id": ctx.guild_id}, {"$set": {"role": role.id}})
    await ctx.respond("الله يجزيك الخير تم تثبيت الرتبة بنجاح, ملاحظه سيتم أرسال منشن لجميع مالكين الرتبه")


@setup_command.child()
@lightbulb.option(
    name="channel", 
    description="الرجاء اختيار القناة الذي تريد رسالة اختيار الرول", 
    type=hikari.OptionType.CHANNEL,
    required=True
)
@lightbulb.command(name="message", description="بداء تثبيت الرساله")
@lightbulb.implements(lightbulb.commands.SlashSubCommand)
async def setup_message(ctx: lightbulb.context.SlashContext) -> None:
    channel = ctx.options.channel
    data = ctx.bot.db.find_one({"_id": ctx.guild_id})
    if not data:
        data = {"_id": ctx.guild_id, "channel": None, "role": None, "count": 0}
        ctx.bot.db.insert_one(data)
    if channel and (data["channel"] and data["channel"] == channel.id):
        await ctx.respond("نعتذر منك البوت مثبت بهاذه الفناة الرجاء اختبار قناه اخرى", flags=hikari.MessageFlag.EPHEMERAL)
        return
    component = ctx.bot.rest.build_action_row()
    (
        component.add_button(hikari.ButtonStyle.PRIMARY, "add_role")
        .set_label("أضغط هنا")
        .set_emoji(config.QURAN_EMOJI)
        .add_to_container()
    )
    message = await ctx.bot.rest.create_message(
        channel,
        embed=hikari.Embed(
            description="أذا كنت تريد الحصول على أشعار بعد كل صلاة أضغط على الزر في الأسفل"
        ),
        component=component
    )
    ctx.bot.db.update_one({"_id": ctx.guild_id}, {"$set": {"message": message.id}})
    await ctx.respond("الله يجزيك الخير تم تثبيت الرساله بنجاح, ملاحظه سيتم الإرسال حسب توقيت مكة المكرمه")

@setup.command()
@lightbulb.command(name="unsetup", description="ايقاف الختمة و حذف البيانات")
@lightbulb.implements(lightbulb.commands.SlashCommand)
async def unsetup_count(ctx: lightbulb.context.SlashContext) -> None:
    ctx.bot.db.delete_one({"_id": ctx.guild_id})
    await ctx.respond("تم ايقاف الختمة و حذف البيانات")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(setup)
