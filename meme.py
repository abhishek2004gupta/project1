from discord.ext import commands
import discord

intents = discord.Intents.all()
thank_points = {}
reaction_counts = {}
final_reactions = {}
max_reac = 0;
bot = commands.Bot(command_prefix="!", intents=intents)

def run():
    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name} - {bot.user.id}")
        print(thank_points)

    @bot.event
    async def on_member_join(member):
        channel = member.guild.system_channel
        if channel is not None:
            welcome_message = f"Welcome to the memes server, {member.mention}! Hope you will have fun here."
            await channel.send(welcome_message)
            await channel.send("There are a few rules and regulations. To access them, enter `!rules`.")

    @bot.event
    async def on_message(message):
        if not message.author.bot:
            await bot.process_commands(message)
        print(reaction_counts)

    @bot.event
    async def on_reaction_add(reaction, user):
        if not user.bot:
            message_link = reaction.message.jump_url
            reaction_counts[message_link] = reaction_counts.get(message_link, 0) + 1

    @bot.event
    async def on_reaction_remove(reaction, user):
        if not user.bot:
            message_link = reaction.message.jump_url
            reaction_counts[message_link] = max(0, reaction_counts.get(message_link, 0) - 1)

    @bot.command()
    async def count_reactions(ctx, message_link):
        try:
            total_reactions = reaction_counts.get(message_link, 0)
            await ctx.send(f"Total reactions for {message_link}: {total_reactions}")
            print(total_reactions)
        except Exception as e:
            await ctx.send("An error occurred. Make sure the message link is correct.")
    @bot.command()
    async def winner(ctx):
        try:
            max_reac = 0
            winners = []
            for i in reaction_counts.values():
                if i > max_reac:
                    max_reac = i;
            
            print(max_reac)
            for mess_link,count in reaction_counts.items():
                if count == max_reac:
                    winners.append(mess_link);
            print(winners)
            for link in winners:
                parts = link.split('/')
                guild_id = int(parts[-3])
                channel_id = int(parts[-2])
                message_id = int(parts[-1])

                guild = bot.get_guild(guild_id)
                if guild:
                    channel = guild.get_channel(channel_id)
                    if channel:
                        message = await channel.fetch_message(message_id)
                        await ctx.send(f"Winning message: {message.jump_url}")
                # link = i.split('/')
                # message = await self.bot.get_guild(int(link[-3])).get_channel(int(link[-2])).fetch_message(int(link[-1]))
                # await ctx.send(f"winning message {message}")
        except Exception as e:
            await ctx.send("An error occurred. Make sure the message link is correct.")

    bot.run('MTE0MjEyNzQwMjcyMjUyNTI3Ng.GUoPFZ.oI44cfjuY8XuME1NM4OJucfBJYZ2A4la02EVUE')

run()
