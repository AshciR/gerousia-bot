from gerousiabot.discord import discord_apis


def test_ping_server():
    assert discord_apis.ping_server() == 200
