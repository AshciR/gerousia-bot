import discord

# TODO: Split this file into small, testable, reusable functions

# TODO: Put these into a function
intents = discord.Intents.default()
intents.presences = True
intents.members = True

# TODO: Make this it's own function
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    # TODO: Replace this with GLG server id
    server_id = 1234
    guild = client.get_guild(server_id)

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


if __name__ == '__main__':
    client.run('use-token-here')
