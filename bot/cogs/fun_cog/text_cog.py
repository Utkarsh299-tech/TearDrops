import discord
from discord.ext import commands
import random
from inputs import responses,fortunes, quo, nerd, tech, rost, bk, cmp, blurt, cf, jk, cfe, chill, cl, ur


class TextCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball"])
    async def magicball(ctx, *, question):
        embed = discord.Embed(title="8Ball :8ball:",
                              colour=discord.Color.magenta())
        embed.add_field(name=f"*Question: {question}*",
                value=f"Conjecture: {random.choice(responses)}")
        await ctx.send(embed=embed)


    @commands.command(aliases=["future"])
    async def fortune(ctx):
        embed = discord.Embed(title='Fortune', color=0x09b58d)
        embed.add_field(name='Your Fortune', value=random.choice(fortunes))
        await ctx.send(embed=embed)


    @commands.command(aliases=['wisdom'])
    async def quote(ctx):
        embed = discord.Embed(title='Quote', color=0x097b5)
        embed.add_field(name='Quote for you', value=f'`{random.choice(quo)}`')
        await ctx.send(embed=embed)


    @commands.command(aliases=['joke','pun'])
    async def dadjoke(ctx):
        embed = discord.Embed(title='Dad joke huh 😏', color=0x5511c2)
        embed.add_field(name=random.choice(jk),
                        value='_looks at you, expecting you to laugh_')
        await ctx.send(embed=embed)


    @commands.command(aliases=['nerdystuff','smartystuff','bigbrains'])
    async def nerd(ctx):
        embed = discord.Embed(title='Nerdy Stuff', color=0x22bfb0)
        embed.add_field(name='Take this you NERD', value=f'{random.choice(nerd)}')
        await ctx.send(embed=embed)


    @commands.command(aliases=['tehc', 'hackerman'])
    async def geek(ctx):
        embed = discord.Embed(title='Geek', color=0xc21155)
        embed.add_field(name="Ahh I am a hackerman",
                        value=f'{random.choice(tech)}')
        await ctx.send(embed=embed)


    @commands.command(aliases=['shame'])
    async def roast(ctx, member: discord.Member = None):
        if not member:
            user = ctx.message.author
        else:
            user = member
        embed = discord.Embed(title='Roast', color=0x11ad4b)
        embed.add_field(name='😈', value=f'{user}, {random.choice(rost)}')
        await ctx.send(embed=embed)


    @commands.command(aliases=['commend'])
    async def compliment(ctx, *, member: discord.Member = None):
        if not member:
            user = ctx.message.author
        else:
            user = member
        embed = discord.Embed(title='Compliment', color=0xa9e010)
        embed.add_field(name="Here's a compliment for you",
                        value = f'{user}, {random.choice(cmp)}')
        await ctx.send(embed=embed)


    @commands.command()
    async def flirt(ctx, *, member: discord.Member = None):
        if not member:
            user = ctx.message.author
        else:
            user = member
        embed = discord.Embed(title='Flirt', color=0xcf8c11)
        embed.add_field(name='Flirt it away',
                        value=f'{user}, {random.choice(blurt)}')
        await ctx.send(embed=embed)




