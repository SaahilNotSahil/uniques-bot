import datetime

import mongoengine


class Prefix(mongoengine.Document):
    guild_name = mongoengine.StringField()
    guild_id = mongoengine.StringField(unique=True)
    guild_join_date = mongoengine.DateTimeField(
        default=datetime.datetime.now()
    )
    prefix = mongoengine.StringField()


def get_prefix(client, message):
    if Prefix.objects(guild_id=str(message.guild.id)):
        pref = Prefix.objects.get(guild_id=str(message.guild.id))
        return pref.prefix
    else:
        return "$"


def get_prefix_from_message(message):
    if Prefix.objects(guild_id=str(message.guild.id)):
        pref = Prefix.objects.get(guild_id=str(message.guild.id))
        return pref.prefix
    else:
        return "$"


def get_prefix_from_ctx(ctx):
    if Prefix.objects(guild_id=str(ctx.guild.id)):
        pref = Prefix.objects.get(guild_id=str(ctx.guild.id))
        return pref.prefix
    else:
        return "$"
