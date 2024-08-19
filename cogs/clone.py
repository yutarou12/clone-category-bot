import json

import discord
from discord import app_commands
from discord.ext import commands


class Clone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='簡単カテゴリ複製')
    @app_commands.guild_only()
    async def cmd_clone(self, interaction: discord.Interaction, category_id: discord.CategoryChannel):
        """カテゴリを複製します。"""

        category_ch = category_id

        if not category_ch:
            return await interaction.response.send_message('指定されたカテゴリが見つかりませんでした。', ephemeral=True)

        overwrites = {}
        for overwrite in category_ch.overwrites:
            overwrites[overwrite[0]] = overwrite[1]

        new_category = await interaction.guild.create_category(category_ch.name, overwrites=overwrites)

        for channel in category_ch.channels:
            if isinstance(channel, discord.TextChannel):
                await new_category.create_text_channel(channel.name, overwrites=channel.overwrites)
            elif isinstance(channel, discord.VoiceChannel):
                await new_category.create_voice_channel(channel.name, overwrites=channel.overwrites)

        return await interaction.response.send_message('カテゴリを複製しました。')


async def setup(bot):
    bot.add_cog(Clone(bot))