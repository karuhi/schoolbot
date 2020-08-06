import discord
from discord.ext import tasks, commands
from datetime import datetime
import asyncio
import os

bot = commands.Bot(command_prefix='$')
token = 'NzQwNTUxNDIzMjQyMTQxNjk2.XyqqQg.62N3VdEOZc_vPui4V11LwmlKfKQ'
# os.environ['DISCORD_BOT_TOKEN']
# 休日モードの日
enableWeekendModeDays = [0, 0, 0, 0, 0, 1, 1]
# お知らせするチャンネル
CHANNEL_ID = 740552175603679263

noticeMode = 0


@bot.event
async def on_ready():
    print('------ Logged in as ------')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------------')
# 時間に自動で通知するやつ
# 30秒に一回ループ


@tasks.loop(seconds=30.0)
async def loop():
    # 現在の時刻
    date = datetime.now()
    time = date.strftime('%H:%M')
    yobi = date.weekday()
    # 平日
    if enableWeekendModeDays[yobi] == 0:
        # 出席
        if time == '08:30':
            await day_morning()
            await asyncio.sleep(60)
        # 退席
        elif time == '16:00':
            await day_evening()
            await asyncio.sleep(60)
    # 休日
    elif enableWeekendModeDays[yobi] == 1:
        # 体調確認
        if time == '09:00':
            await end_morning()
            await asyncio.sleep(60)


async def day_morning():
    embed = discord.Embed(
        title="おはようございます、今日も一日頑張りましょう！",
        description="下のリンクからバーチャル登校をしましょう👍",
        color=discord.Colour.from_rgb(252, 223, 135))
    embed.add_field(
        name="リンク", value="[体調報告フォーム](https://forms.office.com/Pages/ResponsePage.aspx?id=XYP-cpVeEkWK4KezivJfyCCgyme_mRtApqvXifAdyEdUOUxUSjBLUDBRRk1HRTI2WklBUjI3S05OUy4u)")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)


async def day_evening():
    embed = discord.Embed(
        title="こんにちは、今日もお疲れ様です。",
        description="下のリンクからバーチャル下校をしましょう👍",
        color=discord.Colour.from_rgb(16, 19, 58))
    embed.add_field(
        name="リンク",
        value="[体調報告フォーム](https://forms.office.com/Pages/ResponsePage.aspx?id=XYP-cpVeEkWK4KezivJfyCCgyme_mRtApqvXifAdyEdUOUxUSjBLUDBRRk1HRTI2WklBUjI3S05OUy4u)")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)


async def end_morning():
    embed = discord.Embed(
        title="おはようございます、週末休めてますか？",
        description="下のリンクから体調報告をしましょう👍",
        color=discord.Colour.from_rgb(246, 135, 65))
    embed.add_field(
        name="リンク",
        value="[体調報告フォーム](https://forms.office.com/Pages/ResponsePage.aspx?id=XYP-cpVeEkWK4KezivJfyCCgyme_mRtApqvXifAdyEdUOUxUSjBLUDBRRk1HRTI2WklBUjI3S05OUy4u)")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(embed=embed)
# 時間に自動で通知するやつここまで
# コマンドたち


@bot.command()
async def notice_on(ctx):
    global noticeMode
    noticeMode = 1
    await ctx.send(":smiley: :wave: 通知を有効にしました")
    await bot.change_presence(activity=discord.Game("通知のお仕事"))


@bot.command()
async def notice_off(ctx):
    global noticeMode
    noticeMode = 0
    await ctx.send(":smiley: :wave: 通知を無効にしました")
    await bot.change_presence(activity=discord.Game("休暇(通知オフ)"))

# ロール自動付与(通知設定)
rolePost = ''


@bot.event
async def on_raw_reaction_add(payload):
    print("react!")
    if payload.message_id == rolePost.id:

        print(payload.emoji.name)
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        role = discord.utils.find(
            lambda r: r.name == payload.emoji.name, guild.roles)

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(
                lambda m: m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("done")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == rolePost.id:
        print(payload.emoji.name)

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        role = discord.utils.find(
            lambda r: r.name == payload.emoji.name, guild.roles)

        if role is not None:
            member = discord.utils.find(
                lambda m: m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            print("done")
# ロール用コマンド


@bot.command()
async def notice(ctx):
    embed = discord.Embed(
        title="通知設定", description="このメッセージにリアクションすることで通知設定ができます", color=0xeee657)
    embed.add_field(
        name="ヒント", value=":school_notice: をつけると通知がオンになります。")
    message = await ctx.send(embed=embed)
    global rolePost
    if rolePost != '':
        await rolePost.delete()
    rolePost = message

bot.remove_command('help')
# ヘルプコマンド


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="学校通知くん", description="便利なBOTでしょ？コマンドたちはこれ:", color=0xeee657)
    embed.add_field(name="$notice", value="通知設定をします", inline=False)
    embed.add_field(name="$notice_on", value="Bot通知をオンにします", inline=False)
    embed.add_field(name="$notice_off", value="Bot通知をオフにします", inline=False)
    embed.add_field(name="$help", value="このメッセージを送ります", inline=False)

    await ctx.send(embed=embed)

# ループ処理実行
loop.start()
# Botの起動とDiscordサーバーへの接続
bot.run(token)
