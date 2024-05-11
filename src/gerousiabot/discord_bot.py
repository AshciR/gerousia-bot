from typing import List

from discord import Intents, VoiceChannel, Client

from src.gerousiabot import utils

logger = utils.setup_logger()


class DiscordBot(Client):

    def __init__(self, bot_token: str, **options):
        intents = get_intents_needed_to_check_online_members()
        logger.debug('Creating DiscordBot with with intents {}'.format(intents))

        super().__init__(bot_token=bot_token, intents=intents, **options)
        logger.debug('Creating DiscordBot with with valid token {}'.format(bot_token is not None))

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
        Gets all the members who are in voice channels for a given server
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
        flattened_online_members = sum(online_members, [])

        online_members_display_names = list(
            map(lambda member: member.display_name, flattened_online_members)
        )

        return online_members_display_names

    async def get_server_voice_channels(self, server_id: int) -> List[VoiceChannel]:
        """
        Returns all the voice channels for a given server
        :param server_id: the server id
        :return: the voice channels
        """
        server = self.get_guild(server_id)

        # Guilds(Servers) have 2 channel types. Text and Voice
        # We only want the Servers with Voice channels.
        server_channels = list(filter(lambda x: hasattr(x, 'voice_channels'), server.channels))

        # Guild(Servers) channels  may have multiple 'Voice Channels' property
        # So we are checking all of them which will result in a list of lists
        guild_voice_channels = list(
            map(lambda server_channel: server_channel.voice_channels, server_channels)
        )

        # Converting from List of lists to a single List that has the voice channels
        flatten_guild_voice_channels = sum(guild_voice_channels, [])

        return flatten_guild_voice_channels


def get_intents_needed_to_check_online_members() -> Intents:
    intents = Intents.default()
    intents.presences = True
    intents.members = True

    return intents


def run_bot() -> DiscordBot:
    """
    Starts the Discord bot
    :return: the started DiscordBot
    """
    bot_token = utils.get_env_variable('DISCORD_API_KEY')
    discord_bot = DiscordBot(bot_token=bot_token)
    discord_bot.run(bot_token)

    return discord_bot
