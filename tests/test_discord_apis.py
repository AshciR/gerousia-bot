from unittest.mock import AsyncMock
from unittest.mock import Mock, patch

import pytest

from gerousiabot import discord_apis


@patch("gerousiabot.utils.get_env_variable")
@patch("gerousiabot.discord_apis.hikari.RESTApp.acquire")
@patch("gerousiabot.discord_apis.hikari.RESTApp")
def test_get_rest_client(mocked_rest_app, mocked_acquire, mocked_get_api_token):
    discord_apis.get_rest_client()

    mocked_rest_app.assert_called()
    mocked_get_api_token.assert_called()
    mocked_get_api_token.assert_called_with("DISCORD_API_KEY")
    # TODO: mock the acquire function
    # mocked_acquire.assert_called()


class AsyncContextManager():
    def __init__(self, mock):
        self.mock = mock

    async def __aenter__(self):
        return self.mock

    async def __aexit__(self, *args):
        return


@pytest.mark.asyncio
async def test_get_my_user():
    client = Mock()
    client.fetch_my_user = AsyncMock()

    acm = AsyncContextManager(client)

    await discord_apis.get_my_user(acm)

    client.fetch_my_user.assert_called()


@pytest.mark.asyncio
async def test_get_my_guilds():
    client = Mock()
    client.fetch_my_guilds = AsyncMock()

    acm = AsyncContextManager(client)

    await discord_apis.get_my_guilds(acm)

    client.fetch_my_guilds.assert_called()


@pytest.mark.asyncio
async def test_get_guild_channels():
    client = Mock()
    client.fetch_guild_channels = AsyncMock()

    acm = AsyncContextManager(client)

    await discord_apis.get_guild_channels(acm, 'Test Guild')

    client.fetch_guild_channels.assert_called()


@patch("gerousiabot.discord_apis.get_rest_client")
@patch("gerousiabot.discord_apis.get_my_user")
def test_print_user(mocked_get_my_user, mocked_get_rest_client):
    discord_apis.print_user()

    mocked_get_my_user.assert_called()
    mocked_get_rest_client.assert_called()


@patch("gerousiabot.discord_apis.get_rest_client")
@patch("gerousiabot.discord_apis.get_my_guilds")
def test_print_guild(mocked_get_my_guilds, mocked_get_rest_client):
    discord_apis.print_guild()

    mocked_get_my_guilds.assert_called()
    mocked_get_rest_client.assert_called()


@patch("gerousiabot.discord_apis.get_rest_client")
@patch("gerousiabot.discord_apis.get_my_guilds")
@patch("gerousiabot.discord_apis.get_guild_channels")
def test_print_channels(mocked_get_guild_channels, mocked_get_my_guilds, mocked_get_rest_client):
    discord_apis.print_channels()

    mocked_get_my_guilds.assert_called()
    mocked_get_guild_channels.assert_called()
    mocked_get_rest_client.assert_called()


def test_ping_server():
    assert discord_apis.ping_server() == 200
