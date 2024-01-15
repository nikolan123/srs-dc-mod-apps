import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='*', intents=intents)
applied_users = set() 

bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
@commands.cooldown(1, 7, commands.BucketType.user)
async def apply(ctx):
    if ctx.author.id in applied_users:
        await ctx.send("You have already applied. Please wait before applying again.")
        return

    hmsg = await ctx.send("Thank you for applying! I will DM you a series of questions. Please answer each question.")

    questions = [
        "Thank you for applying for the Community Moderator position in SRS, before we start please review the requirements. If you do not meet the requirements, please don’t reply to this message. If you don’t answer within 300 seconds the application will be cancelled.\n\nRequirements:\n- Must have been in the server for at least 30 days\n- Must be active\n- Must be over the age of 13\n\nLet’s start with the first question, what’s your Discord name and id?",
        "Which position do you want to apply for?\n- Good Sirs (your gonna be rejected 99%)\n- Moderator\n- Supervisor",
        "For how long have you been a member of this server?",
        "How old are you?",
        "Why do you want to apply for this position?",
        "Do you have any prior experience in moderating? If so, please send a link too",
        "What are your hobbies?",
        "Will you actually moderate or do you just want the role?",
        "Why do you think you should be accepted?",
        "A member is spamming. What will you do? (Tell them to use #bsat / timeout / ban / tell them to stop / other)",
        "In which timezone are you?"
    ]

    answers = {}

    for question in questions:
        try:
            await ctx.author.send(question)
            
            def check(message):
                return message.author == ctx.author and message.guild is None

            try:
                response = await bot.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                await ctx.author.send("Time's up! You took too long to answer.")
                #await ctx.send("Time's up! You took too long to answer.")
                return

            answers[question] = response.content
        except discord.Forbidden:
            await hmsg.edit(content="It seems that your DMs are closed. Please enable DMs and run the command again.")
            return
    schan = bot.get_channel(1176268484888498186)

    application_message = f"Application from {ctx.author.mention} at {current_time}:\n"
    for question, answer in answers.items():
        application_message += f"{question}\n{answer}\n\n"
    
    await schan.send(application_message)
    applied_users.add(ctx.author.id)

    await ctx.author.send(f"Application completed! Your answers have submitted.")


@bot.command()
async def ping(ctx):
    ping = round(bot.latency*1000)
    await ctx.reply(f"pongy :3 {ping}")


bot.run('no u')
