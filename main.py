import discord, os
from discord.ext import commands, tasks
from Ink_Scraper import return_chap
from database import return_recent, add_to_table

client = discord.Client()
arr = ["https://ashenclouds.wordpress.com/2021/09/23/sword-pilgrim-%ea%b2%80%ec%9d%98-%ec%88%9c%eb%a1%80%ec%9e%90/",'https://ashenclouds.wordpress.com/2021/10/11/surviving-a-shounen-manga-%ec%86%8c%eb%85%84%eb%a7%8c%ed%99%94%ec%97%90%ec%84%9c-%ec%82%b4%ec%95%84%eb%82%a8%ea%b8%b0/','https://ashenclouds.wordpress.com/2021/10/21/surviving-the-game-as-a-barbarian-%ea%b2%8c%ec%9e%84-%ec%86%8d-%eb%b0%94%eb%b0%94%eb%a6%ac%ec%95%88%ec%9c%bc%eb%a1%9c-%ec%82%b4%ec%95%84%eb%82%a8%ea%b8%b0/']
bot = commands.Bot(command_prefix = "$")
set = False

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  send_update.start()

@client.event
async def on_message(message):
  m = message.content
  fin = False
  chap_num = ""
  

  if message.author == client.user:
    return 
  
  if m.startswith('$sword '):
    chap_num = m[7:]
    url = arr[0]
    id = "Sword_Pilgrim"
    add_to_table(id)

  if m.startswith('$shounen '):
    chap_num = m[9:]
    url = arr[1]
    id = "Shounen"
    add_to_table(id)
    
  if m.startswith('$barb '):
    chap_num = m[6:]
    url = arr[2]
    id = "Barbarian"
    add_to_table(id)

  fin = True
  
  if ('recent') in m:
   await message.channel.send(return_recent(id))
  elif ('timer') in m:
    global set
    set = message.channel
  else: 
    if fin == True and chap_num != "":
      send = return_chap(chap_num, url, id)
      if(send != ""):
        await message.channel.send(send)
      else:
        send = ""
             
@tasks.loop(seconds = 1)
async def send_update():
    li = []
    if set:
      li.append(return_chap(return_recent("Sword_Pilgrim")+1,     arr[0],"Sword_Pilgrim"))
      li.append(return_chap(return_recent("Shounen")+1,     arr[1],"Shounen"))
      li.append(return_chap(return_recent("Barbarian")+1,     arr[2],"Barbarian"))
    for i in range(len(li)):
      if li[i] != -1 and set:
        await set.send(embed = li[i])
        print(li[i])
    li.clear()

client.run(os.getenv('TOKEN'))