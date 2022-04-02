import hikari
import lightbulb
from lightbulb.ext import tasks

task = lightbulb.Plugin(__name__)


@task.listener(hikari.InteractionCreateEvent)
async def interaction_create_event(event: hikari.InteractionCreateEvent) -> None:
    if event.interaction.custom_id == "add_role" and event.interaction.type == hikari.InteractionType.BUTTON:
        guild_id = event.interaction.member.guild_id
        data = task.bot.db.find_one({"_id": guild_id})
        if not data or data["channel"] != event.interaction.channel_id:
            return
        if not data["role"] or not task.bot.cache.get_role(data["role"]):
            await event.app.rest.create_interaction_response(
                interaction=event.interaction,
                token=event.interaction.token,
                response_type=hikari.ResponseType.MESSAGE_CREATE,
                content="نعتذر منك يجب تثبيت رتبه للبوت في السيرفر",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return
        role = task.bot.cache.get_role(data["role"])
        user = task.bot.cache.get_member(guild_id, event.interaction.member.user)
        if not user:
            user = await event.app.rest.fetch_member(guild_id, event.interaction.member.user)
        role_ids = user.role_ids
        if role.id in role_ids:
            await event.app.rest.remove_role_from_member(guild_id, user, role)
            await event.app.rest.create_interaction_response(
                interaction=event.interaction,
                token=event.interaction.token,
                response_type=hikari.ResponseType.MESSAGE_CREATE,
                content="تم الغاء أشتراك بالرتبه بنجاح",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            task.bot.db.update_one({"_id": guild_id}, {"$set": {"count": data["count"] - 1}})
        else:
            await event.app.rest.add_role_to_member(guild_id, user, role)
            await event.app.rest.create_interaction_response(
                interaction=event.interaction,
                token=event.interaction.token,
                response_type=hikari.ResponseType.MESSAGE_CREATE,
                content="تمت أضافتك للخمته بنجاح",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            task.bot.db.update_one({"_id": guild_id}, {"$set": {"count": data["count"] + 1}})


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(task)