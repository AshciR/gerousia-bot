"""
This module will hold the functions used for
interacting with the Discord APIs
"""
import hikari
from hikari.impl.rest import RESTClientImpl
from hikari.iterators import LazyIterator
from typing import Sequence
import asyncio
import os
from dotenv import load_dotenv

def get_api_token(key) -> str:
    """
    Gets the API token for a given key
    :param key: the key for the token you want returned
    :return: the API token
    """
    load_dotenv()
    return os.getenv(key)

def get_rest_client() -> RESTClientImpl:
    rest_app = hikari.RESTApp()
    token = get_api_token("DISCORD_API_KEY")
    rest_client = rest_app.acquire(token, "Bot")
    return rest_client
    

async def get_my_user(rest_client) -> hikari.OwnUser:
    async with rest_client as client:
        user = await client.fetch_my_user()
        return user

async def get_my_guilds(rest_client) -> LazyIterator[hikari.OwnGuild]:
    async with rest_client as client:
        guilds = await client.fetch_my_guilds()
        return guilds
        
async def get_guild_channels(rest_client,guild) -> Sequence[hikari.GuildChannel]:
    async with rest_client as client:
        channels = await client.fetch_guild_channels(guild)
        return channels

def print_user():
    rest_client = get_rest_client()
    user = asyncio.run(get_my_user(rest_client))
    print(user)

def print_guild():
    rest_client = get_rest_client()
    guild = asyncio.run(get_my_guilds(rest_client))
    print(guild)

def print_channels():
    rest_client = get_rest_client()
    guild = asyncio.run(get_my_guilds(rest_client))
    channels = asyncio.run(get_guild_channels(rest_client,guild[0]))
    print(channels)

def ping_server() -> int:
    """Placeholder function that will ping the discord server"""
    return 200
