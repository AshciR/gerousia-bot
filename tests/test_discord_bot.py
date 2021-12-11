from unittest import TestCase
from unittest.mock import patch

import pytest

from gerousiabot import discord_bot
from gerousiabot import utils

logger = utils.setup_logger()


class MockStatus:
    def __init__(self, value):
        self.value = value


class MockMember:
    def __init__(self, status, display_name):
        self.status = status
        self.display_name = display_name


class MockVoiceChannel:
    def __init__(self, members):
        self.members = members


class MockChannel:
    def __init__(self, name, voice_channels):
        self.name = name
        self.voice_channels = voice_channels


class MockGuild:
    def __init__(self, name, channels, members):
        self.name = name
        self.channels = channels
        self.members = members


@pytest.fixture
def set_up():
    bot_token = 'DISCORD_API_KEY'
    g_bot = discord_bot.DiscordBot(bot_token=bot_token)
    return g_bot


@pytest.fixture
def get_mocked_channels():
    return [
        MockVoiceChannel(
            [
                MockMember(MockStatus('offline'), 'rick'),
                MockMember(MockStatus('online'), 'richie'),
                MockMember(MockStatus('online'), 'paul')
            ]
        ),
        MockVoiceChannel(
            [
                MockMember(MockStatus('online'), 'chad'),
                MockMember(MockStatus('online'), 'kirby')
            ]
        ),
        MockVoiceChannel(
            [
                MockMember(MockStatus('offline'), 'jk'),
            ]
        )
    ]


@patch('gerousiabot.discord_bot.DiscordBot')
@patch("gerousiabot.utils.get_env_variable")
@patch.object(discord_bot.DiscordBot, 'run')
def test_run_bot(mocked_run, mocked_get_env, mocked_bot):
    res = discord_bot.run_bot()
    mocked_get_env.assert_called()
    mocked_bot.assert_called()


@pytest.mark.asyncio
@patch.object(discord_bot.DiscordBot, 'get_server_voice_channels')
@patch.object(discord_bot.DiscordBot, 'get_members_who_are_in_voice_channels')
@patch("gerousiabot.utils.get_env_variable", return_value='11111111111111111')
async def test_on_ready(mocked_get_env, mocked_get_members, mocked_get_server, set_up):
    g_bot = set_up
    res = await g_bot.on_ready()
    mocked_get_members.assert_called()
    mocked_get_server.assert_called()


@pytest.mark.asyncio
async def test_get_members_who_are_in_voice_channels(set_up, get_mocked_channels):
    mocked_voice_channels = get_mocked_channels
    g_bot = set_up
    res = await g_bot.get_members_who_are_in_voice_channels(mocked_voice_channels)
    TestCase().assertEqual(len(res), 6)


@pytest.mark.asyncio
@patch.object(discord_bot.DiscordBot, 'get_guild', return_value=MockGuild(
    name="Test Server",
    channels=[
        MockChannel('Voice Channels', ["words"]),
        MockChannel('Voice Channels', ["fail"])
    ],
    members=[
        MockMember(MockStatus('online'), 'test_name')
    ]
))
async def test_get_server_voice_channels(mocked_get_guild, set_up):
    server_id = 'GOOD_LOOKING_GAMERS_SERVER_ID'
    g_bot = set_up
    res = await g_bot.get_server_voice_channels(server_id)
    mocked_get_guild.assert_called()
    TestCase().assertEqual(len(res), 2)


@patch("gerousiabot.discord_bot.Intents")
def test_get_intents_needed_to_check_online_members(mocked_intents):
    res = discord_bot.get_intents_needed_to_check_online_members()
    mocked_intents.default.assert_called()
    TestCase().assertTrue(res.presences)
    TestCase().assertTrue(res.members)
