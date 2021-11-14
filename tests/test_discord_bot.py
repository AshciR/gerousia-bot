from unittest.mock import AsyncMock
from unittest.mock import Mock, patch
from unittest import TestCase
import pytest
import json

from gerousiabot import utils

from gerousiabot import discord_bot

logger = utils.setup_logger()


bot_token = utils.get_env_variable('DISCORD_API_KEY')
g_bot = discord_bot.GerousiaBot(bot_token=bot_token)

class mock_status:
    def __init__(self, value): 
        self.value = value

class mock_member :
    def __init__(self, status,display_name): 
        self.status = status
        self.display_name = display_name

class mock_voice_channel :
    def __init__(self, members): 
        self.members = members

class mock_channel :
    def __init__(self, name,voice_channels): 
        self.name = name 
        self.voice_channels = voice_channels 
    
class mock_guild :
    name="Test Server"
    channels=[
        mock_channel('Voice Channels',["words"]),
        mock_channel('Voice Channels',["fail"])
        ]
    members=[
        mock_member(mock_status('online'),'test_name')
    ]

@patch('gerousiabot.discord_bot.GerousiaBot')
@patch("gerousiabot.utils.get_env_variable")
@patch.object(discord_bot.GerousiaBot, 'run')
def test_run_bot(mocked_run,mocked_get_env,mocked_bot):
    res = discord_bot.run_bot()
    mocked_get_env.assert_called()
    mocked_bot.assert_called()
    #mocked_run.assert_called()


@pytest.mark.asyncio
@patch.object(discord_bot.GerousiaBot, 'get_server_voice_channels' )
@patch.object(discord_bot.GerousiaBot, 'get_members_who_are_in_voice_channels')
@patch("gerousiabot.utils.get_env_variable",return_value='11111111111111111')
async def test_on_ready(mocked_get_env,mocked_get_members,mocked_get_server):
    res = await g_bot.on_ready()
    mocked_get_members.assert_called()
    mocked_get_server.assert_called()

@pytest.mark.asyncio
async def test_get_members_who_are_in_voice_channels():
    mocked_voice_channels = [
        mock_voice_channel(
            [
                mock_member( mock_status('offline'), 'rick'),
                mock_member( mock_status('online'), 'richie'),
                mock_member( mock_status('online'), 'paul')
            ]
        ),
        mock_voice_channel(
            [
                mock_member( mock_status('online'), 'chad'),
                mock_member( mock_status('online'), 'kirby')
            ]
        ),
        mock_voice_channel(
            [
                mock_member( mock_status('offline'), 'jk'),
            ]
        )
    ]
    res = await g_bot.get_members_who_are_in_voice_channels(mocked_voice_channels)
    TestCase().assertEqual(len(res),6)


    
@pytest.mark.asyncio
@patch.object(discord_bot.GerousiaBot, 'get_guild',return_value = mock_guild() )
async def test_get_server_voice_channels(mocked_get_guild):
    server_id = 'GOOD_LOOKING_GAMERS_SERVER_ID'
    res = await g_bot.get_server_voice_channels(server_id)
    mocked_get_guild.assert_called()


@patch("gerousiabot.discord_bot.Intents")
def test_get_intents_needed_to_check_online_members(mocked_intents):
    res = discord_bot.get_intents_needed_to_check_online_members()
    mocked_intents.default.assert_called()
    TestCase().assertTrue(res.presences)
    TestCase().assertTrue(res.members)