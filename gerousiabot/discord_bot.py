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
    server_id = 904082388794109962
    guild = client.get_guild(server_id)

    # TODO: Create function for this
    members = guild.members
    online_members = list(filter(lambda member: member.status.value == 'online', members))

    for online_member in online_members:
        print(online_member.name)


if __name__ == '__main__':
    client.run('insert-token-here')
