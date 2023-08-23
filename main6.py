from discord.ext import commands
import discord

intents = discord.Intents.all()
thank_points = {}
reaction_counts = {} 
final_reactions = {}
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
            welcome_message = f"Welcome to the memes server, {member.mention}!,hope you will have fun here"
            await channel.send(welcome_message)
            await channel.send("there are few rules and regulation. To access them enter -- !rules --")

    @bot.event
    async def on_message(message):
        if not message.author.bot: 
            reaction_counts[message.jump_url] = sum(reaction.count for reaction in message.reactions)
        await bot.process_commands(message)
        print(reaction_counts)
    @bot.command()
    async def thanks(ctx, mention):
        await ctx.send(f"{mention} has been thanked!")
        await ctx.send(f"{mention} is the user")
        print(mention)
        if mention not in thank_points.keys():
            thank_points[mention] = 1
        else:
            thank_points[mention] += 1
        print(thank_points)

    @bot.command()
    async def thank_leaderboard(ctx):
        embed = discord.Embed(
            title="Leaderboard",
            description="Most Thanked Users",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url="https://e0.pxfuel.com/wallpapers/1020/999/desktop-wallpaper-artstation-indian-cricket-bcci-football-team-logo-sudip-samanta-cricket-logo-thumbnail.jpg")

        for key, value in thank_points.items():
            embed.add_field(name=key, value=value, inline=False)

        await ctx.send(embed=embed)
        print(thank_points)

    @bot.command()
    async def kick(ctx, user: discord.Member, reason: str = "for_not_following_rules"):
        if ctx.author.guild_permissions.kick_members:
            await user.kick(reason=reason)
            await ctx.send(f"{user.mention} has been kicked from the server. Reason: {reason}")
        else:
            await ctx.send("You do not have permission to kick members.")

    @bot.command()
    async def rules(ctx):
        await ctx.send("rules will be updated soon")

    @bot.command()
    async def count_reactions(ctx, message_link):
        try:
            message_id = int(message_link.split('/')[-1])
            message = await ctx.fetch_message(message_id)           
            n_reactions = 0
            for reaction in message.reactions:
                # reaction_counts[str(reaction.emoji)] = reaction.count
                n_reactions += reaction.count
                reaction_counts[message_link] = n_reactions

            total_reactions = reaction_counts.get(message_link, n_reactions)  #for takig reaction count from dictionary

            await ctx.send(f"Total reactions for {message_link}: {total_reactions}") 
            print(total_reactions)
        except Exception as e:
            await ctx.send("An error occurred. Make sure the message link is correct.")

    bot.run('MTEzMzM1NTUzOTI0MjQzMDUxNQ.G5C4nF.eDjSiACVE0yXnXNpMer7KW0MSshq3XUkaGaptg')

run()
