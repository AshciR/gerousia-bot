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
        guild_voice_channels = await self.get_server_voice_channels(server_id)
        members_in_voice_channels = await self.get_members_who_are_in_voice_channels(guild_voice_channels)

        for member in members_in_voice_channels:
            print(member)

    async def get_members_who_are_in_voice_channels(self, voice_channels: List[VoiceChannel]) -> List[str]:
        """
        Gets all of the members who are in voice channels for a given server
        :param voice_channels: a list of voice channels
        :return: A list of strings with each members display name in Discord
        """
        voice_channels_with_members = list(
            (filter(lambda voice_channel: len(voice_channel.members) != 0, voice_channels))
        )

        # This will be a list of lists
        # [ [member_0, member_1], [member_2], etc ]
        online_members = list(
            map(lambda voice_channel: voice_channel.members, voice_channels_with_members)
        )

        # Converting from List of lists to a single List that has the members
        flattened_online_members = [online_member for members in online_members for online_member in members]

        online_members_display_names = list(
            map(lambda member: member.display_name, flattened_online_members)
        )

        return online_members_display_names

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
