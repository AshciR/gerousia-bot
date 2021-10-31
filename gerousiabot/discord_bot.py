from typing import List

from discord import Intents, Member, VoiceChannel, Client

from gerousiabot import utils

logger = utils.setup_logger()


class GerousiaBot(Client):

    def __init__(self, bot_token: str, **options):
        intents = get_intents_needed_to_check_online_members()
        logger.debug('Creating bot with with intents {}'.format(intents))

        super().__init__(intents=intents, **options)
        logger.debug('Creating bot with with valid token {}'.format(bot_token is not None))
        self.bot_token = bot_token

    async def on_ready(self):
        """
        Asynchronous event that fires once the bot has logged in and ready to work.
        """
        logger.info('Bot has logged in as {0.user}'.format(self))

        server_id = int(utils.get_env_variable('GOOD_LOOKING_GAMERS_SERVER_ID'))
        online_members = await self.get_server_online_members(server_id)
        guild_voice_channels = await self.get_server_voice_channels(server_id)

        # TODO: Create function that will filter guild_voice_channels based on channels with members in them
        # TODO: Can use guild_voice_channels.members
        # TODO: Collect a list that has all the member currently in channels

        for online_member in online_members:
            print(online_member.name)

    async def get_server_online_members(self, server_id: int) -> List[Member]:
        """
        Returns all the members who are online for a given server.
        :param server_id: the server id
        :return: a list of online members
        """
        server = self.get_guild(server_id)
        members = server.members
        online_members = list(filter(lambda member: member.status.value == 'online', members))

        logger.info('Returning {} online members for server {}'.format(len(online_members), server.name))
        return online_members

    async def get_server_voice_channels(self, server_id: int) -> List[VoiceChannel]:
        """
        Returns all the voice channels for a given server
        :param server_id: the server id
        :return: the voice channels
        """
        server = self.get_guild(server_id)

        # Guilds(Servers) have 2 channel types. Text and Voice
        # We only want the Voice channels.
        server_channels = list(filter(lambda x: x.name == 'Voice Channels', server.channels))

        # Guild(Servers) objects will only have 1 'Voice Channels' property
        # So it's safe to access the 0th index
        guild_voice_channels = server_channels[0].voice_channels
        return guild_voice_channels


def get_intents_needed_to_check_online_members() -> Intents:
    intents = Intents.default()
    intents.presences = True
    intents.members = True

    return intents


if __name__ == '__main__':
    bot_token = utils.get_env_variable('ASHCIR_BOT_TOKEN')
    g_bot = GerousiaBot(bot_token=bot_token)
    g_bot.run(bot_token)
