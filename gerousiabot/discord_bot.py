import discord
# TODO: Put these into a function
from discord import Intents

from gerousiabot import utils

logger = utils.setup_logger()


class GerousiaBot(discord.Client):

    def __init__(self, bot_token: str, **options):

        intents = get_intents_needed_to_check_online_members()
        logger.debug('Creating bot with with intents {}'.format(intents))

        super().__init__(intents=intents, **options)
        logger.debug('Creating bot with with valid token {}'.format(bot_token is not None))
        self.bot_token = bot_token

    async def on_ready(self):
        logger.info('Bot has logged in as {0.user}'.format(self))

        # TODO: Replace this with GLG server id
        server_id = int(utils.get_env_variable('GOOD_LOOKING_GAMERS_SERVER_ID'))
        guild = self.get_guild(server_id)

        # TODO: Create function for this (Might not need it tho)
        members = guild.members
        online_members = list(filter(lambda member: member.status.value == 'online', members))

        # TODO: Create function for this
        # The filter is ensured to return only 1 value b/c we're only checking this guild
        guild_voice_channels = list(filter(lambda x: x.name == 'Voice Channels', guild.channels))[0].voice_channels

        # TODO: Create function that will filter guild_voice_channels based on channels with members in them
        # TODO: Can use guild_voice_channels.members
        # TODO: Collect a list that has all the member currently in channels

        for online_member in online_members:
            print(online_member.name)


def get_intents_needed_to_check_online_members() -> Intents:
    intents = discord.Intents.default()
    intents.presences = True
    intents.members = True

    return intents


# TODO: Make this it's own function


if __name__ == '__main__':
    bot_token = utils.get_env_variable('ASHCIR_BOT_TOKEN')
    g_bot = GerousiaBot(bot_token=bot_token)
    g_bot.run(bot_token)
