import discord
from replit import db
from discord.ext import commands
from webserver import keep_alive
import asyncio
import os

client = commands.Bot(command_prefix = '!', case_insensitive=True)

ALLOWEDCHARACTERS = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','a','b','c','d','e','f']
# db['Addresses'] = []
# db['IDs'] = []
# db['Usernames'] = []

def create_text(name,array):
  f = open(f"{name}.txt", "w")
  for item in array:
    f.write(f'{item}\n')
  f.close()

def valid_address(address):
    if len(address) != 42:
        print ("Wrong length",len(address))
        return False
    newaddress = address[2:42]
    for letter in newaddress:
        if letter not in ALLOWEDCHARACTERS:
            print("Wrong character",letter)
            return False
    return True
    
@client.command(name='printdb')
async def printdb(ctx):
  create_text('IDs',db['IDs'])
  create_text('Addresses',db['Addresses'])
  create_text('Usernames',db['Usernames'])

@client.event
async def on_message(message):

    await client.process_commands(message)
    if message.channel.id == 947088198029410356:
      if message.author == client.user:
        return
    
      if "whitelist" in [role.name.lower() for role in message.author.roles]:
        content = message.content
        await message.delete()
        
        if content == "blockwhite":
          tmpmsg = await message.channel.send('✅ Correct passcode! Please directly enter the wallet address.') 
          await asyncio.sleep(5)
          await tmpmsg.delete()
        # Record address
        if content[0:2] == '0x':
          if valid_address(content):
            if content not in db['Addresses']:
              db['IDs'].append(str(message.author.id))
              usernames = await client.fetch_user(message.author.id)
              db['Usernames'].append(str(usernames))
              db['Addresses'].append(content)
            # Send and delete msg
            tmpmsg = await message.channel.send('✅ Successful record whitelist address.')  
            await asyncio.sleep(5)
            await tmpmsg.delete()
          else:
            tmpmsg = await message.channel.send('❗Please enter the correct address format.')  
            await asyncio.sleep(5)
            await tmpmsg.delete()
        else:
          tmpmsg = await message.channel.send('❗Please enter the correct address format.')  
          await asyncio.sleep(5)
          await tmpmsg.delete()
      
      else:
      # Passcode correct
        if message.content == "blockwhite":
          await message.delete()
          # Add role
          role = discord.utils.get(message.guild.roles, name = "whitelist")        
          await message.author.add_roles(role)
          # Send and delete msg
          tmpmsg = await message.channel.send('✅ Correct passcode! Please directly enter the wallet address.')        
          await asyncio.sleep(5)
          await tmpmsg.delete()
        else: # Passcode error
          await message.delete()
          tmpmsg = await message.channel.send('❌ Wrong passcode.')
          await asyncio.sleep(5)
          await tmpmsg.delete()

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)