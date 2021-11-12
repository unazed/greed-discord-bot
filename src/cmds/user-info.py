from discord.guild import Guild
from discord.member import Member
from lib.client import DiscordClient
from discord import Message, Embed
from src import utils
import discord


__COMMAND__ = "userinfo"


async def position(guild: Guild, member: Member):
  if member.created_at is None:
      return "n/a"
  pos = sum(other.joined_at < member.joined_at for other in guild.members if other != member and other.joined_at is not None)
  return f"{1+pos}/{len(guild.members)}"


async def invoke(bot: DiscordClient, message: Message, user_id: int):
  if isinstance(user_id, str):
    if not user_id.isnumeric():
      return await bot.alert_user(message.channel, message.author,
          "the provided user ID is non-numeric")
    user_id = int(user_id)
  
  try:
    user = await message.guild.fetch_member(user_id)
    join_position = await position(message.guild, user)
    guild_join_date = utils.format_date(user.joined_at)
    guild_boost_date = utils.format_date(user.premium_since)
  except discord.errors.NotFound:
    try:
      user = await bot.fetch_user(user_id)
      join_position = "n/a"
      guild_join_date = "n/a"
      guild_boost_date = "n/a"
    except discord.errors.NotFound:
      return await bot.alert_user(message.channel, message.author,
          "the given user ID doesn't exist")

  embed = Embed(
    title=str(user),
    description=f"{user_id} - Join position: {join_position}",
    color=0x7d7d7d
    )

  embed.set_author(
    name=str(message.author),
    icon_url=message.author.avatar_url
  )

  embed.set_thumbnail(
    url=user.avatar_url
    )

  embed.add_field(
    name="Registration date",
    value=utils.format_date(user.created_at),
    inline=False
    )

  embed.add_field(
    name="Guild join date",
    value=guild_join_date,
    inline=False
    )

  embed.add_field(
    name="Last guild boost date",
    value=guild_boost_date,
    inline=False
    )

  embed.set_footer(text="greedy-bot")
  await message.channel.send(embed=embed)
  
  